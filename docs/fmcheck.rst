fmcheck
*******

The fmcheck tool validates if links, nodes and flows are in sync between the switch, configuration and operational data store, as well as providing the capability to obtain flow, group and services stats. Lscli also allows you to delete flows or groups directly from a switch.

Commands
--------

Verify
~~~~~~

Verify links between switches and hosts in network against supplied topology file.

::

$ fmcheck links [-srd] [--topology=FILE]

Verify nodes between switches and hosts in network against supplied topology file.

::

$ fmcheck nodes [-srd] [--topology=FILE]

Verify flows between switches and operational configuration in controller datastores.

::

$ fmcheck flows [-ad] [--topology=FILE]

Verifies roles found in switch with the elected owner of the cluster.

::

$ fmcheck roles [-d] [--topology=FILE]

Verify data consistency between controller datastores in a cluster.

::

$ fmcheck sync-status [-d] [--topology=FILE]


Delete
~~~~~~

Delete groups in a specific switch

::

$ fmcheck delete-random-flows [-d] [--topology=FILE]

Delete flows in a specific switch

::

$ fmcheck delete-flows <name> [-d] [--topology=FILE]



Get Stats
~~~~~~~~~

::

$ fmcheck get-flow-node-stats-all <node> [-d] [--topology=FILE]

::

$ fmcheck get-flow-node-stats <node> <filter>... [-d] [--topology=FILE]

::

$ fmcheck get-group-stats-all [-d] [--topology=FILE]

:: 

$ fmcheck get-group-stats <filter>... [-d] [--topology=FILE]

:: 

$ fmcheck get-group-node-stats-all <node> [-d] [--topology=FILE]

::

$ fmcheck get-group-node-stats <node> <filter>... [-d] [--topology=FILE]

::

$ fmcheck get-eline-stats-all [-d] [--topology=FILE]

::

$ fmcheck get-eline-stats <filter>... [-d] [--topology=FILE]

::

$ fmcheck get-eline-summary-all [-d] [--topology=FILE]

::

$ fmcheck get-eline-summary <filter>... [-d] [--topology=FILE]

::

$ fmcheck get-etree-stats-all [-d] [--topology=FILE]

::

$ fmcheck get-etree-stats <filter>... [-d] [--topology=FILE]

::

$ fmcheck get-etree-summary-all [-d] [--topology=FILE]

:: 

$ fmcheck get-etree-summary <filter>... [-d] [--topology=FILE]

::

$ fmcheck get-sr-summary-all [-d] [--topology=FILE]

::

$ fmcheck get-sr-summary <source> <destination> [-d] [--topology=FILE]

::

$ fmcheck get-node-summary [-d] [--topology=FILE]

::

$ fmcheck get-flow-stats-all [-d] [--topology=FILE]

::

$ fmcheck get-flow-stats <filter>... [-d] [--topology=FILE]


Command Options
~~~~~~~~~~~~~~~

.. literalinclude:: fmcheck_options.txt
