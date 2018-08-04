"""fmcheck CLI

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
  fmcheck (-h | --help)

Options:
  -h --help     Show this screen.
  -t, --topology=FILE   Topolofy file name [default: fm-topo.yml].
  -c, --controller=IP   Controller IP address
  -s --stopped      If Mininet is not running.
  -r --segmentrouting  Use segment routing topology.
  -a --check-stats  Check flow/groups states with previous check
  -d --debug  Log debug level
  --version     Show version.

"""
from __future__ import print_function
import os
import sys
import yaml
import logging
import coloredlogs
from fmcheck.topology import Topology
import fmcheck.openflow
from docopt import docopt


class Shell(object):

    def __init__(self):
        arguments = docopt.docopt(__doc__, version='fmcheck 1.0')

        # Reduce urllib3 logging messages
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        # Colored logging
        if arguments['--debug']:
            logging.getLogger().setLevel(logging.DEBUG)
            coloredlogs.install(level='DEBUG')
            # print(arguments)
        else:
            logging.getLogger().setLevel(logging.INFO)
            coloredlogs.install(level='INFO')

        if arguments['--topology']:
            topo_file = arguments['--topology']
            if not (os.path.isfile(topo_file)):
                raise Exception(
                    "given topology file {} not found".format(topo_file))
        else:
            topo_file = 'prod-topo.yml' if os.path.isfile('prod-topo.yml') else None
            topo_file = 'mn-topo.yml' if not topo_file and os.path.isfile(
                'mn-topo.yml') else topo_file
            topo_file = 'fm-topo.yml' if not topo_file and os.path.isfile(
                'fm-topo.yml') else topo_file
            if not topo_file:
                raise Exception('default topology file not found')

        props = None
        if os.path.isfile(topo_file):
            with open(topo_file, 'r') as f:
                props = yaml.load(f)

        if props is None:
            logging.error("yml topology file %s not loaded", topo_file)
            sys.exit(1)

        if arguments['--controller']:
            props['controller'] = []
            i = 0
            for ip in arguments['--controller']:
                props['controller'].append(
                    {'name': "c{}".format(i),
                     'ip': ip
                     })
                i = i + 1

        result = None
        topology = Topology(props)
        if arguments['links']:
            should_be_up = True if not arguments['--stopped'] else False
            include_sr = True if arguments['--segmentrouting'] else False
            result = topology.validate_links(
                should_be_up=should_be_up, include_sr=include_sr)

        elif arguments['nodes']:
            should_be_up = True if not arguments['--stopped'] else False
            include_sr = True if arguments['--segmentrouting'] else False
            result = topology.validate_nodes(
                should_be_up=should_be_up, include_sr=include_sr)

        elif arguments['roles']:
            result = topology.validate_nodes_roles()

        elif arguments['flows']:
            result = topology.validate_openflow_elements()

        elif arguments['sync-status']:
            result = topology.validate_cluster()

        # Delete commands
        elif arguments['delete-groups']:
            switch = topology.get_switch(arguments['<name>'])
            if switch:
                result = switch.delete_groups()
            else:
                logging.error("switch %s not found", arguments['<name>'])

        elif arguments['delete-flows']:
            result = topology.get_switch(arguments['<name>']).delete_flows()

        # Get flow stats
        elif arguments['get-flow-stats-all']:
            result = topology.get_random_controller().get_flow_stats()

        elif arguments['get-flow-stats']:
            result = topology.get_random_controller().get_flow_stats(
                filters=arguments['<filter>'])

        elif arguments['get-flow-node-stats-all']:
            result = topology.get_node_cluster_owner(
                arguments['<node>']).get_flow_stats(node_name=arguments['<node>'])

        elif arguments['get-flow-node-stats']:
            result = topology.get_node_cluster_owner(
                arguments['<node>']).get_flow_stats(node_name=arguments['<node>'], filters=arguments['<filter>'])

        # Get group stats
        elif arguments['get-group-stats-all']:
            result = topology.get_random_controller().get_group_stats()

        elif arguments['get-group-stats']:
            result = topology.get_random_controller().get_group_stats(
                filters=arguments['<filter>'])

        elif arguments['get-group-node-stats-all']:
            result = topology.get_node_cluster_owner(
                openflow_name=arguments['<node>']).get_group_stats(node_name=arguments['<node>'])

        elif arguments['get-group-node-stats']:
            result = topology.get_node_cluster_owner(
                openflow_name=arguments['<node>']).get_group_stats(filters=arguments['<filter>'], node_name=arguments['<node>'])

        # Get Eline stats
        elif arguments['get-eline-stats-all']:
            result = topology.get_random_controller().get_eline_stats()
        elif arguments['get-eline-stats']:
            result = topology.get_random_controller().get_eline_stats(
                filters=arguments['<filter>'])
        elif arguments['get-eline-summary-all']:
            result = topology.get_random_controller().get_eline_summary()
        elif arguments['get-eline-summary']:
            result = topology.get_random_controller().get_eline_summary(
                filters=arguments['<filter>'])

        # Get Etree stats
        elif arguments['get-etree-stats-all']:
            result = fmcheck.openflow.get_etrees(
                topology.get_random_controller())
            result = topology.get_random_controller().get_etree_stats()
        elif arguments['get-etree-stats']:
            result = topology.get_random_controller().get_etree_stats(
                filters=arguments['<filter>'])
        elif arguments['get-etree-summary-all']:
            result = topology.get_random_controller().get_etree_summary()
        elif arguments['get-etree-summary']:
            result = topology.get_random_controller().get_etree_summary(
                filters=arguments['<filter>'])

        # Get Segment Routing info
        elif arguments['get-sr-summary-all']:
            result = topology.get_random_controller().get_sr_summary_all(
                topology.switches_by_openflow_name)
        elif arguments['get-sr-summary']:
            result = topology.get_random_controller().get_sr_summary(
                topology.switches_by_openflow_name,
                source=arguments['<source>'], destination=arguments['<destination>'])
        # Get Node Summary
        elif arguments['get-node-summary']:
            result = topology.get_random_controller().get_node_summary(
                topology.switches_by_openflow_name)

        if not result:
            sys.exit(1)


def main():
    Shell()


if __name__ == "__main__":
    Shell()
