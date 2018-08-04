"""
Unit test utils functionality 
"""

import pytest
from fmcheck.switch import Switch
from fmcheck.link import Link
from fmcheck.group import Group
from fmcheck.utils import check_mandatory_values
from fmcheck.utils import contains_filters
import logging


def return_switch():
    return {'switch': [{'name': 's11', 'dpid': '64', 'ip': '172.24.86.98', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}, {'name': 's11', 'dpid': 'C8', 'ip': '172.24.86.99', 'password': 'noviflow', 'type': 'ovs', 'protocols': 'OpenFlow13', 'user': 'superuser'}]}


def test_check_mandatory_values():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            output = check_mandatory_values(properties,properties);
            assert output is None


def test_contains_filters():
    filters=None
    output = contains_filters(filters,'132227')
    assert output is True
