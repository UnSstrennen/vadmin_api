from requests import session as requests_session
from grequests import request as async_request
from time import sleep
import warnings


token_type = ''
access_token = ''
headers = {
    'X-API-VERSION': '1.0',
    'content-type': 'application/json'
}


vadmin_api_session = requests_session()
vadmin_api_session.hooks = {
    'response': lambda r, *args, **kwargs: r.raise_for_status()
}


class BrokenPlanError(Exception):
    """ Error occures in case if user is trying to start the broken plan """


class VAdminAPI:
    def __init__(self, new_vadmin_api_host, database_id):
        self.host = new_vadmin_api_host
        self.database_id = database_id

    def get_token(self, username, password):
        """
        Returns token by username&password given.
        Sets token_type and access_token attributes.
        Adds Authorization header.
        """
        url = self.host + "/idsrv/connect/token"
        payload = "grant_type=password&scope=openid profile email roles viqubeadmin_api viqube_api&response_type=id_token token&username={}&password={}".format(username, password)
        cur_headers = {
            'content-type': "application/x-www-form-urlencoded",
            'authorization': "Basic dmlxdWJlYWRtaW5fcm9fY2xpZW50OjcmZEo1UldwVVMkLUVVQE1reHU="
            }
        res = vadmin_api_session.request("POST", url, data=payload, headers=cur_headers)
        token_type = res.json()['token_type']
        access_token = res.json()['access_token']
        headers['Authorization'] = '{} {}'.format(token_type, access_token)
        return access_token

    def auth_by_username(self, username, password):
        """ auths user by username&password """
        self.get_token(username, password)

    def auth_by_token(self, new_token_type, new_access_token):
        """ auths user by token type and token """
        token_type = new_token_type
        access_token = new_access_token
        headers['Authorization'] = '{} {}'.format(token_type, access_token)

    def get_load_plans(self, with_status=False):
        """ returns list of LoadPlan objects """
        if with_status:
            url = self.host + '/vqadmin/api/databases/{}/loadplans/all/status'.format(self.database_id)
        else:
            url = self.host + '/vqadmin/api/databases/{}/loadplans'.format(self.database_id)
        res = vadmin_api_session.request('GET', url, headers=headers)
        return [LoadPlan(**plan, database_id=self.database_id, host=self.host) for plan in res.json()]

    def get_load_plan_by_id(self, id):
        """ returns LoadPlan object by given id """
        res = vadmin_api_session.request('GET', self.host + '/vqadmin/api/databases/{}/loadplans/{}'.format(self.database_id, id), headers=headers)
        return LoadPlan(**res.json(), database_id=self.database_id, host=self.host)

    def get_load_plan_by_name(self, name):
        """ returns LoadPlan object by given name """
        plans = self.get_load_plans()
        for plan in plans:
            if plan.name == name:
                return plan
        raise ValueError("Plan called {} doesn't exist")


class LoadPlan:
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
        if not hasattr(self, 'status'):
            self.get_status()

    def __repr__(self):
        return '<LoadPlan {} ({})>'.format(self.name, self.id)

    def get_steps(self):
        """ update object steps attribute, returns list of steps """
        res = vadmin_api_session.request('GET', self.host + '/vqadmin/api/databases/{}/loadplans/{}/steps'.format(self.database_id, self.id), headers=headers)
        self.steps = res.json()
        return res.json()

    def get_status(self):
        """ updates object status attribute, returns status as-is """
        res = vadmin_api_session.request('GET', self.host + '/vqadmin/api/databases/{}/loadplans/{}/status'.format(self.database_id, self.id), headers=headers)
        self.status = res.json()
        if res.json()['error']:
            warnings.warn('LoadPlan with id {} is broken.'.format(self.id), ResourceWarning)
        return res.json()['status']

    def get_progress(self):
        """ updates object status attribute, returns status as-is """
        res = vadmin_api_session.request('GET', self.host + '/vqadmin/api/databases/{}/loadplans/{}/status'.format(self.database_id, self.id), headers=headers)
        self.status = res.json()
        return res.json()['progress']

    def execute(self, with_prints=True):
        """ starts load plan and waits the response. """
        if self.status['error']:
            raise BrokenPlanError('The plan is broken or contains errors.')
        res = vadmin_api_session.request('POST', self.host + '/vqadmin/api/databases/{}/loadplans/{}/start'.format(self.database_id, self.id), headers=headers)
        while True:
            res = self.get_status()
            if res != 'Running':
                break
            else:
                if with_prints:
                    print('Load progress:', self.get_progress())
                sleep(1)

    def start(self):
        """ starts load plan without waiting for response """
        if self.status['error']:
            raise BrokenPlanError('The plan is broken or contains errors.')
        async_request('POST', self.host + '/vqadmin/api/databases/{}/loadplans/{}/start'.format(self.database_id, self.id), headers=headers)

    def stop(self):
        """ stops load plan """
        res = vadmin_api_session.request('POST', self.host + '/vqadmin/api/databases/{}/loadplans/{}/stop'.format(self.database_id, self.id), headers=headers)
