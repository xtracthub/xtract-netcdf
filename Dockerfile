FROM python:latest

MAINTAINER Ryan Wong

COPY xtract_netcdf_main.py /

RUN pip install netCDF4 numpy

ENTRYPOINT ["python", "xtract_netcdf_main.py"]

