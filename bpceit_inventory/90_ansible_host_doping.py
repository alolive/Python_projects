#!/usr/bin/python
#
# Add specifications to each values of per
# hosts ansible_host evaluation facts JSON.
# Information stored in output files.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./90_ansible_host_doping.py
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

# Needed custom functions
import json_doper

def main():
    """
    For each host in generated JSON hosts file :
    Open the ansible_host evaluation ajson file in output dir.
    Specify the key with extra informations.
    Dump in a new file with .ajsond extension.
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

    # Build value default specification JSON for key first.
    # Default is to have a DNS entry fulfilled.

    t = "retrieved"
    s = "local domain name system infrastructure"
    d = "shorted dig query through hop box resolver"
    b = "no"

    json_spec1 = { "type": t,"source": s,"description": d,\
                   "built-in-group": b}

    # Log doping starting phase.
    string = "Starting ansible_host evaluation results doping phase."
    logger.info( string )

    #
    # Let's loop over whole hosts Satellite JSON file.
    #
    for host_json in hosts_list_json['results']:

      # Get FQDN for output file generation
      fqdn = host_json['name']
      (rc, json_doped) = json_doper.whole( fqdn, 'ansh', json_spec1 )

      if ( rc == 0 ):  

        # Correct specification when we have an straight IP value.
        # That means it as been evaluated.

        try:

          litteral = re.search( "[a-z]", json_doped[fqdn]['ansible_host'] )
          if not litteral:
  
            # Change specications values.
            del json_doped[fqdn]['ansible_host_value']
  
            t = "evaluated"
            s = "satellite local json bunch facts files"
            d = "algorithm evaluated by __evaluate_ansible_host__ module"
  
            json_spec2 = { "type": t,"source": s,"description": d,\
                           "built-in-group": b}
  
            json_doped[fqdn]['ansible_host_value'] = json_spec2 
           
          json_doper.dump2file ( fqdn, 'ansh', json_doped )

        except:

          json_doper.dump2file ( fqdn, 'ansh', json_doped )
          

if __name__ == '__main__':
    main()
