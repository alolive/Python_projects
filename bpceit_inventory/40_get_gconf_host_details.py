#!/usr/bin/python
#
#
# Retrieve all per host Gconf details in JSON format.
# Information stored in output file.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./40_get_gconf_hosts_details.py
#
# Changelog:
#
# v 1.0 - 2020/03/02: Creation

__author__ = "D2I_FDT_SVS_SOU <D2I_FDT_SVS_SOU@bpce-it.fr>"
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
import json_gconf_filtered

def main():
    """
    For each host in generated JSON hosts file :
    Retrieve selected fields from daily export Gconf CSV.

    Gather only in per host file what's is needed
    for next factory steps.
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

    # Log Gconf JSON build starting phase.
    string = "Starting Gconf per host gathering."
    logger.info( string )

    # Open the Gconf JSON as data input file to retrieve from.
    infi = "%s/%s" % ( cf.gconf_dir , cf.gconf_json_file )
    fd_infi = open ( infi, 'r' )
    gconf = json.loads ( fd_infi.read() )

    #
    # Let's loop over whole hosts Satellite JSON file.
    #
    for host_json in hosts_list_json['results']:
 
      # Convert hostname to Gconf friendly matching...
      fqdn = host_json['name']
      NAME = re.sub( '\..*$', '', fqdn ).upper()
  
      # 
      # Browse all item list until something's found.
      #

      # Set found to zero and blank status by default
      found = 0
      status = ""

      for index in range( len ( gconf ) ):
 
        # Get JSON for item
        item = gconf[index]

        #
        # Search for NAME in matching in items. Retrieve info
        # only if status is "En fonction". Else log issues.
        #
        if ( item['name_equipment'] == NAME ): 

          # Gconf status is good so do the job.
          if ( item['name_state'] == "En fonction" or \
               item['name_state'].encode('ascii', 'ignore') == "Install" ):

            # Found the box in inventory
            found = 1

            # Gather Gconf facts.
            MyGconfFacts = json_gconf_filtered.bunch ( fqdn, **item )
  
            # Dumping result to file. Action logged as info.
            string = "Dumping JSON filtered results to file"
            logger.info( string )
  
            # Write result in output file.
            of = "%s/%s.gjson" % ( cf.output_dir, fqdn )
            fd_of = open( of, 'w' ) 
  
            for line in json.dumps( MyGconfFacts, sort_keys=True, indent=4):
         
                fd_of.write( line )
                  
            fd_of.write( '\n' )
            fd_of.close ()
  
            break

          # log status issues depending on severity.
          elif ( item['name_state'] == "Au rebut" and \
                 item['department_system'] == "INF_SOS_UNI" ):

            # Found the box in inventory but continue searching.
            status = "Au rebut"

          elif ( item['name_state'] == "Inactif" and \
                 item['department_system'] == "INFSOS_UNI" ):

            # Found the box in inventory but continue searching.
            status = "Inactif"

      if ( found == 0 and status == "Au rebut" ):

        # Log "Au rebut" as an error for immediate clean-up.
        string = "host %s state is Au rebut. Please remove in Satellite." % ( fqdn )
        logger.error( string )

      if ( found == 0 and status == "Inactif" ):

        # Log "Inactif" as a warning for later check.
        string = "host %s state is Inactif. Skipped for today." % ( fqdn )
        logger.warning( string )

      if ( found == 0 and status == "" ):
      
        # Log critical issue as we can't find box in Gconf...
        string = "Can not find Gconf entry for %s" % (fqdn)
        logger.critical( string )


if __name__ == '__main__':
    main()

