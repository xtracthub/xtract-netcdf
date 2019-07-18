#!/bin/bash

IMAGE_NAME='xtract_netcdf_image'

docker rmi -f $IMAGE_NAME

docker build -t $IMAGE_NAME .
