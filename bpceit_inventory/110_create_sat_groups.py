#!/usr/bin/python
#
# For each Satellite V6 listed hosts parse
# values to be grouped is sjsond bunch facts file.
# Create groups and feed them.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./110_create_sat_groups.py
#
# Changelog:
#
# v 1.0 - 2020/04/02: Creation

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
import satellite_group

def main():
    """
    For each host in generated JSON hosts file :
    Parse the doped satellite bunch facts file.
    For each values with a built-in group set to yes,
    create a group with value name and feed it.
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

    # Cleanup everything before new execution.
    satellite_group.delete()

    # Log Satellite groups creation starting phase.
    string = "Starting global Satellite values groups creation."
    logger.info( string )

    #
    # Let's loop over whole hosts Satellite JSON file.
    #
    for host_json in hosts_list_json['results']:
 
      fqdn = host_json['name']

      try:

        # Load Satellite doped bunch files as a JSON.
        infi = "%s/%s.sjsond" % ( cf.output_dir, fqdn )
        fd_sat_json = open( infi, 'r' ) 
        sat_json = json.loads( fd_sat_json.read() )

        for fqdn in sat_json.keys():

          sat_facts = sat_json[fqdn]

          # Parse facts searching for keys with value.          
          for (ik,iv) in sat_facts.items():
    
            #
            # WARNING : tricky part there
            #
            # For group creation to happen we've to fulfilled
            # multiple conditions :
            #
            # Fist : Key value can not be void
            # Then : Key name can not contain _value as they are
            #        specifications keys containig a JSON.
            # Then : Value specification must have built-in group flag. 
            #

            # First exclude void keys.
            if ( iv != None ):

              # Then exclude value specifications keys.
              sk = re.search ( "_value", ik )

              if ( not sk ):

                # Does that key have a value specifications JSON ?
                # Default's set to none and JSON specs to void.

                found = 0
                value_specifications = {}

                # Parse once again dictionnary.
                for (jk,jv) in sat_facts.items():

                   # Build value specifications key name to search for.
                   vsk_name = "%s_value" % ( ik )

                   if ( jk == vsk_name ):

                     # Something found. Store JSON. Set flag.
                     found = 1
                     value_specifications = jv

                # Did we have found flag set ?
                if ( found == 1 ):

                  # We also should have a JSON to search in for
                  # built-in-group flag set as yes.

                  if ( value_specifications['built-in-group'] == "yes" ):

                    # This is now time to open or create snippet file 
                    # to populate with current fqdn.

                    ( rc , sat_snip ) = satellite_group.GetJson ( iv )

                    # Check if we need to create snippet before feeding.                    
                    if ( rc == 0 ):

                      satellite_group.create( ik, iv , value_specifications )
                      ( rc , sat_snip ) = satellite_group.GetJson ( iv )

                    # Add current fqdn to snippet hosts list.
                    satellite_group.populate( fqdn, sat_snip )
                    
                    # Save new member to the snippet file.
                    satellite_group.dump2file( iv, sat_snip )

      except:

        # Log an error as we can not open a sjsond file.
        string = "Can not open %s doped satellite bunch file." % ( fqdn )
        logger.error ( string )
      

if __name__ == '__main__':
    main()

