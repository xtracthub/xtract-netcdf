FROM python:3.6

MAINTAINER Ryan Wong

COPY xtract_netcdf_main.py requirements.txt /

RUN pip install -r requirements.txt
RUN pip install git+https://github.com/Parsl/parsl git+https://github.com/DLHub-Argonne/home_run

#ENTRYPOINT ["python", "xtract_netcdf_main.py"]

