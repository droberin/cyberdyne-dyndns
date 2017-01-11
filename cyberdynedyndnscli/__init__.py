import time
import datetime
import requests


class CyberdyneDynDns():
    debug = False
    hostname = None
    username = None
    password = None
    server_address = "https://cyberdyne.es/dyndns/update"
    last_update = 0
    update_delay = 299

    def __init__(self, hostname=None, username=None, password=None, server_address=None):
        if hostname:
            self.hostname = hostname
        if username:
            self.username = username
        if password:
            self.password = password
        if server_address:
            self.server_address = server_address

    def request_update(self):
        if self.last_update is not 0 or (time.time() - self.last_update) <= self.update_delay:
            print("No way, Jose..., Last known request was at {}".format(
                datetime.datetime.fromtimestamp(int(self.last_update)).strftime('%Y-%m-%d %H:%M:%S'))
            )
            return False
        print("last successful known update happened long ago, requesting update")

        headers = {'X-API-TOKEN': 'your_token_here'}
        payload = "'hostname'='{}'&'username'='{}'".format(self.hostname, self.username)

        return self.__requester(payload=payload, headers=headers)

    def set(self, instance, value=None):
        if hasattr(self, instance) and self.is_editable_value(type(self.__getattribute__(instance))):
            self.__setattr__(instance, value)
            if instance is "password":
                value = "****"
            print("Variable {} set to {}".format(instance, value))
        else:
            print("Variable {} not found".format(instance))

    def test_attr(self):
        pass

    def __requester(self, payload, headers):
        response = None
        try:
            response = requests.post(self.server_address, data=payload, headers=headers, timeout=10)
        except requests.exceptions.ConnectionError as e:
            print("ERROR: [{}] Connection error: '{}'".format(self.hostname, e.__cause__))
            return False
        except TimeoutError:
            print("ERROR: Connection timeout")
            return False
        finally:
            if response is not None:
                print("Response:\n{}".format(response.text))
                self.last_update = time.time()
                return True
            else:
                return False

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
