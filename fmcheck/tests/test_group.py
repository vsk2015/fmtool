"""
Unit group functionality of group.
"""

import pytest
from fmcheck.group import Group
import logging


def test_add_of_config():
    new_group = Group('openflow:12','s1','2000000001');
    new_group.add_of_config('2000000001');
    print new_group.of_config;
    assert new_group.of_config == '2000000001';



def test_add_of_operational():
    new_group = Group('openflow:12','s1','2000000001');
    new_group.add_of_operational('2000000001');
    assert new_group.of_operational == '2000000001';

def test_add_switch():
    new_group = Group('openflow:12','s1','2000000001');
    new_group.add_switch('2000000001');
    assert new_group.switch == '2000000001';


def test_mark_as_calculated():
    new_group = Group('openflow:12','s1','2000000001');
    new_group.mark_as_calculated();
    assert new_group.calculated == True;

def test_check():
    new_group = Group('openflow:12','s1','2000000001');
    abc = new_group.check();
    print abc;

test_check();
