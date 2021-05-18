import config as cf
import logging,json

def bunch( fqdn ):
    """
    Arg is host FQDN. Function will open the both gconf
    and satellite bunch facts files as databases. It calls
    every algorithm within module to evaluate IT specific
    bubble if any. Default is set to classic LAN.

    Return retcode and DMZ JSON box bunch facts as a tuple.
    """
  
    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__bunch__' )
    logger = logging.getLogger( ls )

    # Set default to standard lan ie null value.
    MyDmz = None

    try:

      # Open GJSON as a database.
      infis = "%s/%s.gjson" % (cf.input_dir , fqdn )
      fd_infi = open( infis , 'r' )
      gjson_host = json.loads( fd_infi.read() )

      # Also open SJSON as a database.
      infis = "%s/%s.sjson" % (cf.input_dir , fqdn )
      fd_infi = open( infis , 'r' )
      sjson_host = json.loads( fd_infi.read() )

      #
      # Does the host match any bubble criteria ?
      #
  
      # Let's start with monetique checks.
      if ( monetique( fqdn, gjson_host ) == 1 ):
  
        MyDmz = "monetique"
  
      # Then check for bunker hosts.
      if ( bunker( fqdn, sjson_host ) == 1 ):

        MyDmz = "bunker"

      # Then check for bigdata hosts.
      if ( bigdata( fqdn, gjson_host ) == 1 ):

        MyDmz = "bigdata"

      # Then check for mars hosts.
      if ( mars( fqdn, sjson_host ) == 1 ):

        MyDmz = "mars"

      MyDmzFactsVars = { "dmz" : MyDmz }
      MyDmzFacts = { fqdn : MyDmzFactsVars }
      rc = 0

    except IOError as err:

      # File not found so time to log issue.
      string = "Error during DMZ evaluation phase for below host."
      logger.error( string )
      logger.error( err )
      rc = 1
      MyDmzFacts = {}
   
    return (rc, MyDmzFacts)

def monetique( fqdn, json_host ):
    """
    First args is host FQDN. Second is the per host gconf JSON.
    Algorithm is based on department responsible as a key factor
    to determine wheter or not box is part of monetique IT bubble.
    Return a boolean.
    """

    # Set no as a default value for boolean.
    monetique = 0

    # Get department responsible for box.
    dep_resp = json_host[fqdn]['dep_resp']
 
    # Does it match with configuration file list provided ?

    for index in range( len ( cf.monetique_resp ) ):

      if ( dep_resp == cf.monetique_resp[index] ):

        monetique = 1

    return monetique

def bunker( fqdn, json_host ):
    """
    First args is host FQDN. Second is the per host sat JSON.
    Algorithm is based on source capsule as a key factor
    to determine wheter or not box is part of bunker IT bubble.
    Return a boolean.
    """

    # Set no as a default value for boolean.
    bunker = 0

    # Get source capsule for box.
    capsule = json_host[fqdn]['capsule']
 
    # Does it match with configuration file value provided ?

    if ( capsule == cf.bunker_capsule ):

      bunker = 1

    return bunker

def bigdata( fqdn, json_host ):
    """
    First args is host FQDN. Second is the per host gconf JSON.
    Algorithm is based on department responsible as a key factor
    to determine wheter or not box is part of bigdata IT bubble.
    Return a boolean.
    """

    # Set no as a default value for boolean.
    bigdata = 0

    # Get department responsible for box.
    dep_resp = json_host[fqdn]['dep_resp']
 
    # Does it match with configuration file list provided ?

    for index in range( len ( cf.bigdata_resp ) ):

      if ( dep_resp == cf.bigdata_resp[index] ):

        bigdata = 1

    return bigdata

def mars( fqdn, json_host ):
    """
    First args is host FQDN. Second is the per host Satellite JSON.
    Algorithm is based on content_source capsule as a key factor
    to determine wheter or not box is part of mars IT bubble.
    Return a boolean.
    """

    # Set no as a default value for boolean.
    mars = 0

    # Get content_source capsule  for box.
    capsule = json_host[fqdn]['capsule']
 
    # Does it match with configuration file list provided ?

    for index in range( len ( cf.mars_capsule ) ):

      if ( capsule == cf.mars_capsule[index] ):

        mars = 1

    return mars
