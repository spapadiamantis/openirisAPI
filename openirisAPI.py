"""
Small API for openiris.io using Python Requests.
Downstream flow only, no support for create and
update operations for the time being.

Author: Sotiris Papadiamantis
"""

import requests
import pandas as pd
import ast
import json
import utilities

def getBookings(cookies,start='2002-03-07',end='2024-03-07'):
    """
    Downloads all bookings linked to a specific cookie
    
    Args:
        cookies: cookie used for the request
        start: start date to filter results
        end: end date to filter results

    Returns:
        Dataframe of all bookings between start and end dates
    """

    # Set up request url
    url = 'https://iris.science-it.ch/resourcesAdminBookings/query'

    # Get response
    data_raw = requests.post(url,params={'from':start,'to': end}, cookies=cookies)

    # Return formatted data
    return utilities.data_from_raw(data_raw.content,data_field="Data")


def getGroupIDs(cookies):
    """
    Downloads a list of all group ids linked to an account
    
    Args:
        cookies: cookie used for the request

    Returns:
        list of all group ids linked to an account via cookie
    """

    # Set up request url
    url = 'https://iris.science-it.ch/groups/query'

    # Get response
    data = requests.post(url,cookies=cookies)

    # Return request content
    return data.content

def getProviderIDs(cookies):
    """
    Downloads a list of all provider ids linked to an account
    
    Args:
        cookies: cookie used for the request

    Returns:
        list of all provider ids linked to an account via cookie
    """

    # Set up request url
    url = 'https://iris.science-it.ch/billingTemplates/queryProviders'

    # Make request
    data_raw = requests.post(url,cookies=cookies)
    
    # Return formatted data
    return utilities.data_from_raw(data_raw.content)
    

def getUsers(cookies,start='2021-03-07',end='2023-03-08', to_csv=False):
    """
    Downloads a dataframe with information on all users that are
    administered by the account linked to the cookie
    
    Args:
        cookies: cookie used for the request
        start: start date to filter results
        end: end date to filter results
        to_csv: flag to save dataframe in csv form

    Returns:
        data: dataframe of all users
    """

    # Set up request url
    url = 'https://iris.science-it.ch/admin-users'

    # Get a list of all provider IDs
    providerIds = getProviderIDs(cookies)

    # Initiate list of providers
    providerList = []

    # Initiate list of result dataframes
    df_list = []

    # For each provider
    for i in providerIds['Id']:

        # Perform request
        data_raw = requests.post(url,params={'from':start, 'to':end,'providerID':i},cookies=cookies)

        # Format data
        data = utilities.data_from_raw(data_raw.content,"Data")

        # Append to list of dataframes
        df_list.append(data)

    # Concatenate dataframes
    data = pd.concat(df_list)

    # If store to csv flag
    if to_csv:
        # Store to file
        data.to_csv('users.csv')

    # Return dataframe
    return data

def getResourcesForProvider(cookies,providerId):
    """
    Downloads a dataframe with information on all resource that are
    administered by a specific provider
    
    Args:
        cookies: cookie used for the request
        providerId: ID of the provider whose resources we will download

    Returns:
        data: dataframe of all resources in provider with providerId
    """

    # Set up request url
    url = 'https://iris.science-it.ch/admin-users/resources'

    # Perform the request
    raw_data = requests.post(url,params={'providerID':providerId},cookies=cookies)

    # Return formatted data
    return utilities.data_from_raw(raw_data.content)


def getAllResources(cookies, to_csv=False):
    providerIds = getProviderIDs(cookies)
    df_list = [] 
    for i in providerIds['Id']:
        df_list.append(getResourcesForProvider(cookies,providerId=i))
    df = pd.concat(df_list)
    if to_csv:
        df.to_csv('resources.csv')
    return df


###### Statistics ########

def listRecourceIDs(cookies):

    return getAllResources(cookies)['ResourceId'].tolist()

def getResourceStatistics(cookies,resources=[],start='2021-03-07',end='2022-03-07'):
    if not resources:
       resources = listRecourceIDs(cookies)
    url = 'https://iris.science-it.ch/statistics/queryResourcesUtilization'
    raw_data = requests.post(url,params={'resources':resources,'from':start,'to':end, 'timeInterval':1,'mode':1},cookies=cookies)
    return data_from_raw(raw_data.content,data_field=False)


def getHeatmapData(cookies,resources=[], start='2021-03-07',end='2022-03-07'):
    if not resources:
       resources = listRecourceIDs(cookies)
    url = 'https://iris.science-it.ch/statistics/queryHeatmapData'
    raw_data = requests.post(url,params={'resources':resources,'from':start,'to':end},cookies=cookies)
    return data_from_raw(raw_data.content,data_field=False)

def getTotalsReportData(cookies,resources=[], start='2021-03-07',end='2022-03-07', mode='user'):
    if not resources:
       resources = listRecourceIDs(cookies)
    url = 'https://iris.science-it.ch/statistics/queryTotalsReportData'
    raw_data = requests.post(url,params={'resources':resources,'from':start,'to':end,'mode':mode},cookies=cookies)
    return data_from_raw(raw_data.content,data_field="OrganizationItems")

def getResourceUsageByUser(cookies,resources=[], start='2021-03-07',end='2022-03-07',mode='scheduled'):
    if not resources:
       resources = listRecourceIDs(cookies)
    url = 'https://iris.science-it.ch/statistics/queryResourceUsageByUser'
    raw_data = requests.post(url,params={'resources':resources,'from':start,'to':end,'mode':mode},cookies=cookies)
    return data_from_raw(raw_data.content,data_field="Items")

def getResourceTypes(cookies, providers=[]):
    if not providers:
       providers = getProviderIDs(cookies)
    url = 'https://iris.science-it.ch/adminresourcetypes/queryadminproviders'
    raw_data = requests.post(url,params={'Providers':providers},cookies=cookies)
    return data_from_raw(raw_data.content,data_field="ParentTypes")

def test_request():
    url = 'https://iris.science-it.ch/Resources?_=1646646300367'
    data = requests.get(url)
    return data.content

def getProviderViews(cookies):
    resources = listRecourceIDs(cookies)
    views = []
    for i in resources:
        views.append(getResourceViews(cookies,14898))
    return resources, views

def getCommunitiesID(cookies):
    url = 'https://iris.science-it.ch/communities/query'
    data_raw = requests.post(url,cookies=cookies)
    return data_from_raw(data_raw.content,data_field="Data")

def getCommunityUsers(cookies, community_id):
    url = 'https://iris.science-it.ch/communities/querycommunityusers'
    data_raw = requests.post(url,params={'id':community_id},cookies=cookies)
    return data_from_raw(data_raw.content,data_field="Data")

def getCommunityLinkedGroups(cookies, community_id):
    url = 'https://iris.science-it.ch/communities/queryLinkedGroups'
    data_raw = requests.post(url,params={'id':community_id},cookies=cookies)
    return data_from_raw(data_raw.content,data_field="Data")


