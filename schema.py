base = ['zimbra-core', 'zimbra-snmp']
ldap = list(set(base + ['zimbra-ldap']))
mailbox = list(set(base + ['zimbra-store','zimbra-apache', 'zimbra-spell']))
logger = list(set(base + ['zimbra-logger']))
mta = list(set(base + ['zimbra-mta', 'zimbra-dnscache']))
proxy = list(set(base + ['zimbra-proxy', 'zimbra-memcached']))

single_server = list(set(ldap + mailbox + logger + mta + proxy))