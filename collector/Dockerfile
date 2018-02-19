FROM python:2.7-alpine
ADD collector.py /collector/
ADD test_data.py /collector/
RUN mkdir -p /tmp/var/cbackup/storage/lxd1.odinson.net
WORKDIR /collector
CMD ["python", "test_data.py"]