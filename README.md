# fmcheck

This tool provides a mechanism to test and validate Lumina Flow Manager application with OVS and Noviflow switches. It also includes obtaining eline/etree/flows/groups stats and summary information, as well as the ability to perfor
m actions such as deleting flows and groups.

- [Install](#install)
- [Usage](#usage)

## Install

### From source

```
cd flow-manager-tools
sudo python setup.py install
```

### Dependencies

Following dependencies are installed with the installation.

* **docopt**
* **pexpect**
* **pyyaml**
* **requests**
* **coloredlogs**

## Usage

The fmcheck tool validates if links, nodes and flows are in sync between the switch, configuration and operational data store, as well as providing the capability to obtain flow, group and services stats. Lscli also allows you to delete flows or groups directly from a switch.

## fmcheck
`fmcheck` will be the command after installation. This is to allow users to test `fmcheck` and `fmcheck` side by side. Eventually `fmcheck` will become `fmcheck`.

```
$ fmcheck -h
Lumina SDN Controller CLI

Usage:
  fmcheck links [-srd] [--topology=FILE] [--controller=IP]...
  fmcheck nodes [-srd] [--topology=FILE] [--controller=IP]...
  fmcheck flows [-ad] [--topology=FILE] [--controller=IP]...
  fmcheck roles [-d] [--topology=FILE] [--controller=IP]...
  fmcheck sync-status [-d] [--topology=FILE] [--controller=IP]...
  fmcheck delete-groups <name> [-d] [--topology=FILE]
  fmcheck delete-flows <name> [-d] [--topology=FILE]
  fmcheck get-flow-stats-all [-d] [--topology=FILE]
  fmcheck get-flow-stats <filter>... [-d] [--topology=FILE]
  fmcheck get-flow-node-stats-all <node> [-d] [--topology=FILE]
  fmcheck get-flow-node-stats <node> <filter>... [-d] [--topology=FILE]
  fmcheck get-group-stats-all [-d] [--topology=FILE]
  fmcheck get-group-stats <filter>... [-d] [--topology=FILE]
  fmcheck get-group-node-stats-all <node> [-d] [--topology=FILE]
  fmcheck get-group-node-stats <node> <filter>... [-d] [--topology=FILE]
  fmcheck get-eline-stats-all [-d] [--topology=FILE]
  fmcheck get-eline-stats <filter>... [-d] [--topology=FILE]
  fmcheck get-eline-summary-all [-d] [--topology=FILE]
  fmcheck get-eline-summary <filter>... [-d] [--topology=FILE]
  fmcheck get-etree-stats-all [-d] [--topology=FILE]
  fmcheck get-etree-stats <filter>... [-d] [--topology=FILE]
  fmcheck get-etree-summary-all [-d] [--topology=FILE]
  fmcheck get-etree-summary <filter>... [-d] [--topology=FILE]
  fmcheck get-sr-summary-all [-d] [--topology=FILE]
  fmcheck get-sr-summary <source> <destination> [-d] [--topology=FILE]
  fmcheck get-node-summary [-d] [--topology=FILE]

Options:
  -h --help     Show this screen.
  -t, --topology=FILE   Topolofy file name [default: fm-topo.yml].
  -c, --controller=IP   Controller IP address
  -s --stopped      If Mininet is not running.
  -r --segementrouting  Use segment routing topology.
  -a --check-stats  Check flow/groups states with previous check
  -d --debug  Log debug level
  --version     Show version.
```

**To Do**
```
  Optimize flows/groups gathering from remote OVS switches

  Documentation

  fmcheck download controller logs
  fmcheck clear controller logs

  fmcheck versions of controllers
  fmcheck versions of switches

  replace print statements with logging

    --Check if operational datastore and configurational datastore match

  fmcheck get-sr-summary-all [-d] [--topology=FILE]
  fmcheck get-sr-summary <source> <destination> [-d] [--topology=FILE]
    --Catch filter errors

  fmcheck isolate-ctrl-switch <switch_name> <seconds> [-d] [--topology=FILE]
    --Clean up log messages

  fmcheck reboot-random-controller [-d] [--topology=FILE]
  fmcheck reboot-controller <name> [-d] [--topology=FILE]
  fmcheck reboot-controller-by-switch <name> [-d] [--topology=FILE]
  fmcheck reboot-controller-by-random-switch [-d] [--topology=FILE]
    --Check if local or ssh/remote controller

  fmcheck reboot-all-switches
    --New features

  fmcheck get-etree-hop-stats
    --New feature to measure pathing efficiency for elines and etree

  fmcheck patch-upload

  fmcheck execute-on-controller <controller> <command>
  fmcheck execute-on-all-controllers <command>

  fmcheck execute-on-switch <controller> <command>
  fmcheck execute-on-all-switches <command>
```
