import json
import os
import sys
from sales_nav_api.sales import SalesNavigator

li_a  = "AQJ2PTEmc2FsZXNfY2lkPTkyMDc2MjQxJTNBJTNBOTE5NzM3NjklM0ElM0F0aWVyMSUzQSUzQTgyNTI0MjY1PPvqyOcWDrPJTLK1jad0J2kokls"
li_at = "AQEFALsBAAAAAARgz-8AAAF2H9bf0gAAAXZD-o1ETQAAXnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjgyNTI0MjY1LDEwOTc3NTYzNiledXJuOmxpOm1lbWJlcjoyMzA1NDE1OTF1Blc5Hx0ZBts1X2Cx4dXOPFDWC2cVFY9DByf7QFBolKCold5BayHgutnDIrHhM1bCZqqB3l3Q-quAfzRQDWHKkkZsEAP5wpnlAfo6724N1hZpwcYimLwcySy5pl8PJikhjD-y-xP4F1OY6tHBdA9z_fzVx7kvmxkTUagTaeXKQb9NZ9NQXp45SDXZA9R0Cj7VDg7w"

sales_nav = SalesNavigator(li_at, li_a)

url = 'https://www.linkedin.com/sales/search/people?companyExcluded=Workato%3A3675685&companyTimeScope=CURRENT&doFetchHeroCard=false&keywords=Workato%20AND%20Python&logHistory=true&page=1&rsLogId=709962092&searchSessionId=JdxjIvR7Ta2usLYs68XiqQ%3D%3D&titleExcluded=Partner%3A18%2CConsultant%3A3&titleTimeScope=CURRENT'
data = sales_nav.get_results_from_search(url, start_from=0, count=100)
print(data)