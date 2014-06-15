#!/usr/bin/env python
import xmlrpclib
import yaml


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


if __name__ == '__main__':
    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file.read())

    api_key = (config.get('test_key') if config.get('test') is True
               else config.get('prod_key'))
    gandi = GandiClient(api_key, test_env=config.get('test'))

    domains = gandi.domain.list()
    domains = sorted(domains, key=lambda d: d.get('fqdn'))
    for domain in domains:
        print('%d: %s' % (domain.get('id'),
                          domain.get('fqdn')))

    domain = gandi.domain.info('example.com')
    import pprint
    pprint.pprint(domain)

    tlds = gandi.domain.tld.list()
    live_tlds = filter(is_tld_live, tlds)
    for tld in live_tlds:
        print('- .%s' % tld.get('name'))

    print('%d total tlds, %d are golive' % (len(tlds), len(live_tlds)))
