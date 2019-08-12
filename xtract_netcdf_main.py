import json
import os
from netCDF4 import Dataset
import numpy as np
import argparse
import time
"""
    This is the code for the NetCDF extractor.  This takes a file deemed 
    a NetCDF file and extracts all metadata from it as a JSON.

    @Inputs: file_handle -- opened NetCDF file.
    @Outputs: metadata -- metadata JSON

    @Author: Tyler J. Skluzacek, derived from code by Paul Beckman.
    @LastEdited: 07/27/2017
"""


class ExtractionFailed(Exception):
    """Basic error to throw when an extractor fails"""


class ExtractionPassed(Exception):
    """Indicator to throw when extractor passes for fast file
    classification."""


class NumpyDecoder(json.JSONEncoder):
    """Serializer used to convert numpy types to normal json
    serializable types. Since netCDF4 produces numpy types, this is
    necessary for compatibility with other metadata scrapers like the
    tabular, which returns a python dict."""
    def default(self, obj):
        if isinstance(obj, np.generic):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.dtype):
            return str(obj)
        else:
            return super(NumpyDecoder, self).default(obj)


def extract_netcdf_metadata(file_handle, pass_fail=False):
    """Create netcdf metadata dictionary from file.

    ParametersL
    file_handle (str): File path of netcdf file.
    pass_fail (bool): Whether to exit after loading file_handle to a
    netCDF4 dataset.

    Return:
    (dictionary): Dictionary of file format, global attributes,
    dimensions, variables and attributes.
    """
    try:
        dataset = Dataset(os.path.realpath(file_handle))
    except IOError:
        raise ExtractionFailed

    if pass_fail:
        raise ExtractionPassed

    metadata = {
        "file_format": dataset.file_format,
    }
    if len(dataset.ncattrs()) > 0:
        metadata["global_attributes"] = {}
    for attr in dataset.ncattrs():
        metadata["global_attributes"][attr] = dataset.getncattr(attr)

    dims = dataset.dimensions
    if len(dims) > 0:
        metadata["dimensions"] = {}
    for dim in dims:
        metadata["dimensions"][dim] = {
            "size": len(dataset.dimensions[dim])
        }
        add_ncattr_metadata(dataset, dim, "dimensions", metadata)

    variables = dataset.variables
    if len(variables) > 0:
        metadata["variables"] = {}
    for var in variables:
        if var not in dims:
            metadata["variables"][var] = {
                "dimensions": dataset.variables[var].dimensions,
                "size": dataset.variables[var].size
            }
        add_ncattr_metadata(dataset, var, "variables", metadata)

    return json.loads(json.dumps(metadata, cls=NumpyDecoder))


def add_ncattr_metadata(dataset, name, dim_or_var, metadata):
    """Gets attributes from a netCDF variable or dimension.

    Parameters:
    dataset (netCDF4 dataset): netCDF4 dataset loaded from a netcdf
    file.
    name (str): Name of attribute.
    dim_or_var (str): Metadata key for attribute info ("dimensions"
    or "variables")
    metadata (dictionary): Dictionary to add attribute info to.
    """
    try:
        metadata[dim_or_var][name]["type"] = dataset.variables[name].dtype
        for attr in dataset.variables[name].ncattrs():
            metadata[dim_or_var][name][attr] = dataset.variables[name].getncattr(attr)
    except KeyError:
        pass


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("--path", help="path to netcdf file",
                       type=str, required=True)
    args = parse.parse_args()

    t0 = time.time()
    meta = {"netcdf": extract_netcdf_metadata(args.path)}
    t1 = time.time() - t0
    meta.update({"extract time": t1})
    print(meta)
    print(t1)



