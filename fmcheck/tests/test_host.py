"""
Unit group functionality of host
"""

import pytest
from fmcheck.host import Host
import logging


def get_single_props():
    #return {'host': [{'ip': '127.0.0.2', 'name': 'c2'}]};
    #return {'name':'c2', 'ip':'127.0.0.2'}
    return {'controller': [{'ip': '127.0.0.2', 'name': 'c2'}], 'link': [{'source_port': 1, 'source': 'noviflow100', 'destination_port': 1, 'destination': 'noviflow200'}, {'source_port': 1, 'source': 'noviflow200', 'destination_port': 1, 'destination': 'noviflow100'}], 'switch': [{'name': 'noviflow100', 'dpid': '64', 'ip': '172.24.86.98', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}, {'name': 'noviflow200', 'dpid': 'C8', 'ip': '172.24.86.99', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}], 'host': [{'ip': '127.0.0.2', 'name': 'h1'}]} 

def test_init():
        props = get_single_props();
        if props.get('host'):
            for properties in props['host']:
                print properties;
                new_host = Host(properties);
                assert 'h1' in new_host.name 
