"""
Examples how to use Peekdata DataGateway API
"""

from Peekdata.DataGatewayAPI.Model import *
import requests
import os

__author__ = 'Vaidotas Senkus'
__email__ = 'vaidas100@gmail.com'


class ApiClient:

    CONST_API_METHOD_HEALTHCHECK = "/datagateway/v1/healthcheck"
    CONST_API_METHOD_GETSELECT = "/datagateway/v1/select"
    CONST_API_METHOD_GETDATA = "/datagateway/v1/select/data"
    CONST_API_METHOD_GETCSV = "/datagateway/v1/select/file"

    def __init__(self, url: str, port: int, scheme: str):
        """
        default constructor
        """
        self.BaseAddress = "{scheme}://{url}:{port}".format(
            url=url,
            port=port,
            scheme=scheme,
        )

    def healthCheck(self):
        """
        method to check service availability
        """
        try:
            r = requests.get(
                "{}{}".format(
                    self.BaseAddress,
                    self.CONST_API_METHOD_HEALTHCHECK
                ),
                headers={'Content-type': 'application/json'},
            )
            r.raise_for_status()
            return r.ok
        except requests.exceptions.RequestException as e:
            print("ERROR:\n  ", e)
        exit(1)

    def getSelect(self, request):
        """
        method to get SELECT statement
        """
        json_request = serialize_to_json(request)
        try:
            r = requests.post(
                "{}{}".format(
                    self.BaseAddress,
                    self.CONST_API_METHOD_GETSELECT
                ),
                headers={'Content-type': 'application/json'},
                data=json_request,
            )
            r.raise_for_status()
            result = r.text.rstrip()
            return result
        except requests.exceptions.RequestException as e:
            print("ERROR:\n  ", e)
        exit(1)

    def getData(self, request):
        """
        method to get DATA
        """
        json_request = serialize_to_json(request)
        try:
            r = requests.post(
                "{}{}".format(
                    self.BaseAddress,
                    self.CONST_API_METHOD_GETDATA
                ),
                headers={'Content-type': 'application/json'},
                data=json_request,
            )
            r.raise_for_status()
            result = json.dumps(
                json.loads(r.text),
                sort_keys=True,
                indent=4
            )
            return result
        except requests.exceptions.RequestException as e:
            print("ERROR:\n  ", e)
        exit(1)

    def GetCSV(self, request, filename):
        """
        method to get CSV file
        """
        json_request = serialize_to_json(request)
        try:
            r = requests.post(
                "{}{}".format(
                    self.BaseAddress,
                    self.CONST_API_METHOD_GETCSV
                ),
                headers={'Content-type': 'application/json'},
                data=json_request,
            )
            r.raise_for_status()
            if os.path.isfile(filename):
                os.unlink(filename)
            with open(filename, 'w') as f:
                f.write(r.text)
            return True
        except requests.exceptions.RequestException as e:
            print("ERROR:\n  ", e)
        exit(1)
