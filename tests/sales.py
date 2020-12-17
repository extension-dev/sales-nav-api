import json
import os
import sys
from sales_nav_api.sales import SalesNavigator

li_a  = "AQJ2PTEmc2FsZXNfY2lkPTkyMDc2MjQxJTNBJTNBOTE5NzM3NjklM0ElM0F0aWVyMSUzQSUzQTgyNTI0MjY1PPvqyOcWDrPJTLK1jad0J2kokls"
li_at = "AQEFALsBAAAAAARgz-8AAAF2H9bf0gAAAXZD-o1ETQAAXnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjgyNTI0MjY1LDEwOTc3NTYzNiledXJuOmxpOm1lbWJlcjoyMzA1NDE1OTF1Blc5Hx0ZBts1X2Cx4dXOPFDWC2cVFY9DByf7QFBolKCold5BayHgutnDIrHhM1bCZqqB3l3Q-quAfzRQDWHKkkZsEAP5wpnlAfo6724N1hZpwcYimLwcySy5pl8PJikhjD-y-xP4F1OY6tHBdA9z_fzVx7kvmxkTUagTaeXKQb9NZ9NQXp45SDXZA9R0Cj7VDg7w"

sales_nav = SalesNavigator(li_at, li_a)

def test_1():	
	url = "https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&geoIncluded=103644278&keywords=%22Python%22%20AND%20%22internal%22%20AND%20(%22API%22%20OR%20%22APIs%22)&logHistory=true&page=1&rsLogId=596836466&searchSessionId=p09MZH2LQnmpJVE39Fvs7Q%3D%3D&titleIncluded=%2522Operations%2520Engineer%2522%2C%2522Business%2520Applications%2522%2C%2522Business%2520Apps%2522%2C%2522Business%2520Application%2522%2C%2522Operations%2520Engineering%2522&titleTimeScope=CURRENT"
	# url = "https://www.linkedin.com/sales/search/people?doFetchHeroCard=true&geoIncluded=103644278&logHistory=true&page=1&rsLogId=721659788&searchSessionId=p09MZH2LQnmpJVE39Fvs7Q%3D%3D&titleIncluded=%2522Operations%2520Engineer%2522%2C%2522Business%2520Applications%2522%2C%2522Business%2520Apps%2522%2C%2522Business%2520Application%2522%2C%2522Operations%2520Engineering%2522&titleTimeScope=CURRENT"
	data = sales_nav.get_results_from_search(url, start_from=0, count=100)
	print(len(data))
	print(data[0])

def test_2():
	# company = "https://www.linkedin.com/sales/company/2738049/people"
	# company = "https://www.linkedin.com/sales/company/1534"
	# company = "https://www.linkedin.com/sales/company/2382910/people"
	company = "https://www.linkedin.com/sales/company/1028"
	company_data = sales_nav.get_company_info(company)
	print(json.dumps(company_data))

def test_3():
	li_a = "AQJ2PTEmc2FsZXNfY2lkPTkwNzE4NTIxJTNBJTNBOTA2ODQ2NDElM0ElM0F0aWVyMSUzQSUzQTgxMzAzNzg1_8whE4VYZvg7ggBBme9PqWZPXJc"
	li_at = "AQEFALsBAAAAAAQtsO4AAAF1euA-3wAAAXaH57h_TQAAXnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjgxMzAzNzg1LDEwOTUwODk3MyledXJuOmxpOm1lbWJlcjoxODUxMjY4MTGV8icO6lnw9p4N59Sgiix60_VUV_8qXL0CzANBpzMbEr_ZPJa8T_Se1XqUVkmQhLpSRHHhtUOiNLmzBYhoCceVvy_0uJ7xx2EsYq_fiSF3ErOYVZACHXswu65vE4qXjMPLYovJLvv01RxAnb-tTCY8uijnAyHiyYXfasqJNC7gy0XcSY_RGFJlEHNcY7xeNlJuBKse"

	sales_nav = SalesNavigator(li_at, li_a)
	connection_url = "https://www.linkedin.com/sales/people/ACwAAAJSSUkBtgOlx53grhX6606ILuOMuEEULZ0,NAME_SEARCH,049O"
	company = "Zava"
	people = sales_nav.get_connections_to_person(connection_url, company, 0, 25)

test_1()
# test_2()
# test_3()