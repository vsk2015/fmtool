"""

This module contains the primitives to access host information.

"""
from fmcheck.utils import check_mandatory_values


class Host(object):

    def __init__(self, props, expected=False):
        check_mandatory_values(props, ['name', 'ip'])
        self.props = props
        self.expected = expected
        self.ip = props['ip'].split(
            '/')[0] if '/' in props['ip'] else props['ip']
        self.mask = props['ip'].split(
            '/')[1] if '/' in props['ip'] else '24'
        self.hosts_ip ={} 
        self.hosts_ip[props['name']] = props['ip'].split('/')[0]
        self.type = 'mininet' if not props.get('type') else props['type']
        self.user = 'vagrant' if not props.get('user') else props['user']
        self.password = 'vagrant' if not props.get(
            'password') else props['password']
        self.port = 22 if not props.get('port') else props['port']
        self.mac = None if not props.get('mac') else props['mac']
        self.name = props['name']
        self.openflow_name = 'host:' + self.mac if self.mac else self.name
