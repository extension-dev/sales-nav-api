# LinkedIn Sales Navigator API

The sales_nav_api is a reverse engineered API for LinkedIn and LinkedIn Sales Navigator.

## How To Use

Go to the `tests` directory and copy `linkedin_public.py` and `sales.py`. [Replace the li_a and li_at cookies with yours](https://github.com/austinoboyle/scrape-linkedin-selenium/issues/7)

There are two test functions in `linkedin_public.py` 
  - in the first test `client.get_profile_data(url)` grabs the profile information for a given LinkedIn profile
  - the second test sends a LinkedIn connection invite using `client.send_invitation(person_urn, tracking_id, ' Hi Yau, would love to connect!')`
  
In `sales.py`
  - in the first test `sales_nav.get_results_from_search(url, start_from=0, count=100)` grabs the first 100 search results for a Sales Navigator search
  - the second test gets the information of a company with `sales_nav.get_company_info(company)`
  - the third test sends a connection request with `sales_nav.get_connections_to_person(connection_url, company, 0, 25)`
  
 
