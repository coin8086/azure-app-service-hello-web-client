import json
import logging
import adal
import urllib2

def request(url, token):
    req = urllib2.Request(url)
    req.add_header('Authorization', 'Bearer ' + token)
    resp = urllib2.urlopen(req)
    return resp.read()

# The information inside such file can be obtained via app registration.
# See https://github.com/AzureAD/azure-activedirectory-library-for-python/wiki/Register-your-application-with-Azure-Active-Directory

parameters = {
  "resource": "af161d7b-779c-4c7c-88b5-86b4dd8bcca7",
  "apiUrl": "https://helloapp2.azurewebsites.net/api/env",
  "tenant" : "microsoft.onmicrosoft.com",
  "authorityHostUrl" : "https://login.microsoftonline.com",
  "clientId" : "feb18e92-97ce-489a-b5db-34a448e1461d",
}

authority_host_url = parameters['authorityHostUrl']
authority_url = authority_host_url + '/' + parameters['tenant']
clientid = parameters['clientId']
GRAPH_RESOURCE = '00000002-0000-0000-c000-000000000000'
RESOURCE = parameters.get('resource', GRAPH_RESOURCE)

# Uncomment for verbose logging
# logging.basicConfig(level=logging.DEBUG)

context = adal.AuthenticationContext(authority_url)
code = context.acquire_user_code(RESOURCE, clientid)
print(code['message'])
token = context.acquire_token_with_device_code(RESOURCE, code, clientid)

print('Here is the token from "{}":'.format(authority_url))
print(json.dumps(token, indent=2))

print('Here is the result from "{}":'.format(parameters['apiUrl']))
result = request(parameters['apiUrl'], token['accessToken'])
print(json.dumps(json.loads(result), indent=2))

# # token refreshing
# refresh_token = token['refreshToken']
# token = context.acquire_token_with_refresh_token(
#     refresh_token,
#     parameters['clientId'],
#     RESOURCE,
# )
# print('\nHere is the refreshed token:')
# print(json.dumps(token, indent=2))
