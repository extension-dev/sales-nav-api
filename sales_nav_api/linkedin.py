"""
Provides linkedin api-related code
"""
import json
import logging
import random
from operator import itemgetter
from time import sleep, time
from urllib.parse import urlencode, quote, unquote, urlparse, parse_qs

from sales_nav_api.client import Client
from sales_nav_api.utils.helpers import get_id_from_urn, safe_get

import requests
import re

def default_evade():
    """
    A catch-all method to try and evade suspension from Linkedin.
    Currenly, just delays the request by a random (bounded) time
    """
    sleep(random.randint(2, 5))  # sleep a random duration to try and evade suspention

class LinkedIn(object):
    def __init__(
        self,
        li_at,
    ):
        """Constructor method"""
        self.client = Client(
            li_at = li_at,
            li_a  = None,
        )
        self.client.initiate()

    def _fetch(self, url, evade=None):
        """GET request to Linkedin API"""
        if evade is not None:
            evade()

        return self.client.fetch(url)

    def _post(self, url, args, evade=None):
        """POST request to Linkedin API"""
        if evade is not None:
            evade()

        return self.client.post(url, args)

    def _parse_search_results(self, data):
        people = []
        for idx, connection in enumerate(data):
            entity_urn = connection['entityUrn']
            sales_nav_id = entity_urn[entity_urn.find("(") + 1 : entity_urn.find(")")]
            data_point = {
                "fullName": connection['fullName'],
                "location": connection['geoRegion'],
                "degree": connection['degree'],
                "sales_nav_url": f"https://www.linkedin.com/sales/people/{sales_nav_id}"
            }

            if len(connection['currentPositions']):
                data_point.update({  
                    "company_name": connection['currentPositions'][0]['companyName'],
                    "current_title": connection['currentPositions'][0]['title'],
                })

                if 'companyUrn' in connection['currentPositions'][0].keys():
                    company_urn = connection['currentPositions'][0]['companyUrn']
                    company_uid = company_urn.split(':')[-1]
                    data_point.update({  
                        "company_sales_url": f"https://www.linkedin.com/sales/company/{company_uid}"
                    })

            people.append(data_point)

        return people

    def _get_uid_from_url(self, url):
        resp = self.client.fetch(url)
        pattern = r'&quot;urn:li:fs_profileNetworkInfo:([A-Za-z0-9_-]+)&quot'
        result = re.search(pattern, resp.text)
        uid = result.group(1)
        return uid

    ############
    # GET APIs #
    ############
    def get_profile_data(self, url):
        uid = self._get_uid_from_url(url)
        query_url = f"https://www.linkedin.com/voyager/api/identity/profiles/{uid}"

        resp = self.client.fetch(query_url)
        result = resp.json()
        profile_result = {
            "url": url,
            "first_name": safe_get(result, 'firstName'),
            "last_name": safe_get(result, 'lastName'),
            "industry": safe_get(result, 'industry'),
            "location": safe_get(result, 'locationName'),
            "conutry": safe_get(result, 'geoCountryName'),
            "headline": safe_get(result, 'headline'),
            "person_urn": safe_get(result, 'entityUrn'),
            "tracking_id": safe_get(result['miniProfile'], 'trackingId')
        }
        return profile_result

    #############
    # POST APIs #
    #############
    def send_invitation(self, receipient_urn, tracking_id, message, evade=None):
        uid = get_id_from_urn(receipient_urn)
        payload = {
            'emberEntityName': 'growth/invitation/norm-invitation',
            'invitee': {
                'com.linkedin.voyager.growth.invitation.InviteeProfile': {
                    'profileId': uid
                }
            },
            'message': message,
            'trackingId': tracking_id
        }

        if evade is not None:
            evade()

        post_url = 'https://www.linkedin.com/voyager/api/growth/normInvitations'
        resp = self._post(post_url, payload, evade)

        if resp.status_cde != 201:
            resp.raise_for_status()