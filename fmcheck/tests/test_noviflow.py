"""
Unit test noviflow functionality 
"""

import pytest
from fmcheck.noviflow import Noviflow
import logging
from fmcheck.ssh import NoviflowSSH



def return_switch():
    return {'switch': [{'name': 'noviflow100', 'dpid': '64', 'ip': '172.24.86.98', 'password': 'noviflow', 'type': 'noviflow', 'protocols': 'OpenFlow13', 'user': 'superuser'}, {'name': 'noviflow200', 'dpid': 'C8', 'ip': '172.24.86.99', 'password': 'noviflow', 'type': 'ovs', 'protocols': 'OpenFlow13', 'user': 'superuser'}]}


def test_init():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_novi = Noviflow(properties, True);
            assert new_novi.type == 'noviflow';

def mock_ssh_open(*a, **kw):
    print a[0]
    print kw
    if 'show status flow tableid all' in a :
        return """        [##################################################] 100%       Flow entries
[FLOW_ENTRIES] Total entries: 264
[TABLE 0] Total entries: 248
    [FLOW_ID132227]
        Timestamp        = Thu May  3 04:50:56 2018
        ofp_version      = 4
        ControllerGroup  = ctrl-1
        ControllerId     = of1
        Priority         = 99
        Idle_timeout     = 0
        Hard_timeout     = 0
        Packet_count     = 1688
        Byte_count       = 156984
        Cookie           = 1f00ffff0000000a
        Send_flow_rem    = false
        [MATCHFIELDS]
            OFPXMT_OFB_ETH_TYPE = 0x88cc
        [INSTRUCTIONS]
            [OFPIT_APPLY_ACTIONS]
                 [ACTIONS]
                    [OFPAT_OUTPUT]
                        port = ctrl
                        mlen = 65535
    [FLOW_ID132573]
        Timestamp        = Thu May  3 06:00:48 2018
        ofp_version      = 4
        ControllerGroup  = ctrl-1
        ControllerId     = of1
        Priority         = 1000
        Idle_timeout     = 0
        Hard_timeout     = 0
        Packet_count     = 0
        Byte_count       = 0
        Cookie           = 1f00001c02000064
        Send_flow_rem    = false
        [MATCHFIELDS]
            OFPXMT_OFB_ETH_TYPE = 0x8847
        [INSTRUCTIONS]
            [OFPIT_GOTO_TABLE]
                table = 1
    [FLOW_ID132574]
        Timestamp        = Thu May  3 06:00:48 2018
        ofp_version      = 4
        ControllerGroup  = ctrl-1
        ControllerId     = of1
        Priority         = 1040
        Idle_timeout     = 0
        Hard_timeout     = 0
        Packet_count     = 0
        Byte_count       = 0
        Cookie           = 1f00000301000190
        Send_flow_rem    = false
        [MATCHFIELDS]
            OFPXMT_OFB_ETH_TYPE = 0x8847
        [INSTRUCTIONS]
            [OFPIT_GOTO_TABLE]
"""

    if 'show stats group groupid all' in a :


        return """       +----------------------+
        | Group id: 2000000000 |
        +----------------------+
        Reference count:  0
        Packet count:     0
        Byte count:       0
        Duration (sec):   56020
        Duration (nsec):  898928330
        Bucket  0:
                Packet count:  0
                Byte count:    0
        Bucket  1:
                Packet count:  0
                Byte count:    0

        +----------------------+
        | Group id: 2000000001 |
        +----------------------+
        Reference count:  0
        Packet count:     0
        Byte count:       0
        Duration (sec):   56020
        Duration (nsec):  894972776
        Bucket  0:
                Packet count:  0
                Byte count:    0
        Bucket  1:
                Packet count:  0
                Byte count:    0"""


def mock_ssh_close(*a, **kw):
    print a[0]
    print kw
    return 0;


def test_get_flows():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_novi = Noviflow(properties, True);

    NoviflowSSH.execute_command = mock_ssh_open
    NoviflowSSH.close = mock_ssh_close
    output = new_novi.get_flows()
    assert output[0]['cookie'] is not None;


def test_get_groups():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_novi = Noviflow(properties, True);

    NoviflowSSH.execute_command = mock_ssh_open
    NoviflowSSH.close = mock_ssh_close
    output = new_novi.get_groups()
    assert output[0]['id'] is not None;


