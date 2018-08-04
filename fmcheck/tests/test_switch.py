"""
Unit test Switch functionality 
"""

import pytest
from fmcheck.switch import Switch
from fmcheck.link import Link
from fmcheck.group import Group
import logging


def return_switch():
    return {'switch': [{'name': 's11', 'dpid': '64', 'ip': '172.24.86.98', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}, {'name': 's11', 'dpid': 'C8', 'ip': '172.24.86.99', 'password': 'noviflow', 'type': 'ovs', 'protocols': 'OpenFlow13', 'user': 'superuser'}]}


def test_init():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_switch = Switch(properties, True);
            assert new_switch.type == 'ovs' or new_switch.type == 'noviflow'


def test_get_link():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_switch = Switch(properties, True);

    output = new_switch.get_link('openflow:11:2');
    assert output.source['name'] == 'openflow:11:2';





def test_get_group():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_switch = Switch(properties, True);

    output = new_switch.get_group('2000000000');
    assert output.groupid == '2000000000';


def test_get_flow():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_switch = Switch(properties, True);
    output = new_switch.get_flow(table='0',name='openflow:11:2');
    assert output.node == 's11';


