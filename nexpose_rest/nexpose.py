import requests, base64, json


class Configuration:
    def __init__(self, host, username, password, ssl_verify=True):
        self.host = host
        self.username = username
        self.password = password
        self.ssl_verify = ssl_verify
        self.auth_data = base64.b64encode(self.username + ":" + self.password)


class MalformedResponseError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)


class InternalServerError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)


class ServiceUnavailableError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)


def _GET(url, config, page=1, size=100):
    args = '?page=' + str(page - 1) + '&size=' + str(size)
    r = requests.get(config.host + url + args, headers={"Authorization": "Basic %s" % config.auth_data})
    try:
        if r.status_code == 500:
            raise InternalServerError("The server responded with an ERROR Code 500!")
        elif r.status_code == 503:
            raise ServiceUnavailableError("The requested service is not available!")
        res = r.json()
        if "page" in res and "resources" in res and res['page']['totalPages'] > page:
            nested_c, nested_j = _GET(url, config, page=page + 1)
            res['resources'] = res['resources'] + nested_j
        if 'resources' in res:
            return r.status_code, res['resources']
        else:
            return r.status_code, res
    except ValueError as e:
        return -1, MalformedResponseError("Unable to parse Response")


def testConnection(config):
    code, data = _GET('/api/3', config)
    return code == 200


def getAssetGroup(config, id):
    code, data = _GET('/api/3/asset_groups/' + str(id), config)
    return data


def getAssetGroupAssets(config, id):
    code, data = _GET('/api/3/asset_groups/' + str(id) + "/assets", config)
    return data


def getAssetGroups(config):
    code, data = _GET('/api/3/asset_groups', config)
    return data


def getAssets(config):
    code, data = _GET('/api/3/assets', config)
    return data


def getAsset(config, id):
    code, data = _GET('/api/3/assets/' + str(id), config)
    return data


def getAssetVulnerabilities(config, id):
    code, data = _GET('/api/3/assets/' + str(id) + "/vulnerabilities", config)
    return data


def getSites(config):
    code, data = _GET('/api/3/sites', config)
    return data


def getSite(config, id):
    code, data = _GET('/api/3/sites/' + str(id), config)
    return data
