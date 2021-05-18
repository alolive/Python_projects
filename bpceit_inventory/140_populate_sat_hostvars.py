#!/usr/bin/python
#
# For each Satellite V6 listed hosts parse
# values that does not need to be grouped
# in sjsond bunch facts file.
# Directly fill skeleton hostvars nested JSON.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./140_populate_meta_hostvars.py
#
# Changelog:
#
# v 1.0 - 2020/05/29: Creation

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
import meta_hostvars

def main():
    """
    For each host in generated JSON hosts file :
    Parse the doped Satellite bunch facts file.
    For each values with a built-in group set to no,
    Directly fill skeleton hostvars nested JSON. 
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

    # Log hostvars JSON creation starting phase.
    string = "Starting hostvars feeding with ungrouped Satellite values."
    logger.info( string )

    # Open skeleton for reading.
    jsf = "%s/%s" % ( cf.input_dir, cf.inv_skel_file )
    fd_skel = open( jsf, 'r' )
    skeleton = json.loads( fd_skel.read() )
    fd_skel.close()

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

        for host in sat_json.keys():

          # Get Satellite facts for this host.
          sat_facts = sat_json[host]

          # Parse facts searching for keys with value.          
          for (ik,iv) in sat_facts.items():

            #
            # WARNING : tricky part there
            #
            # For hostvars feed to happen we've to fulfilled
            # multiple conditions :
            #
            # First : Key name can not contain _value as they are
            #         specifications keys containig a JSON.
            # Then : Value specification must have built-in group flag
            #        set to no.
            #

            # Exclude value specifications keys.
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
                # built-in-group flag set as no.

                if ( value_specifications['built-in-group'] == "no" ):

                  # This is now time to check or create a host entry
                  # within hostvars.

                  rc = meta_hostvars.GetEntry ( fqdn, **skeleton )

                  # Check if we need to create entry before feeding.                    
                  if ( rc == 0 ):

                    meta_hostvars.create( fqdn, **skeleton )

                  # Add current key and value.
                  meta_hostvars.populate( fqdn, ik, iv, **skeleton )
                  
                  # Add current specs key and value specifications.
                  meta_hostvars.populate( fqdn, \
                                         vsk_name, \
                                         value_specifications, \
                                         **skeleton )

      except:

        # Log an error as we can not open a sjsond file.
        string = "Can not open %s doped Satellite bunch file." % ( fqdn )
        logger.error ( string )

    # Dump and write whole all skeleton.
    jsf = "%s/%s" % ( cf.input_dir, cf.inv_skel_file )
    fd_skel = open( jsf, 'w' )

    for line in json.dumps( skeleton, sort_keys=True, indent=4):

      fd_skel.write( line )

    fd_skel.close()


if __name__ == '__main__':
    main()

