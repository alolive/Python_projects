#!/usr/bin/python
#
#
# Evaluate for each Satellite V6 listed hosts
# the DMZ value depending on algorithm.
# Information stored in output file.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./60_evaluate_host_dmz.py
#
# Changelog:
#
# v 1.0 - 2020/03/11: Creation

__author__ = "DIC_SOS_UNI <DIC_SOS_UNI@bpce-it.fr>"
__version__ = "1.0"

# Needed modules.
import datetime,logging,sys,os,re
import urllib3,httplib,json

# Build path to functions directory.
dir_path = os.path.dirname( os.path.realpath( __file__ ) )
funcpath = "%s/%s" % ( dir_path , 'functions' )

# Add it to search path for modules/functions to import.
sys.path.append( funcpath )

# Import global configuration parameters as cf.
import config as cf

# Needed custom functions
import evaluate_dmz

def main():
    """
    For each host in generated JSON hosts file :
    Evaluate the DMZ values based on algorithms.
    These algorithms may use previous retrieved facts.
    As of now, evaluation is done for bunker
    monetique, big data and classic LAN.
    dmz default value is set null ie no IT specific
    bubble just standard LAN.
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

    # Log DMZ evaluation starting phase.
    string = "Starting DMZ per host evaluation."
    logger.info( string )

    #
    # Let's loop over whole hosts Satellite JSON file.
    #
    for host_json in hosts_list_json['results']:
 
      fqdn = host_json['name']
      # Call function for evaluation of DMZ value.
      (rc, json_evaluated) = evaluate_dmz.bunch( fqdn )

      # Dump if return code is zero.
      if ( rc == 0 ):

        # Build output file string and open it.
        of = "%s/%s.ejson" % ( cf.output_dir, fqdn )
        fd_of = open( of, 'w' )

        # Write result in output file.
        for line in json.dumps ( json_evaluated , sort_keys=True, indent=4):
  
          fd_of.write ( line )
        
        fd_of.write( '\n' )
        fd_of.close ()
      

if __name__ == '__main__':
    main()

