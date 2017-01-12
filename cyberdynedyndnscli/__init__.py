import time
import datetime
import requests


class CyberdyneDynDns():
    debug = False
    hostname = None
    username = None
    password = None
    last_known_external_ip_address = None
    # server_address = "https://cyberdyne.es/dyndns/update"
    server_address = "http://api.cyberdyne.es/update/dyndns"
    get_my_external_ip_request_url = "http://api.cyberdyne.es/get_my_ip"
    last_update = 0
    update_delay = 299

    def __init__(self, hostname=None, username=None, password=None, server_address=None, debug=False):
        if hostname:
            self.hostname = hostname
        if username:
            self.username = username
        if password:
            self.password = password
        if server_address:
            self.server_address = server_address
        if debug:
            self.debug = debug

    def get_my_external_ip(self):
        data = self.__requester(self.get_my_external_ip_request_url, method="get",
                                request_url=self.get_my_external_ip_request_url)
        if data:
            if data['status'] is True and data['status_code'] is 200:
                self.last_known_external_ip_address = data['text']
                return self.last_known_external_ip_address
        return None

    def request_update(self):
        if self.last_update is not 0 or (time.time() - self.last_update) <= self.update_delay:
            print("No way, Jose..., Last known request was at {}".format(
                datetime.datetime.fromtimestamp(int(self.last_update)).strftime('%Y-%m-%d %H:%M:%S'))
            )
            return False
        #print("last successful known update happened long ago, requesting update")

        if self.get_my_external_ip():
            headers = {'X-API-TOKEN': 'your_token_here'}
            payload = "'hostname'='{}'&'username'='{}'".format(self.hostname, self.username)
            requester_result = self.__requester(payload=payload, headers=headers)
            if self.debug:
                print("Requester result: {}".format(requester_result['text']))

            return requester_result['status']
        else:
            return "ERROR getting external IP address"

    def set(self, instance, value=None):
        if hasattr(self, instance) and self.is_editable_value(type(self.__getattribute__(instance))):
            self.__setattr__(instance, value)
            if instance is "password":
                value = "****"
            print("Variable {} set to {}".format(instance, value))
        else:
            print("Variable {} not found".format(instance))

    def __requester(self, payload=None, headers=None, method="post", request_url=server_address):
        response = requests.models.Response
        response_return = {
            "status_code": 0,
            "status": False,
            "text": None,
        }

        try:
            if method is "post":
                response = requests.post(request_url, data=payload, headers=headers, timeout=10)
            else:
                response = requests.get(request_url, timeout=10)
        except ConnectionError as e:
            print("ERROR: [{}] Connection error: '{}'".format(self.hostname, e.__cause__))
            return response_return
        except requests.exceptions.SSLError as e:
            print("ERROR: SSL error: {}".format(e.args[0]))
            return response_return
        except TimeoutError:
            print("ERROR: Connection timeout")
            response_return['status'] = False
            return response_return
        finally:
            if response.text and hasattr(response, "status_code"):
                response_return['status_code'] = response.status_code
                if response.status_code is 200:
                    response_return['status'] = True
                    response_return['text'] = response.text
                else:
                    response_return['status'] = False


            #print("Response:\n{}".format(response.text))
            #self.last_update = time.time()
            return response_return

    @classmethod
    def is_editable_value(cls, value):
        if cls.debug:
            print("valor: {}".format(value))
        return {
                str: True,
                int: True,
                float: True,
                list: True,
                dict: True,
            }.get(value, False)    # False is default if type value not found
