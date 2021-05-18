#!/usr/bin/python
#
# Add specifications to each values of per
# hosts Satellite JSON.
# Information stored in output files.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./30_sat_host_doping.py
#
# Changelog:
#
# v 1.0 - 2020/02/28: Creation

__author__ = "D2I_FDT_SVS_SOU <D2I_FDT_SVS_SOU@bpce-it.fr>"
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

# Needed custom functions
import json_doper

def main():
    """
    For each host in generated JSON hosts file :
    Open the Satellite sjson file in output dir.
    Specify every keys with extra informations.
    Dump in a new file with .sjsond extension.
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

    # Open JSON hosts_list file as loop input file.
    jf = "%s/%s" % ( cf.input_dir, cf.input_hosts_file )
    fd_json = open( jf, 'r' )
    hosts_list_json = json.loads( fd_json.read() )

    # Build value specification JSON for whole keys first.

    t = "retrieved"
    s = "satellite v6 katello api endpoint host/:id"
    d = "extracted from returned json"
    b = "yes"

    json_spec1 = { "type": t,"source": s,"description": d,\
                   "built-in-group": b}

    # Log doping starting phase.
    string = "Starting Satellite results doping phase."
    logger.info( string )

    #
    # Let's loop over whole hosts Satellite JSON file.
    #
    for host_json in hosts_list_json['results']:

      # Get FQDN for output file generation
      fqdn = host_json['name']
      (rc, json_doped) = json_doper.whole( fqdn, 'sat', json_spec1 )

      if ( rc == 0 ):  

        # Remove timestamp specs as it's a non sense.
        del json_doped[fqdn]['timestamp_value']

        # Refine os_minor_value as it doesn't have to be grouped.
        # Do the same for IP list...
        del json_doped[fqdn]['os_minor_value']
        del json_doped[fqdn]['ip_address_value']
        b = "no"
        json_spec2 = { "type": t,"source": s,"description": d,\
                       "built-in-group": b}

        json_doped[fqdn]['os_minor_value'] = json_spec2
        json_doped[fqdn]['ip_address_value'] = json_spec2
      
        json_doper.dump2file ( fqdn, 'sat', json_doped )

if __name__ == '__main__':
    main()
