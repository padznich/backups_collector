
# -*- coding: utf-8 -*-

import os

from collector import normalize_storage


def init_fake_files(s):
    names = [
        "2016-01-01--00-00-00_etc.00.tar.gz",
        "2016-01-03--00-00-00_etc.00.tar.gz",
        "2016-01-02--00-00-00_etc.00.tar.gz",  # to yearly
        "2017-12-03--00-00-00_etc.00.tar.gz",  # to yearly

        "2as018-01-01--00-00-00_etc.00.tar.gz",  # ignored
        "2018-01-01--00-00-00_etc.00.tar.gz",
        "2018-01-02--00-00-00_etc.01.tar.gz",
        "2018-01-03--00-00-00_etc.02.tar.gz",
        "2018-01-04--00-00-00_etc.00.tar.gz",
        "2018-01-05--00-00-00_mysql.tar.gz",

        "2018-02-05--00-00-00_mysql.tar.gz",

        "2222-02-05--00-00-00_mysql.tar.gz",
    ]

    for f in names:
        with open(os.path.join(s, f), 'w'):
            pass

    print('%s Fake Data Prepared!' % s)


if __name__ == '__main__':
    # DEBUG
    BASE_DIR = '/tmp/var/cbackup/storage'

    init_fake_files(os.path.join(BASE_DIR, 'lxd1.odinson.net', 'backup_filtered'))
    normalize_storage(BASE_DIR)

    # yearly_path = os.path.join(BASE_DIR, 'lxd1.odinson.net/yearly')
    # monthly_path = os.path.join(BASE_DIR, 'lxd1.odinson.net/monthly')
    #
    # # DOCKER output
    # print('NORMALIZED STORAGE!')
    # print('\n'.join(
    #     ['=' * 20 + BASE_DIR,
    #      '\n'.join(os.listdir(BASE_DIR)),
    #      '+' * 40]
    # ))
    # print('\n'.join(
    #     ['=' * 20 + monthly_path,
    #      '\n'.join(os.listdir(monthly_path)),
    #      '+' * 40]
    # ))
    # print('\n'.join(
    #     ['=' * 20 + yearly_path,
    #      '\n'.join(os.listdir(yearly_path)),
    #      '+' * 40]
    # ))
    # print('\n'.join(
    #     ['=' * 40 + 'lxd1.odinson.net',
    #      '\n'.join(
    #          os.listdir(os.path.join(BASE_DIR, 'lxd1.odinson.net/'))[:5]
    #      ),
    #      '+' * 40]
    # ))
