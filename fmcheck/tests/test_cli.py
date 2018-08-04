
"""
Unit test file to test CLI options of fmcheck

CLI options - 
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
#from fmcheck.shell import Shell



#def test_shell():

#    new_shell = Shell();
#    output = new_shell.Shell()
#    print output


#test_shell();


