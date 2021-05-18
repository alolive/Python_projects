#!/usr/bin/python
#
# Add every previously created groups to skeleton.
#
# For extended information, please use:
#
# /usr/bin/pydoc ./170_skeleton_add_groups.py
#
# Changelog:
#
# v 1.0 - 2020/06/03: Creation

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
import meta_hostvars

def main():
    """
    For each group in output directory add it to
    skeleton. Dump global JSON to inventory at the
    end of process.
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

    # Log skeleton groups insertion starting phase.
    string = "Starting groups insertion in skeleton."
    logger.info( string )

    # Open skeleton for reading.
    jsf = "%s/%s" % ( cf.input_dir, cf.inv_skel_file )
    fd_skel = open( jsf, 'r' )
    skeleton = json.loads( fd_skel.read() )
    fd_skel.close()

    # Retrieve all previously created groups in a list.
    grp_path = "%s/grp_*.json" % ( cf.input_dir )
    grp_files = glob.glob ( grp_path )

    #
    # Let's loop over the file list
    #
    for file in grp_files:

      # Load it as a python dictionnary.
      fd_infi = open ( file, 'r' )
      grp_json = json.loads( fd_infi.read() )

      # Retrieve the one and only couple of key/value.
      for ( ik, iv) in grp_json.items():

        # Add the group key to skeleton.
        skeleton[ik] = iv

    # Dump enriched skeleton JSON to bpce-it inventory.
    isf = "%s/%s" % ( cf.input_dir, cf.inv_file )
    fd_inv = open( isf, 'w' )

    for line in json.dumps( skeleton, sort_keys=True, indent=4):

      fd_inv.write( line )

    fd_inv.close()


if __name__ == '__main__':
    main()

