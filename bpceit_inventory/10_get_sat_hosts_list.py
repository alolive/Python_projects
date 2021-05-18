#!/usr/bin/python
#
#
# Retrieve all Satellite V6 hosts in JSON format.
# Information stored in output file.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./10_get_sat_hosts_list.py
#
# Changelog:
#
# v 1.0 - 2020/02/04: Creation
# v 1.1 - 2020/09/14: Add a retry loop to wait for Satellite response

__author__ = "D2I_FDT_SVS_SOU <D2I_FDT_SVS_SOU@bpce-it.fr>"
__version__ = "1.1"

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

def main():
    """
    Call Satellite API through get_hosts_thin.
    Depending on API ret code we dump returned JSON to
    output file or return code is shown as error in logs.
    JSON provided contains number of hosts retrieved.
    Log that number with WARNING priority.
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

    # We'll call API and log call starting with retries and timer. 
    for i in range (1,5):
    
      string = "Calling API (try : %s) on %s" % ( i, cf.url_base )
      logger.info( string )
      result_rc, result = get_sat_hosts.thin( cf.url_base )
  
      # We got a correct answer. We can exit loop.
      if result_rc == 200:
       
        break

      # Add extra wait time for Satellite to respond...
      time.sleep(90*i)

    #
    #  We got a correct answer. Dump to file 
    #
    if result_rc == 200:
 
      # Feed log file with ret code.
      string = "API retcode : %s. Dumping JSON result to file" % (result_rc)
      logger.info( string )
  
      # Build output file string and open it.
      of = "%s/%s" % ( cf.output_dir, cf.output_hosts_file )
      fd_of = open( of, 'w' )

      # Write result in output file.
      for line in json.dumps ( result , sort_keys=True, indent=4):
    
        fd_of.write ( line )
          
      fd_of.close ()
    
      # Feed log file with number of retrieved hosts.
      string = "Info received for %s hosts" % ( result["total"] )
      logger.warning( string )
  
    #
    # Had issue with the call...
    #
    else:

      # Feed log file with ret code.
      string = "API call failed. Return code is %s" % (result_rc)
      logger.error( string )

      # Feed log file with error message.
      logger.error( result )

if __name__ == '__main__':
    main()
