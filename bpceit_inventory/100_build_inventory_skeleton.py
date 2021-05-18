#!/usr/bin/python
#
# Build initial fram for ansible inventory. 
# It'll be filled by later python scripts in
# next steps factory.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./100_build_inventory_skeleton.py
#
# Changelog:
#
# v 1.0 - 2020/03/19: Creation

__author__ = "DIC_SOS_UNI <DIC_SOS_UNI@bpce-it.fr>"
__version__ = "1.0"

# Needed modules.
import time,datetime,logging,sys,os,re
import urllib3,httplib,json

# Build path to functions directory.
dir_path = os.path.dirname( os.path.realpath( __file__ ) )
funcpath = "%s/%s" % ( dir_path , 'functions' )

# Add it to search path for modules/functions to import.
sys.path.append( funcpath )

# Import global configuration parameters as cf.
import config as cf

def main():
    """
    Build each single component of a JSON type ansible inventory.
    Put them all together in "empty" file to be later filled.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( os.path.basename(__file__) , __name__ )
    logger = logging.getLogger( ls )

    # Prepare logging modules parameters
    lf = "%s/%s" % ( cf.logs_dir, cf.logs_file )

    logging.basicConfig( level=logging.DEBUG,
                         format="%(asctime)s | %(levelname)s | " +\
                                "%(threadName)s | " + \
                                "%(name)s | %(message)s",
                         filename=lf,
                         filemode='a')

    # Build meta part with its nested JSON vars.
    meta = { "hostvars" : {} , "vars" : {} } 

    # Build the all group.
    # Add ungrouped by default to it (prerequisite).
    # Set ansible_connection to ssh for everyone.
    all = { "children" : [] , "hosts" : [] , "vars" : {} }
    all['children'].insert(0, "ungrouped")
    all['vars']['ansible_connection'] = "ssh"

    # Also build the ungrouped mandatory group.
    ungrouped = { "children" : [] , "hosts" : [] , "vars" : {} } 

    # Bring the skeleton up.
    skel = { "_meta" : meta, \
             "all": all, \
             "ungrouped": ungrouped \
           }

    # Build output file string and open it.
    of = "%s/%s" % ( cf.output_dir, cf.inv_skel_file )
    fd_of = open( of, 'w' )

    # Write result in output file.
    for line in json.dumps ( skel , sort_keys=True, indent=4):

      fd_of.write ( line )

    fd_of.write ( '\n' )
    fd_of.close ()



if __name__ == '__main__':
    main()
