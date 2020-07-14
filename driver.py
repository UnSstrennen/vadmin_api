from requests import request


HOST = 'http://84.201.138.2'  # host to which requests will be made


class VAdminAPI:

    def __init__(self, *args):
        self.token_type = ''
        self.access_token = ''
        self.headers = {
            'X-API-VERSION': self.get_api_version(),
            'content-type': "application/json"
        }

    def get_api_version(self):
        # res = request("GET", HOST + '/viqube/version')
        # return res.json()['apiStable']
        return '1.0'

    def get_token(self, username, password):
        """
        Returns token by username&password given.
        Sets token_type and access_token attributes.
        Adds Authorization header.
        """
        url = HOST + "/idsrv/connect/token"
        payload = "grant_type=password&scope=openid profile email roles viqubeadmin_api viqube_api&response_type=id_token token&username={}&password={}".format(username, password)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'authorization': "Basic dmlxdWJlYWRtaW5fcm9fY2xpZW50OjcmZEo1UldwVVMkLUVVQE1reHU="
            }
        res = request("POST", url, data=payload, headers=headers)
        self.token_type = res.json()['token_type']
        self.access_token = res.json()['access_token']
        self.headers['Authorization'] = '{} {}'.format(self.token_type, self.access_token)
        return self.access_token

    def auth_by_username(self, username, password):
        """ auths user by username&password """
        self.get_token(username, password)

    def auth_by_token(self, token_type, access_token):
        """ auths user by token type and token """
        self.token_type = token_type
        self.access_token = access_token
        self.headers['Authorization'] = '{} {}'.format(self.token_type, self.access_token)

    def get_load_plans(self, database_id):
        res = request('GET', HOST + '/vqadmin/api/databases/{}/loadplans'.format(database_id), headers=self.headers)
        return [LoadPlan(plan) for plan in res.json()]

    def get_load_plan(self, database_id, load_plan_id):
        res = request('GET', HOST + '/vqadmin/api/databases/{}/loadplans/{}'.format(database_id, load_plan_id), headers=self.headers)
        return LoadPlan(res.json())


class LoadPlan:
    def __init__(self, dict_repr):
        for key in dict_repr.keys():
            setattr(self, key, dict_repr[key])

    def __repr__(self):
        return '<LoadPlan {} ({})>'.format(self.name, self.id)
