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

def default_evade():
    """
    A catch-all method to try and evade suspension from Linkedin.
    Currenly, just delays the request by a random (bounded) time
    """
    sleep(random.randint(2, 5))  # sleep a random duration to try and evade suspention


class SalesNavigator(object):
    def __init__(
        self,
        li_at,
        li_a
    ):
        """Constructor method"""
        self.client = Client(
            li_at = li_at,
            li_a  = li_a,
        )
        self.client.initiate()

    def _fetch(self, url, evade=default_evade):
        """GET request to Linkedin API"""
        # evade()
        return self.client.fetch(url)

    def _post(self, uri, evade=default_evade):
        """POST request to Linkedin API"""
        evade()

        url = f"{self.client.LINKEDIN_BASE_URL}{uri}"
        return self.client.session.post(url, **kwargs)

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


    ##################
    # below are APIs #
    ##################
    def get_connections_to_person(
        self,
        person_link,
        company=None,
        start_from=0,
        count=25
    ):
        # build target URN
        target_uid = person_link.split('/')[5];
        urn_string = quote(f"urn:li:fs_salesProfile:({target_uid})")
        
        # build company string
        company_string = ""
        if company:
            company_string = f"companyV2:(scope:CURRENT,includedValues:List((text:{company}))),"

        url = f"{self.client.LINKEDIN_BASE_URL}/sales-api/salesApiPeopleSearch?q=peopleSearchQuery&start={start_from}&count={count}&query=({company_string}doFetchHeroCard:false,spellCorrectionEnabled:true,spotlightParam:(selectedType:ALL),doFetchFilters:true,doFetchHits:true,doFetchSpotlights:true,pivotParam:(com.linkedin.sales.search.AllConnectionsPivotRequest:(targetMember:{urn_string})))&decorationId=com.linkedin.sales.deco.desktop.search.DecoratedPeopleSearchHitResult-6"
        res = self._fetch(url)
        return self._parse_search_results(res.json()["elements"])

    def get_results_from_search(
        self,
        url,
        start_from = 0,
        count = 25
    ):
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        queries = ['doFetchHeroCard:false']
        if 'keywords' in query_params.keys():
            param = f"keywords:{query_params['keywords'][0]}"
            queries.append(param)

        if 'geoIncluded' in query_params.keys():
            geos = query_params['geoIncluded'][0].split(',')
            geo_ids = ",".join([f"(id:{geo})" for geo in geos])
            param = f"bingGeo:(includedValues:List({geo_ids}))"
            queries.append(param)

        if 'relationship' in query_params.keys():
            relationship = query_params['relationship'][0]
            param = f"relationship:List({relationship})"
            queries.append(param)

        if 'companyIncluded' in query_params.keys():
            companies = query_params['companyIncluded'][0].split(',')
            company_queries = []
            for company in companies:
                if ':' in company:
                    company_name, company_id = company.split(':')
                    company_queries.append(f'(text:{company_name},id:{company_id})')
                else:
                    company_queries.append(f'(text:{company})')

            time_scope = query_params['companyTimeScope'][0]
            param = f"companyV2:(scope:{time_scope},includedValues:List({','.join(company_queries)}))"
            queries.append(param)

        if 'industryIncluded' in query_params.keys():
            industies = query_params['industryIncluded'][0].split(',')
            industies_query = [f"(id:{ind})" for ind in industies]
            param = f"industryV2:(includedValues:List({','.join(industies_query)}))"
            queries.append(param)

        if 'companySize' in query_params.keys():
            company_size = query_params['companySize'][0]
            param = f'companySize:List({company_size})'
            queries.append(param)

        if 'seniorityIncluded' in query_params.keys():
            senorities = query_params['seniorityIncluded'][0].split(',')
            senorities_query = [f'(id:{s})' for s in senorities]
            param = f"seniorityLevelV2:(includedValues:List({','.join(senorities_query)}))"
            queries.append(param)

        if 'functionIncluded' in query_params.keys():
            functions = query_params['functionIncluded'][0].split(',')
            functions_query = [f'(id:{s})' for s in functions]
            param = f"functionV2:(includedValues:List({','.join(functions_query)}))"
            queries.append(param)

        if 'titleIncluded' in query_params.keys():
            titles = query_params['titleIncluded'][0].split(',')
            title_quries = []
            for title in titles:
                if ':' in title:
                    title_name, title_id = title.split(':')
                    title_quries.append(f'(text:{title_name},id:{title_id})')
                else:
                    title_quries.append(f'(text:{title})')

            time_scope = query_params['titleTimeScope'][0]
            param = f"titleV2:(scope:{time_scope},includedValues:List({','.join(title_quries)}))"
            queries.append(param)

        if 'schoolIncluded' in query_params.keys():
            schools = query_params['schoolIncluded'][0].split(',')
            school_queries = [f'(id:{s})' for s in schools]
            param = f"schoolV2:(includedValues:List({','.join(school_queries)}))"
            queries.append(param)

        # stock parameters
        queries.append("spellCorrectionEnabled:true,spotlightParam:(selectedType:ALL),doFetchFilters:true,doFetchHits:true,doFetchSpotlights:true")
        sales_nav_api_url = f"https://www.linkedin.com/sales-api/salesApiPeopleSearch?q=peopleSearchQuery&start={start_from}&count={count}&query=({','.join(queries)})&decorationId=com.linkedin.sales.deco.desktop.search.DecoratedPeopleSearchHitResult-6"
        res = self._fetch(sales_nav_api_url)
        return self._parse_search_results(res.json()["elements"])

    def convert_to_public_url(self, url):
        resp = requests.post(
            "https://nehi58zyck.execute-api.us-west-2.amazonaws.com/test/sales-nav-api/public-url",
            json = {
                "sales_nav_link": url,
                "li_at": self.client.li_at_cookies,
                "li_a": self.client.li_a_cookies,
            }
        )
        public_url = json.loads(resp.json()['body'])['publicUrl']
        return public_url

    def get_company_info(self, company_url):
        company_id = company_url.split("/")[5]
        build_query = f"(entityUrn,name,description,industry,employeeCount,employeeDisplayCount,employeeCountRange,location,headquarters,website,revenue,formattedRevenue,flagshipCompanyUrl)"
        # build_query = f"(entityUrn,name,account(saved,noteCount,listCount,crmStatus),pictureInfo,companyPictureDisplayImage,description,industry,employeeCount,employeeDisplayCount,employeeCountRange,location,headquarters,website,revenue,formattedRevenue,employeesSearchPageUrl,flagshipCompanyUrl,employees*~fs_salesProfile(entityUrn,firstName,lastName,fullName,pictureInfo,profilePictureDisplayImage))"

        build_query = quote(build_query)
        query_url = f"https://www.linkedin.com/sales-api/salesApiCompanies/{company_id}?decoration=" + build_query

        res = self._fetch(query_url)
        data = res.json()

        return {
            'name': safe_get(data, 'name'),
            'description': safe_get(data, 'description'),
            'website': safe_get(data, 'website'),
            'industry': safe_get(data, 'industry'),
            'employeeCount': safe_get(data, 'employeeCount'),
            'location': safe_get(data, 'location'),
        }