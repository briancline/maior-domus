#!/usr/bin/env python
from provider import gandi
import yaml


if __name__ == '__main__':
    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file.read())

    api_key = (config.get('test_key') if config.get('test') is True
               else config.get('prod_key'))
    api = gandi.GandiClient(api_key, test_env=config.get('test'))

    domains = api.domain.list()
    domains = sorted(domains, key=lambda d: d.get('fqdn'))
    for domain in domains:
        print('%d: %s' % (domain.get('id'),
                          domain.get('fqdn')))

    domain = api.domain.info('example.com')
    print(domain)

    tlds = api.domain.tld.list()
    live_tlds = filter(gandi.is_tld_live, tlds)
    for tld in live_tlds:
        print('- .%s' % tld.get('name'))

    print('%d total tlds, %d are golive' % (len(tlds), len(live_tlds)))
