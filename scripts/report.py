#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pprint

import requests
from requests_oauthlib import OAuth2Session

api_url = 'https://api.fr-stage.cloud.gov'
token_url = 'https://login.fr-stage.cloud.gov'
report_url = 'https://abacus-usage-reporting.fr-stage.cloud.gov'

resp = requests.post(
    '{}/oauth/token'.format(token_url),
    auth=(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET')),
    data={'grant_type': 'client_credentials', 'response_type': 'token'},
)

session = OAuth2Session(os.getenv('CLIENT_ID'), token=resp.json())

resp = session.get('{}/v2/organizations'.format(api_url))
orgs = resp.json()['resources']

report = {}

for org in orgs:
    resp = session.get(
        '{}/v1/metering/organizations/{}/aggregated/usage'.format(
            report_url, org['metadata']['guid']
        ),
    )
    try:
        usage = resp.json()['resources'][0]['plans'][0]['aggregated_usage'][0]['windows'][-1][0]['summary']
        report[org['metadata']['guid']] = {
            'name': org['entity']['name'],
            'usage': usage,
        }
    except (IndexError, KeyError):
        pass

pprint.pprint(report)
