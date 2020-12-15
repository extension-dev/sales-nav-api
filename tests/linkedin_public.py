import json
import os
import sys
from sales_nav_api.linkedin import LinkedIn

li_at = "AQEFALsBAAAAAARgz-8AAAF2H9bf0gAAAXZD-o1ETQAAXnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjgyNTI0MjY1LDEwOTc3NTYzNiledXJuOmxpOm1lbWJlcjoyMzA1NDE1OTF1Blc5Hx0ZBts1X2Cx4dXOPFDWC2cVFY9DByf7QFBolKCold5BayHgutnDIrHhM1bCZqqB3l3Q-quAfzRQDWHKkkZsEAP5wpnlAfo6724N1hZpwcYimLwcySy5pl8PJikhjD-y-xP4F1OY6tHBdA9z_fzVx7kvmxkTUagTaeXKQb9NZ9NQXp45SDXZA9R0Cj7VDg7w"
client = LinkedIn(li_at)

def test_1():
	url = 'https://www.linkedin.com/in/dan-riccio-16092210/'
	profile = client.get_profile_data(url)
	print(profile)

def test_2():
	url = 'https://www.linkedin.com/in/liyau/'
	profile = client.get_profile_data(url)
	tracking_id = profile['tracking_id']
	person_urn = profile['person_urn']
	client.send_invitation(person_urn, tracking_id, ' Hi Yau, would love to connect!')

test_1()
