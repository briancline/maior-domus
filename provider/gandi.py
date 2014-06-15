import xmlrpclib


def is_tld_live(tld):
    return (tld.get('phase') == 'golive')


class GandiClient(xmlrpclib.ServerProxy):

    TestURL = 'https://rpc.ote.gandi.net/xmlrpc/'
    ProdURL = 'https://rpc.gandi.net/xmlrpc/'

    def __init__(self, api_key, test_env=False):
        self._api_key = api_key

        xmlrpclib.ServerProxy.__init__(self,
                                       GandiClient.TestURL if test_env else
                                       GandiClient.ProdURL)

    def __getattr__(self, name):
        return xmlrpclib._Method(self.__keyed_request, name)

    def __keyed_request(self, method_name, params):
        params = (self._api_key,) + params
        return xmlrpclib.ServerProxy.__getattr__(self, method_name)(*params)
