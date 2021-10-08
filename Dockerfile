FROM python:3.6

MAINTAINER Tyler J. Skluzacek (skluzacek@uchicago.edu)

COPY xtract_netcdf_main.py requirements.txt /
COPY test_files /

RUN pip install -r requirements.txt
