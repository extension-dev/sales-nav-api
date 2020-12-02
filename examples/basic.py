import json
from linkedin_api import Linkedin

credentials = {
	"username": "zihua@include.ai",
	"password": "James19961025"
}

if credentials:
    linkedin = Linkedin(credentials["username"], credentials["password"])

    profile = linkedin.get_profile("ACoAABQ11fIBQLGQbB1V1XPBZJsRwfK5r1U2Rzw")
    profile["contact_info"] = linkedin.get_profile_contact_info(
        "ACoAABQ11fIBQLGQbB1V1XPBZJsRwfK5r1U2Rzw"
    )
    connections = linkedin.get_profile_connections(profile["profile_id"])
