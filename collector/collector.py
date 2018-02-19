#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
cbackup collector

1.  add /var/cbackup/storage/$SERVERNAME/monthly
    add /var/cbackup/storage/$SERVERNAME/yearly
2.  search last lxd, mysql, files for each month & year
3.  copy to /monthly
    copy to /yearly
4.  remove backups older than 30 days

"""
import os
import re
from datetime import datetime
from itertools import groupby
from shutil import copy2, rmtree


# SETUP
BASE_DIR = '/var/cbackup/storage'
DAYS_LIMIT = 30

# Constants
DATE_FORMAT = '%Y-%m-%d--%H-%M-%S'


# incremental backups pattern
pattern = re.compile(r'^\w+.\d{2}[.\w]+$')


def add_directory(root_path, name):
    """
    Creates folder. Handle exception in case of folder already exists.

    :param root_path: [STRING].
    :param name: [STRING].
    :return: [BOOL].
    """
    folder_path = os.path.join(root_path, name)
    try:
        os.mkdir(folder_path)
    except OSError:
        # print('{} already exists'.format(folder_path))
        return False
    return True


def group_backups(backups, year=None):
    """
    Get map of last in month backups.
    Only full backups.

    :param backups: type: list[str]. ex: ["2017-12-04--00-00-00_etc.02.tar.gz"].
    :param year: type: None. Used to manage group by. None - Month, Year - otherwise
    :return: type: tuple[ dict[str, list[str]], list[str]].
        ex: ({'etc.00.tar.gz': ['2016-01-03--00-00-00']},  ["2017-12-04--00-00-00_etc.02.tar.gz"]).
    """
    current_date = datetime.now()
    if year is None:
        group_by_tag = 7
    else:
        group_by_tag = 4

    # compose dict. backup name as a key. list of last dates for each month/year as a value
    last_in_map = {}  # type: dict[str, list[str]]
    outdated_backups = []
    for row in backups:
        _date, backup_name = row.split('_')

        row_date = datetime.strptime(_date, DATE_FORMAT)  # type: datetime

        # aggregate outdated backups
        if (current_date - row_date).days > DAYS_LIMIT:
            outdated_backups.append(backup_name + '_' + _date)

        # for yearly backup skip current year
        if year and row_date.year >= current_date.year:
            print('Skip current year for %s' % _date + '_' + backup_name)
            continue

        # for monthly backup skip current month
        if row_date.year >= current_date.year and row_date.month >= current_date.month and year is None:
            print('Skip current month for %s' % _date + '_' + backup_name)
            continue

        # skip not full incremental backups
        if pattern.match(backup_name) and '00' not in backup_name:
            print('Skip incremental backup for %s' % _date + '_' + backup_name)
            continue

        # aggregate return map
        if last_in_map.get(backup_name):
            last_in_map[backup_name].append(_date)
            last_in_map[backup_name] = [
                # Get last dates for grouped items
                sorted(i[1], reverse=True)[0] for i in
                # GROUP BY year-month. !! sorted - is required !!
                groupby(sorted(last_in_map[backup_name]), lambda x: x[:group_by_tag])
            ]
        else:
            last_in_map[backup_name] = [_date]

    return last_in_map, outdated_backups


def copy_backups(path, backups, server_name, folder):
    """
    Used to execute system call.
    Copy files to specified destination.

    :param path: type: str.
    :param backups: type: dict[str, list[str]].
    :param server_name: type: str.
    :param folder: type: str.
    :return: type: bool.
    """
    backup_dst = os.path.join(path, server_name, folder)
    for backup_name, _dates in backups.items():
        for _date in _dates:
            backup_src = os.path.join(path, server_name, _date + '_' + backup_name)
            print(' -> '.join((backup_src, backup_dst)))  # log
            copy2(backup_src, backup_dst)

    return True


def remove_backups(path, server_name, backups):
    """
    Used to remove backups

    :param path: type: str.
    :param server_name: type: str.
    :param backups: type: list[str].
    :return: type: bool.
    """
    for backup in backups:
        backup_path = os.path.join(path, server_name, backup)
        print('Remove outdated backup: %s' % backup_path)
        rmtree(backup_path, ignore_errors=True)
    return True


def normalize_storage(path):
    """
    Used to copy last full backup in month into monthly/ folder.
    And removes all backups older than specified DAYS_LIMIT.

    :param path: type: str. ex: '/var/cbackup/storage'.
    :return: type: bool.
    """
    for child in os.listdir(path):

        child_path = os.path.join(path, child)
        server_files = [f_name for f_name in os.listdir(child_path) if f_name not in ['monthly', 'yearly']]

        if server_files:

            # copy to monthly folder
            print('\t\t-= Copy monthly backups for {} =-'.format(child))  # log
            monthly_backups_map, outdated_backups = group_backups(server_files)
            if monthly_backups_map:
                # add aggregation folder
                add_directory(child_path, 'monthly')
                copy_backups(path, monthly_backups_map, child, 'monthly')
            print('')  # log

            # copy to yearly folder
            print('\t\t-= Copy yearly backups for {} =-'.format(child))  # log
            yearly_backups_map, _ = group_backups(server_files, year=True)
            if yearly_backups_map:
                # add aggregation folder
                add_directory(child_path, 'yearly')
                copy_backups(path, yearly_backups_map, child, 'yearly')

            # remove outdated backups
            remove_backups(path, child, outdated_backups)

            print('')  # log
    return True


if __name__ == '__main__':
    normalize_storage(BASE_DIR)
