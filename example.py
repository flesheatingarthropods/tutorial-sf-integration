#!/usr/bin/python

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import requests #simple_salesforce builds on requests instead httplib2
from simple_salesforce import Salesforce

def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    service_account_email,
    key_file_location,
    scopes = scope
  )

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service

def get_sf_service(sfuser,sfpass,sftoken):
    sf = Salesforce(username=sfuser, password=sfpass, security_token=sftoken)
    return sf

def get_results(service, profile_id):
  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='90daysAgo',
      end_date='today',
      dimensions='ga:dimension1,ga:source,ga:medium,ga:campaign',
      metrics='ga:sessions').execute()

def update_sf_lead(sf_service, row):
    try:
        sf_row = sf_service.Lead.get_by_custom_id('gaid__c', row[0])
        if sf_row:
            id = sf_row['Id']
            sf_service.lead.update(id,{'source__c': row[1] , 'medium__c': row[2] , 'campaign__c': row[3]})
            print "Lead updated from row with Id " + row[0]
    except Exception, Argument:
        # print  Argument
        print "Row with Id " + row[0] + " did not update anything"


def main():

  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  sfuser = "xxx"
  sfpass = "xxx"
  sftoken = "xxx"

  service_account_email = "xxx"
  key_file_location = "client_secrets.p12"
  profile = "xxx"

  sf_service = get_sf_service(sfuser,sfpass,sftoken)
  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,service_account_email)

  results = get_results(service, profile)
  if results.get('rows', []):
    for row in results.get('rows'):
        update_sf_lead(sf_service, row)

if __name__ == '__main__': main()
