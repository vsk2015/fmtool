"""

This class contains common methods to be consumed by all modules.

"""
import logging


def check_mandatory_values(obj, names):
    for name in names:
        if name not in obj or not obj[name]:
            raise Exception("{} is missing in object {}".format(name, obj))


def contains_filters(filters=None, value=None):
    if not value:
        return False
    if not filters or len(filters) <= 0:
        return True
    for fil in filters:
        try:
            if fil not in value:
                return False
        except Exception:
            logging.debug('Filter error')
    return True

def compare_switch_tables(swtableflows, run1, run2,swname):
    #logging.info("Table rows for RUN1 \n %s\n\n", swtableflows)
    l1 = []
    c1 = []
    d1 = {}
    l2 = []
    c2 = []
    d2 = {}
    # print "START-Length of switch rows", len(swtableflows)
    for i in swtableflows:
        #print i
        if i[0] == run1:
            # l1.append(i)
            c1.append(i[3])
            # d1[run1]=l1
            d1['cookie']=c1
            d1[i[3]]=i

        elif i[0] == run2:
            # l2.append(i)
            c2.append(i[3])
            # d2[run2]=l2
            d2['cookie']=c2
            d2[i[3]]=i
        else:
            print "Unknown RUN NAME"

    # print "run2 details", len(d2['cookie']),len(l1)
    # print "\n\n"
    # print "run1 details", len(d2['cookie']),len(l2)
    cookiedifference=set(d1['cookie']).symmetric_difference(d2['cookie'])
    logging.debug("Cookie difference between runs %s and %s for switch %s is below\n%s ",run1.upper(),run2.upper(),swname, str(cookiedifference))
    # print "END of Switch\n\n\n\n"
    for i in cookiedifference:
        if i not in d1['cookie']:
            # l1.append("%s \t flow not in switch %s was not found in RUN-NAME -> %s\n\n\n\n".format(d2[i][2],d2[i][1], run1.upper()))
            l1.append("{} \t".format(d2[i][2]))
        if i not in d2['cookie']:
            # l2.append("%s \t flow in switch %s was not found in RUN-NAME -> %s\n\n\n\n",d1[i][2],d1[i][1], run2.upper())
            l2.append("{} \t".format(d1[i][2]))
    if len(l1) > 0:
       logging.info("\n\n\nSWITCH NAME -> %s AND FLOWS IN RUN-NAME -> %s (but not in other):",swname,run2)
       for flow in l1:
            logging.info("%s",flow)
    if len(l2) > 0:
       logging.info("\n\n\nSWITCH NAME -> %s AND FLOWS IN RUN-NAME -> %s (but not in other):",swname,run1)
       for flow in l2:
            logging.info("%s",flow)
    logging.debug("Comparison Complete for switch %s\n\n\n\n\n", swname)
