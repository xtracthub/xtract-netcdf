#!/bin/bash

IMAGE_NAME='xtract_netcdf_image'

args_array=("$@")
DIRECTORY=("${args_array[@]:0:1}")   
CMD_ARGS=("${args_array[@]:1}")

docker run -it -v "${DIRECTORY[@]}":/"${DIRECTORY[@]}" $IMAGE_NAME "${CMD_ARGS[@]}"

