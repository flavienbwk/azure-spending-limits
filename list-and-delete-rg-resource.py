#!/usr/bin/env python3

# Original repo : https://github.com/flavienbwk/azure-spending-limits
# List and delete resources from a resource group using the Azure API.
# Configure the CLIENT_ID (Azure App Registration) to be able to read/delete RESOURCE_GROUP's resources in the IAM of the RESOURCE_GROUP.

import requests

def extract_type_prefix(input_string):
    if '/' in input_string:
        return input_string.split('/')[0]
    return input_string

# Azure app registration details
TENANT_ID = 'xxxxxxxxxxx' # In Azure AD
CLIENT_ID = 'xxxxxxxxxxx' # In Azure App Registration
CLIENT_SECRET = 'xxxxxxxxxxx'
RESOURCE = 'https://management.azure.com/'

# Azure resource details to be deleted
SUBSCRIPTION_ID = 'xxxxxxxxxxx'
RESOURCE_GROUP = 'xxxxxxxxxxx'
RESOURCE_TYPE = 'accounts'

# Endpoint for acquiring token
TOKEN_ENDPOINT = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"

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

RESOURCES_PROVIDER_AND_NAME = []
LIST_RESOURCES_ENDPOINT = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/resources?api-version=2021-04-01"
response = requests.get(LIST_RESOURCES_ENDPOINT, headers=headers)
if response.status_code == 200:
    resources = response.json().get('value', [])
    print("Resources in the resource group:")
    for resource in resources:
        RESOURCES_PROVIDER_AND_NAME.append({
            "provider": extract_type_prefix(resource['type']),
            "name": resource['name']
        })
        print(resource['name'])
else:
    print(f"Error retrieving resources. HTTP Status Code: {response.status_code}")
    print(response.text)

print("\n")

# Delete the resource
API_VERSION_FROM_PROVIDER = {
    "Microsoft.Bing": "2020-06-10",
    "Microsoft.CognitiveServices": "2021-04-30"
}
for resource in RESOURCES_PROVIDER_AND_NAME:
    print(f"{resource['name']}: Deleting...")
    DELETE_ENDPOINT = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/{resource['provider']}/{RESOURCE_TYPE}/{resource['name']}?api-version={API_VERSION_FROM_PROVIDER[resource['provider']]}"
    response = requests.delete(DELETE_ENDPOINT, headers=headers)
    if response.status_code in [202, 204]:
        print(f"{resource['name']}: Resource deletion initiated successfully!")
    elif response.status_code == 200:
        print(f"{resource['name']}: Resource deleted successfully!")
    else:
        print(f"{resource['name']}: Error deleting resource. HTTP Status Code: {response.status_code}")
        print(response.text)
