import config as cf
import logging,json,glob,os

def GetEntry( fqdn, **kwargs ):
    """
    Check if there's an existing fqdn entry in skeleton
    hostvars nested JSON. Boolean return.
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__GetEntry__' )
    logger = logging.getLogger( ls )

    try:

      # is the fqdn an item of hostvars JSON ?
      # Retrieve selected parts of skeleton.
      meta = kwargs.get('_meta', None)

      e = meta['hostvars'][fqdn]
      entry = 1
  
    except:

      entry = 0

    return( entry )

def create( fqdn, **kwargs ):
    """
    Create a fqdn item in hostvars nested JSON.
    Initial value is set to null.
    """
    
    # Retrieve selected parts of skeleton.
    meta = kwargs.get('_meta', None)

    # Add key and void value for provided fqdn.
    meta['hostvars'][fqdn] = {}

    return( )

def populate ( fqdn, key, value, **kwargs ):
    """
    First arg is the fqdn of host in hostvars.
    second an third args are couple of value to insert
    in dictionnary.
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__populate__' )
    logger = logging.getLogger( ls )

    # Retrieve selected parts of skeleton.
    meta = kwargs.get('_meta', None)

    # Add provided couple key/value in hostvars nested JSON.
    meta['hostvars'][fqdn][key] = value

    return( )
