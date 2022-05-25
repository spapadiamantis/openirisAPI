"""
Simple utility module used for the OpenIrisAPI

Author: Sotiris Papadiamantis
"""
import pandas as pd
import json
import ast

def data_from_raw(data,data_field=" "):
    """
    Simple data extraction function from request response

    Args:
        data: response.content attribute
        data_field: Data field name to extract info

    Returns
        Pandas dataframe of response data
    """
    dict_str = data.decode("UTF-8")
    if data_field ==" ":
       return(pd.DataFrame.from_dict(json.loads(dict_str)))
    elif data_field == "Data":
        return(pd.DataFrame.from_dict(json.loads(dict_str)["Data"]))
    else:
        return(pd.DataFrame.from_dict(json.loads(dict_str)[data_field]))

def get_cookie(filepath='cookie.txt'):
    """
    Read cookie stored in filepath
    
    Args:
        filepath: filepath of txt file storing login cookie

    Returns:
        cookie in python dictionary format
    """

    # Read raw data from file
    with open(filepath) as f:
        data = f.read()

    # Return python dictionary
    return ast.literal_eval(data)
