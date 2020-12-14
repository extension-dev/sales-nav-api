def get_id_from_urn(urn):
    """
    Return the ID of a given Linkedin URN.

    Example: urn:li:fs_miniProfile:<id>
    """
    return urn.split(":")[3]

def safe_get(obj, key):
	if key in obj.keys():
		return obj[key]
	else:
		return ""