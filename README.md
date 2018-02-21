Backups Collector
===

Used to collect last full backups for each month.

Aggregation for last month-backups to $SERVER ```monthly/``` folder.

Aggregation for last year-backups to $SERVER ```yearly/``` folder.

```
For monthly collector - current month is not considering
For yearly collector - current year is not considering
```

Backups older than ```30 days``` must be ```deleted```.


Set Up
===
At collector/collector.py specify BASE_DIR. 

Default path: ```/var/cbackup/storage ```


Usage
===
```
$ python collector/collector.py
```
