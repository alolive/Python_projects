#!/usr/bin/python
#
#
# Retrieve from Satellite V6 host detail in JSON format.
# Information stored in output files.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./20_get_sat_host_details.py
#
# Changelog:
#
# v 1.0 - 2020/02/11: Creation

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
import get_sat_hosts
import json_sat_filtered

def main():
    """
    For each host in generated JSON hosts file :
    First check data Freshness then call
    Satellite API through get_sat_hosts.details.
    Data are considered fresh if they've been retrieved
    less then three days ago (72 hours).

    Gather everything but dump only in per host file
    what's is needed for next factory steps.
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

    # Turn off annoying http warnings.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

    # Open JSON hosts_list file as input file
    jf = "%s/%s" % ( cf.input_dir, cf.input_hosts_file )
    fd_json = open( jf, 'r' )
    hosts_list_json = json.loads( fd_json.read() )
    
    # Log massive API call starting.
    string = "Starting massive API calls for details on %s" % ( cf.url_base )
    logger.info( string )

    #
    # Let's loop over whole hosts Satellite JSON file.
    #
    for host_json in hosts_list_json['results']:

      # Get id for API call
      host_id = host_json['id']

      # Get FQDN for output file generation
      host_fqdn = host_json['name']

      # Call API
      # Do we already have a sjson file with not so bad timestamp ?

      try:

        pj = "%s/%s.sjson" % (cf.output_dir , host_fqdn )
        fd_pj = open( pj , 'r' )
        previous_json = json.loads( fd_pj.read() )

      except IOError as err:
 
        # File not found so time to call.
        result_rc, result = get_sat_hosts.details( cf.url_base , host_id )

      else:

        # Evaluate timestamp gap. Must be under 72 hours.
        now = round( time.time () / 3600 )

        # Let's see if JSON's containing a timestamp.
        try:

          ts = previous_json[host_fqdn]['timestamp']
          gap = ( now - ts )
  
          # More than 3 days old so refresh by calling API.
          if ( gap >= 72 ):

            result_rc, result = get_sat_hosts.details( cf.url_base , host_id )
 
          else:

            # Log information of skipping refreshing.
            result_rc = 199
            result = "Fresh info for %s. Skip API call." % ( host_fqdn )

        except:

          # The JSON was empty, bad or messy thus call API.

          result_rc, result = get_sat_hosts.details( cf.url_base , host_id )
      
      #
      # Depending on return code. Choose proper actions.
      #

      if ( result_rc == 200 ):

          # We got a correct answer. Dumping and count.

          string1 = "API retcode : %s. " % (result_rc)
          string2 = "Dumping JSON filtered results to file"
          string = "%s%s" % ( string1, string2 )
           
          logger.info( string )

          # Write result in output file.
          of = "%s/%s.sjson" % ( cf.output_dir, host_fqdn )
          fd_of = open( of, 'w' )

          # Filter before dumping.
          MySatFacts = json_sat_filtered.bunch ( host_fqdn, **result )

          for line in json.dumps( MySatFacts, sort_keys=True, indent=4):
       
              fd_of.write( line )
                
          fd_of.write( '\n' )
          fd_of.close ()

      elif ( result_rc == 199 ):

        # Fresh data so just log that we skipped call.

        logger.info( result )

      else:

        # Had issue with the call...

        string = "API call failed. Return code is %s" % (result_rc)
        logger.error( result )

if __name__ == '__main__':
    main()
