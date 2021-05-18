#!/usr/bin/python
#
# Add specifications to each values of per
# hosts Gconf facts JSON.
# Information stored in output files.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./50_gconf_host_doping.py
#
# Changelog:
#
# v 1.0 - 2020/03/11: Creation

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

# Needed custom functions
import json_doper

def main():
    """
    For each host in generated JSON hosts file :
    Open the Gconf sjson file in output dir.
    Specify every keys with extra informations.
    Dump in a new file with .gjsond extension.
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
    s = "gconf daily query 40 relations-serveurs-application.json"
    d = "extracted keys value from source json"
    b = "yes"

    json_spec1 = { "type": t,"source": s,"description": d,\
                   "built-in-group": b}

    # Log doping starting phase.
    string = "Starting Gconf results doping phase."
    logger.info( string )

    #
    # Let's loop over whole hosts Satellite JSON file.
    #
    for host_json in hosts_list_json['results']:

      # Get FQDN for output file generation
      fqdn = host_json['name']
      (rc, json_doped) = json_doper.whole( fqdn, 'gconf', json_spec1 )

      if ( rc == 0 ):  

        # Refine ip_ilo value if any.

        try:

          # We do not want to build group based on name, so we got to
          # refine specification value for name.
          b ="no"
          json_spec2 = { "type": t,"source": s,"description": d,\
                         "built-in-group": b}
          del json_doped[fqdn]['name_value']
          json_doped[fqdn]['name_value'] = json_spec2

          # Do we have a ip_ilo in this JSON file ?
          ip_ilo = json_doped[fqdn]['ip_ilo']

          del json_doped[fqdn]['ip_ilo_value']
          json_doped[fqdn]['ip_ilo_value'] = json_spec2
          json_doper.dump2file ( fqdn, 'gconf', json_doped )

        except:

          json_doper.dump2file ( fqdn, 'gconf', json_doped )

if __name__ == '__main__':
    main()
