import urllib.parse as urlparse
from urllib.parse import parse_qs
url = 'https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&keywords=sales%20operations&logHistory=true&page=1&rsLogId=701774412&searchSessionId=BWqJov50RnW69NIm29cHKw%3D%3D&titleIncluded=genshin%2520impact%2CSales%2520Assistant%3A237&titleTimeScope=CURRENT'
parsed = urlparse.urlparse(url)
print(parse_qs(parsed.query))