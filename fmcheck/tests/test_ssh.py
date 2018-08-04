"""
unit test ssh functionality of fmcheck
"""

import pytest
from fmcheck.ssh import SSH
import logging


def test_init():
    ssh = SSH(ip='127.0.0.1', user='lion', password='paass')
    assert ssh.port == 22
