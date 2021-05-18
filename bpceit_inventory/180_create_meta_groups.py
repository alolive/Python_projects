#!/usr/bin/python
#
# Add native Gconf environment groups to
# meta groups as children. Intended to provide
# an easiest way to classify boxes.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./180_create_meta_groups.py
#
# Changelog:
#
# v 1.0 - 2020/06/22: Creation

__author__ = "DIC_SOS_UNI <DIC_SOS_UNI@bpce-it.fr>"
__version__ = "1.0"

# Needed modules.
import datetime,logging,sys,os,re,glob
import urllib3,httplib,json

# Build path to functions directory.
dir_path = os.path.dirname( os.path.realpath( __file__ ) )
funcpath = "%s/%s" % ( dir_path , 'functions' )

# Add it to search path for modules/functions to import.
sys.path.append( funcpath )

# Import global configuration parameters as cf.
import config as cf

# Needed custom functions
import meta_group

def main():
    """
    For each native hard coded Gconf environment
    remap it to to meta group category.
    Classification can be found in config module.
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

    # Log meta groups creation starting phase.
    string = "Starting meta groups creation in inventory."
    logger.info( string )

    # Define in a list all meta groups we want to create.
    MetaGroups = [ 'MAP' , 'INT' , 'PRD' ]

    for item in MetaGroups:

      # Creation phase.
      meta_group.create( item )

      # Open it as a json.
      jsf = "%s/grp_meta_%s.json" % ( cf.input_dir, item )
      fd_jmg = open( jsf, 'r' )
      json_meta_group = json.loads( fd_jmg.read() )
      fd_jmg.close()

      # Populate with config module lists contents.
      meta_group.populate( json_meta_group )

      # Dump phase.
      meta_group.dump2file( item, json_meta_group )


if __name__ == '__main__':
    main()

