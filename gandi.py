#!/usr/bin/env python
from provider import gandi
import yaml

def heading(title):
    print('\n%s %s' % (title, '=' * (73 - len(title))))

def subheading(title):
    print('[ %s ]%s' % (title, '-' * (70 - len(title))))

if __name__ == '__main__':
    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file.read())

    api_key = (config.get('test_key') if config.get('test') is True
               else config.get('prod_key'))
    api = gandi.GandiClient(api_key, test_env=config.get('test'))

    # List all domains on the account
    heading('ALL DOMAINS')
    domains = api.domain.list()
    domains = sorted(domains, key=lambda d: d.get('fqdn'))
    for domain in domains:
        print('%d: %s' % (domain.get('id'),
                          domain.get('fqdn')))

    # List all account contacts
    heading('ALL CONTACTS')
    contacts = api.contact.list()
    for contact in contacts:
        print('%s: %s %s (%s)' % (contact['handle'],
                                  contact['given'], contact['family'],
                                  contact['email']))

    # Get detailed domain information
    heading('DOMAIN DETAILS')
    domain = api.domain.info(domains[0]['fqdn'])

    subheading(domain.get('fqdn'))
    listables = ['contacts', 'nameservers', 'services', 'status', 'tags']
    for k, v in sorted(domain.iteritems()):
        if k == 'contacts':
            v = ['%s:%s' % (ck, cv['handle'] if cv else '-')
                            for ck, cv in v.iteritems()]

        if k in listables:
            v = ', '.join(v)

        print('  %-23s: %s' % (k, v))

    # Retrieve and list all available TLDs
    heading('FULL-ISH TLD LISTING')
    tlds = api.domain.tld.list()
    live_tlds = filter(gandi.is_tld_live, tlds)
    for tld in live_tlds:
        print('- .%s' % tld.get('name'))

    print('%d total tlds, %d are golive' % (len(tlds), len(live_tlds)))
