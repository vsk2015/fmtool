"""
Unit OVS functionality 
"""

import pytest
from fmcheck.ovs import OVS
from fmcheck.switch import Switch
from fmcheck.ssh import NoviflowSSH
import logging


def return_switch():
    return {'switch': [{'name': 's11', 'dpid': '64', 'ip': '172.24.86.98', 'password': 'noviflow', 'type': 'ovs', 'protocols': 'OpenFlow13', 'user': 'superuser'}, {'name': 's11', 'dpid': 'C8', 'type': 'ovs', 'protocols': 'OpenFlow13'}]}

def test_init_local():
    props = return_switch();
    if props.get('switch'):
            print props['switch'][1];
            new_ovs = OVS(props['switch'][1], True);
            assert new_ovs.execute_local == True


def test_init():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_ovs = OVS(properties, True);
            assert new_ovs.type == 'ovs';

def mock_ssh(*a, **kw):
    print a[0]
    print kw
    if 'sudo ovs-ofctl dump-flows s11 --protocol=Openflow13' in a :
        flows = '''cookie=0x2b00000000000003, duration=94526.209s, table=0, n_packets=18906, n_bytes=1644822, priority=100,dl_type=0x88cc actions=CONTROLLER:65535
 cookie=0x1f0000010000000a, duration=94526.206s, table=0, n_packets=0, n_bytes=0, priority=99,dl_type=0x88cc actions=CONTROLLER:65535
 cookie=0x1f00000300000064, duration=94451.977s, table=0, n_packets=0, n_bytes=0, priority=1000,mpls actions=goto_table:1
 cookie=0x1f00000200000190, duration=94451.849s, table=0, n_packets=0, n_bytes=0, priority=1040,mpls actions=goto_table:1
 cookie=0x2b00000000000002, duration=94522.204s, table=0, n_packets=79, n_bytes=5762, priority=2,in_port="s11-eth2" actions=output:"s11-eth1"
 cookie=0x2b00000000000003, duration=94522.204s, table=0, n_packets=37, n_bytes=2590, priority=2,in_port="s11-eth1" actions=output:"s11-eth2",CONTROLLER:65535
 cookie=0x1f00000600000190, duration=94451.849s, table=1, n_packets=0, n_bytes=0, priority=30311,mpls,in_port="s11-eth2",mpls_label=18012 actions=group:2000000001
 cookie=0x1f00000400000190, duration=94451.849s, table=1, n_packets=0, n_bytes=0, priority=30310,mpls,mpls_label=15002 actions=pop_mpls:0x8847,output:"s11-eth2"
 cookie=0x1f00000500000190, duration=94451.849s, table=1, n_packets=0, n_bytes=0, priority=30310,mpls,mpls_label=18012 actions=group:2000000000'''

        return flows;

    if 'sudo ovs-ofctl dump-group-stats s11 --protocol=Openflow13' in a :

        groups = ''' group_id=2000000001,duration=96225.011s,ref_count=1,packet_count=0,byte_count=0,bucket0:packet_count=0,byte_count=0
 group_id=2000000000,duration=96225.011s,ref_count=1,packet_count=0,byte_count=0,bucket0:packet_count=0,byte_count=0'''

        return groups;


def test_get_flows():

    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_ovs = OVS(properties, True);
    new_ovs._execute_command = mock_ssh;
    output = new_ovs.get_flows();
    print output[0]['cookie'];
    assert output[0]['cookie'] is not None;





def test_get_groups():
    props = return_switch();
    if props.get('switch'):
        for properties in props['switch']:
            print properties;
            new_ovs = OVS(properties, True);
    new_ovs._execute_command = mock_ssh;
    output = new_ovs.get_groups();
    print output;
    assert output[0]['id'] is not None;

