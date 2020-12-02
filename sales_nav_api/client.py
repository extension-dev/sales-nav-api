import requests
from bs4 import BeautifulSoup
import json

class Client(object):
    """
    Class to act as a client for the Linkedin API.
    """

    # Settings for general Linkedin API calls
    LINKEDIN_BASE_URL = "https://www.linkedin.com"
    REQUEST_HEADERS = {
        "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        # "accept": "application/vnd.linkedin.normalized+json+2.1",
        "accept-language": "en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "x-li-lang": "en_US",
        "x-restli-protocol-version": "2.0.0",
        # "x-li-track": '{"clientVersion":"1.2.6216","osName":"web","timezoneOffset":10,"deviceFormFactor":"DESKTOP","mpName":"voyager-web"}',
    }

    # Settings for authenticating with Linkedin
    AUTH_REQUEST_HEADERS = {
        "X-Li-User-Agent": "LIAuthLibrary:3.2.4 \
                            com.linkedin.LinkedIn:8.8.1 \
                            iPhone:8.3",
        # "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        "User-Agent": "LinkedIn/8.8.1 CFNetwork/711.3.18 Darwin/14.0.0",
        "X-User-Language": "en",
        "X-User-Locale": "en_US",
        "Accept-Language": "en-us",
    }

    # base linkedin api url
    API_BASE_URL = f"{LINKEDIN_BASE_URL}/voyager/api"

    def __init__(self, li_at, li_a):
        self.session = requests.session()
        self.session.headers.update(Client.REQUEST_HEADERS)
        self.metadata = {}
        self.li_at_cookies = li_at
        self.li_a_cookies = li_a

    def _add_li_cookies(self, li_at, li_a):
        li_at_cookie = requests.cookies.create_cookie(
            domain='.wwww.linkedin.com',
            name='li_at',
            value=li_at
        )
        li_a_cookie = requests.cookies.create_cookie(
            domain='.wwww.linkedin.com',
            name='li_a',
            value=li_a
        )
        self.session.cookies.set_cookie(li_at_cookie)
        self.session.cookies.set_cookie(li_a_cookie)

    def _request_session_cookies(self):
        """
        Return a new set of session cookies as given by Linkedin.
        """
        res = requests.get(
            f"{Client.LINKEDIN_BASE_URL}/uas/authenticate",
            headers=Client.AUTH_REQUEST_HEADERS,
        )
        return res.cookies

    def _set_session_cookies(self, cookies):
        """
        Set cookies of the current session and save them to a file named as the username.
        """
        self.session.cookies = cookies
        Client.REQUEST_HEADERS["csrf-token"] = self.session.cookies["JSESSIONID"].strip(
            '"'
        )

    def _fetch_metadata(self):
        """
        Get metadata about the "instance" of the LinkedIn application for the signed in user.

        Store this data in self.metadata
        somehow this does not work in the lambda
        """
        res = self.fetch(Client.LINKEDIN_BASE_URL)
        
        soup = BeautifulSoup(res.text, "lxml")

        clientApplicationInstanceRaw = soup.find(
            "meta", attrs={"name": "applicationInstance"}
        ).attrs["content"]
        clientApplicationInstance = json.loads(clientApplicationInstanceRaw)

        clientPageInstanceId = soup.find(
            "meta", attrs={"name": "clientPageInstanceId"}
        ).attrs["content"]

        self.metadata["clientApplicationInstance"] = clientApplicationInstance
        self.metadata["clientPageInstanceId"] = clientPageInstanceId

    @property
    def cookies(self):
        return self.session.cookies

    def initiate(self): 
        session_cookies = self._request_session_cookies()
        self._set_session_cookies(session_cookies)
        self._add_li_cookies(self.li_at_cookies, self.li_a_cookies)
        # self._fetch_metadata()

    def fetch(self, url):
        cookieString = ";".join([f"{c.name}={c.value}" for c in self.session.cookies])
        Client.REQUEST_HEADERS.update({
            "Cookie": cookieString,
        })
        return requests.get(url, headers=Client.REQUEST_HEADERS)


    def post(self, url):
        cookieString = ";".join([f"{c.name}={c.value}" for c in self.session.cookies])
        Client.REQUEST_HEADERS.update({
            "Cookie": cookieString,
        })
        return requests.post(url, headers=Client.REQUEST_HEADERS)
