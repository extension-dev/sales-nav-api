import json
import os
import sys
from sales_nav_api.sales import SalesNavigator

li_a  = "AQJ2PTEmc2FsZXNfY2lkPTkyMDc2MjQxJTNBJTNBOTE5NzM3NjklM0ElM0F0aWVyMSUzQSUzQTgyNTI0MjY1PPvqyOcWDrPJTLK1jad0J2kokls"
li_at = "AQEFALsBAAAAAARgz-8AAAF2H9bf0gAAAXZD-o1ETQAAXnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjgyNTI0MjY1LDEwOTc3NTYzNiledXJuOmxpOm1lbWJlcjoyMzA1NDE1OTF1Blc5Hx0ZBts1X2Cx4dXOPFDWC2cVFY9DByf7QFBolKCold5BayHgutnDIrHhM1bCZqqB3l3Q-quAfzRQDWHKkkZsEAP5wpnlAfo6724N1hZpwcYimLwcySy5pl8PJikhjD-y-xP4F1OY6tHBdA9z_fzVx7kvmxkTUagTaeXKQb9NZ9NQXp45SDXZA9R0Cj7VDg7w"

sales_nav = SalesNavigator(li_at, li_a)

def test_1():	
	url = 'https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&logHistory=true&page=1&rsLogId=715796908&schoolIncluded=150005&searchSessionId=S%2BLrlI%2BjT6CvZ35gnUoEWA%3D%3D&titleIncluded=sales%2520AND%2520Ops%2Csales%2520AND%2520Operations&titleTimeScope=CURRENT'
	data = sales_nav.get_results_from_search(url, start_from=0, count=100)
	print(len(data))

def test_2():
	# company = "https://www.linkedin.com/sales/company/2738049/people"
	# company = "https://www.linkedin.com/sales/company/1534"
	# company = "https://www.linkedin.com/sales/company/2382910/people"
	company = "https://www.linkedin.com/sales/company/1028"
	company_data = sales_nav.get_company_info(company)
	print(json.dumps(company_data))


# test_1()
test_2()