#!/usr/bin/env python3

# Original repo : https://github.com/flavienbwk/azure-spending-limits
# List and delete resource groups from a subscription.
# Configure the CLIENT_ID (Azure App Registration) to be able to read/delete SUBSCRIPTION's resource groups in the IAM of the the SUBSCRIPTION.

import requests

def filter_unique_strings(list1, list2):
    def is_substring_or_superstring(s1, s2):
        return s1 in s2 or s2 in s1
    return [s1 for s1 in list1 if not any(is_substring_or_superstring(s1, s2) for s2 in list2)]

# Azure app registration details
TENANT_ID = 'xxxxxxxxxxx' # In Azure AD
CLIENT_ID = 'xxxxxxxxxxx' # In Azure App Registration
CLIENT_SECRET = 'xxxxxxxxxxx'
RESOURCE = 'https://management.azure.com/'

# Azure resource details to be deleted
SUBSCRIPTION_ID = 'xxxxxxxxxxx'

# Endpoint for acquiring token
TOKEN_ENDPOINT = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"

# Additional param
EXCLUDED_RESOURCE_GROUP_SUBSTR = {
    "prod",
    "permanent"
}

# Acquire token
data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'resource': RESOURCE
}

token_response = requests.post(TOKEN_ENDPOINT, data=data)
token = token_response.json().get('access_token')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Retrieve all resource groups
LIST_RESOURCE_GROUPS_ENDPOINT = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourcegroups?api-version=2021-04-01"
response = requests.get(LIST_RESOURCE_GROUPS_ENDPOINT, headers=headers)

if response.status_code == 200:
    resource_groups = response.json().get('value', [])
    resource_groups_tbr = []  # final list of resource groups to be removed

    for rg_excl in EXCLUDED_RESOURCE_GROUP_SUBSTR:
        for rg in resource_groups:
            if rg_excl not in rg:
                resource_groups_tbr.append(rg)

    print("Resource groups to be deleted:")
    for rg in resource_groups_tbr:
        rg_name = rg['name']
        print(rg_name)
        
        # Delete the resource group
        DELETE_RG_ENDPOINT = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourcegroups/{rg_name}?api-version=2021-04-01"
        delete_response = requests.delete(DELETE_RG_ENDPOINT, headers=headers)
        
        if delete_response.status_code in [202, 204]:
            print(f"{rg_name}: Resource group deletion initiated successfully!")
        elif delete_response.status_code == 200:
            print(f"{rg_name}: Resource group deleted successfully!")
        else:
            print(f"{rg_name}: Error deleting resource group. HTTP Status Code: {delete_response.status_code}")
            print(delete_response.text)
else:
    print(f"Error retrieving resource groups. HTTP Status Code: {response.status_code}")
    print(response.text)
