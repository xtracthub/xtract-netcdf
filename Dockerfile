FROM python:3.6

MAINTAINER Ryan Wong

COPY xtract_netcdf_main.py /

RUN pip install netCDF4 numpy git+https://github.com/Parsl/parsl git+https://github.com/DLHub-Argonne/home_run

#ENTRYPOINT ["python", "xtract_netcdf_main.py"]

