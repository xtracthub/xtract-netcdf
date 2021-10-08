#!/bin/bash

IMAGE_NAME='xtract-netcdf'

docker rmi -f $IMAGE_NAME

docker build -t $IMAGE_NAME .
