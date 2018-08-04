"""
Unit test link functionality of fmcheck
"""

import pytest
from fmcheck.link import Link
import logging


def test_init():
    src_node_port = "openflow:11:2"
    dst_node_port = "openflow:12:1"
    link = Link(src_node_port, dst_node_port)
    print link.source
    assert link.source['id'] == '11' 


def test_add_sr_dst():
    src_node_port = "openflow:11:2"
    dst_node_port = "openflow:12:1"
    link = Link(src_node_port, dst_node_port)
    link.add_sr_dst(dst_node_port)
    print link.sr_dst
    assert link.sr['id'] == '12'    

def test_add_of_dst():
    src_node_port = "openflow:11:2"
    dst_node_port = "openflow:12:1"
    link = Link(src_node_port, dst_node_port)
    link.add_of_dst(dst_node_port)
    print link.of_dst
    assert link.of['id'] == '12'    
