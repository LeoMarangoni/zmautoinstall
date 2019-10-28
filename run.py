import random
import sys
import string
from servers import servers
from config import (
    domain,
    ldap_host,
    logger_host,
    smtp_host,
    ldap_password,
    admin_password,
    admin_account
)


def randomString(stringLength=10):
    letters = string.ascii_letters + string.digits + "_+=-@"
    return ''.join(random.choice(letters) for i in range(stringLength))


def getService(servers, service):
    for server in servers:
        pkgs = servers[server]['schema']
        if service in pkgs:
            print("Found %s as %s host") % (server, service)
            return server
        else:
            pass
    print("%s server not found in configuration") % (service)
    sys.exit(1)


def genEtcHosts(servers, domain):
    f = open("files/etchosts.tmp", "w+")
    f.write("127.0.0.1\tlocalhost\r\n")
    for server in sorted(servers):
        ip = servers[server]['ip']
        f.write("%s\t%s.%s\t\t%s\n" % (ip, server, domain, server))
    f.close()


def dictToStdout(d):
    for v in d:
        print("%s=\"%s\"") %(v, d[v])


def dictToFile(d, path):
    f = open(path, "w+")
    for v in d:
        f.write("%s=\"%s\"\r\n" % (v, d[v]))
    f.close()
    

ldap_host = ldap_host or (getService(servers, 'zimbra-ldap') + "." + domain)
logger_host = logger_host or (getService(servers, 'zimbra-logger') + "." + domain)
smtp_host = smtp_host or (getService(servers, 'zimbra-mta') + "." + domain)
ldap_password = ldap_password or randomString()
admin_password = admin_password or randomString()
admin_account = (admin_account or 'admin') + "@" + domain

autoinstall = {
    'zimbra-core': {
        'LDAPHOST': ldap_host,
        'LDAPROOTPASS': ldap_password,
        'LDAPADMINPASS': ldap_password,
        'zimbraLogHostname': logger_host
    },
    'zimbra-ldap': {
        'LDAPAMAVISPASS': ldap_password,
        'LDAPPOSTPASS': ldap_password,
        'LDAPREPPASS': ldap_password,
        'LDAPNGINXPW': ldap_password
    },
    'zimbra-logger': {},
    'zimbra-mta': {
        'LDAPAMAVISPASS': ldap_password,
        'LDAPPOSTPASS': ldap_password
    },
    'zimbra-dnscache': {},
    'zimbra-snmp': {},
    'zimbra-store': {
        'SMTPHOST': smtp_host,
        'CREATEADMIN': admin_account,
        'CREATEADMINPASS': admin_password
    },
    'zimbra-apache': {},
    'zimbra-spell': {},
    'zimbra-convertd': {},
    'zimbra-memcached': {},
    'zimbra-proxy': {
        'PROXYMODE': 'redirect',
        'LDAPNGINXPW': ldap_password
    },

}

for server in servers:
    server_pkgs = servers[server]['schema']
    server_autoinstall = {
        'HOSTNAME': server + "." + domain,
        'INSTALL_PACKAGES': " ".join(server_pkgs)
    }
    for pkg in autoinstall:
        if pkg in server_pkgs:
            server_autoinstall.update(autoinstall[pkg])
    path = "files/autoinstall_" + server
    dictToFile(server_autoinstall, path)


genEtcHosts(servers, domain)
