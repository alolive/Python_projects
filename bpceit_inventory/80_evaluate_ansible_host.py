#!/usr/bin/python
#
#
# Evaluate for each Satellite V6 listed hosts
# the "best" value for ansible_host access.
# Information stored in output file.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./80_evaluate_ansible_host.py
#
# Changelog:
#
# v 1.0 - 2020/03/16: Creation

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
import evaluate_ansible_host

def main():
    """
    For each host in generated JSON hosts file :
    Evaluate the ansible_host values based on algorithms.
    DNS should be the primary source of iformation but
    these algorithms may also use previous retrieved facts.
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

    # Log ansible_host evaluation starting phase.
    string = "Starting ansible_host access per host evaluation."
    logger.info( string )

    #
    # Let's loop over whole hosts Satellite JSON file.
    #
    for host_json in hosts_list_json['results']:
 
      fqdn = host_json['name']

      # Call function for evaluation of ansible_host value.
      (rc, json_evaluated) = evaluate_ansible_host.bunch( fqdn )

      # Dump if return code is zero.
      if ( rc == 0 ):

        # Build output file string and open it.
        of = "%s/%s.ajson" % ( cf.output_dir, fqdn )
        fd_of = open( of, 'w' )

        # Write result in output file.
        for line in json.dumps ( json_evaluated , sort_keys=True, indent=4):
  
          fd_of.write ( line )
        
        fd_of.write( '\n' )
        fd_of.close ()
      

if __name__ == '__main__':
    main()

