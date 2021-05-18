import config as cf
import logging,re,json,time

def bunch ( fqdn, **kwargs ):
    """
    First arg is the FQDN hostname to get Gconf
    bunch facts.  Second arg is the Gconf JSON
    item provided by daily exports.

    We want to build a Gconf facts databases that
    will be accessed in next inventory factory steps.
    Hence only snippet of keys will be kept.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__bunch__' )
    logger = logging.getLogger( ls )

    # Retrieve values and build JSON.

    Myzone = zone ( fqdn, **kwargs )
    (MySite, Myroom) = SiteRoom ( fqdn, **kwargs )
    MyDepResp = DepResp ( fqdn, **kwargs )
    MyEnv = environment ( fqdn, **kwargs )
      
    MyGconfFactsVars = { "name": kwargs.get('name_equipment'), \
                         "zone" : Myzone, \
                         "site": MySite, \
                         "room": Myroom, \
                         "dep_resp": MyDepResp, \
                         "environnement": MyEnv }

    # Add as an extra for physical boxes only
    # the IP of ILO.

    hardware = kwargs.get('model_type')

    if ( hardware != 'VIRTUAL_MACHINE' ):

      MyIpIlo = IpIlo (  fqdn, **kwargs )
      MyGconfFactsVars[ 'ip_ilo' ] = MyIpIlo


    MyGconfFacts = { fqdn : MyGconfFactsVars }

    return MyGconfFacts

def zone ( fqdn, **kwargs ):
    """
    First arg is the FQDN hostname to get Gconf
    bunch facts.  Second arg is the Gconf JSON
    item provided by daily exports.
    Retrieve zone value in.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__zone__' )
    logger = logging.getLogger( ls )

    # Retrieve zone key in JSON.
    zone_raw1 = kwargs.get('zone')

    if ( zone_raw1 == None ):

      # Now time to log issue and feed to blank...
      string = "Empty Gconf zone field for %s" % (fqdn)
      logger.warning( string )
      zone = None

    else:

      # Remove bad chars from Gconf inputs.
      # Substitute any white space with underscore.
  
      zone_raw2 = zone_raw1.encode('ascii', 'ignore')
      zone = re.sub( ' ', '_', zone_raw2 )

    return zone

def SiteRoom ( fqdn, **kwargs ):
    """
    First arg is the FQDN hostname to get Gconf
    bunch facts.  Second arg is the Gconf JSON
    item provided by daily exports.
    Retrieve as a tuple site and room values.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__SiteRoom__' )
    logger = logging.getLogger( ls )

    # Retrieve site key in JSON.
    SiteRoom_raw1 = kwargs.get('site')

    if ( SiteRoom_raw1 == None ):

      # Now time to log issue and feed to blank...
      string = "Empty Gconf site field for %s" % (fqdn)
      logger.warning( string )
      site = room = None

    else:

      # Remove bad chars from Gconf inputs.
      # Split to retrieve both site and room.
  
      SiteRoom_raw2 = SiteRoom_raw1.encode('ascii', 'ignore')
      site_raw = re.sub( '.* \(', '', SiteRoom_raw2 )
      site = re.sub( '\)', '', site_raw )

      room = re.sub( ' .*', '', SiteRoom_raw2 )


    return ( site, room )

def DepResp ( fqdn, **kwargs ):
    """
    First arg is the FQDN hostname to get Gconf
    bunch facts.  Second arg is the Gconf JSON
    item provided by daily exports.
    Retrieve responsible department.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__DepResp__' )
    logger = logging.getLogger( ls )

    # Retrieve dept_responsible key in JSON.
    DepResp_raw1 = kwargs.get('dept_responsible')

    if ( DepResp_raw1 == None ):

      # Now time to log issue and feed to blank...
      string = "Empty Gconf dept_responsible field for %s" % (fqdn)
      logger.warning( string )
      DepResp = None

    else:

      # Remove bad chars from Gconf inputs.
      # Substitute any white space with underscore.
  
      DepResp_raw2 = DepResp_raw1.encode('ascii', 'ignore')
      DepResp = re.sub( ' ', '_', DepResp_raw2 )

    return DepResp

def environment ( fqdn, **kwargs ):
    """
    First arg is the FQDN hostname to get Gconf
    bunch facts.  Second arg is the Gconf JSON
    item provided by daily exports.
    Retrieve IT environment.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__Environment__' )
    logger = logging.getLogger( ls )

    # Retrieve dept_responsible key in JSON.
    env_raw1 = kwargs.get('name_environment')

    if ( env_raw1 == None ):

      # Now time to log issue and feed to blank...
      string = "Empty Gconf name_environment field for %s" % (fqdn)
      logger.warning( string )
      environment = None

    else:

      # Remove bad chars from Gconf inputs.
      # Substitute any white space with underscore.
  
      env_raw2 = env_raw1.encode('ascii', 'ignore')
      environment = re.sub( ' ', '_', env_raw2 )

    return environment

def IpIlo ( fqdn, **kwargs ):
    """
    First arg is the FQDN hostname to get Gconf bunch facts.
    Second is Gconf JSON item provided by daily exports.
    Should be called only if host model_type is not
    virtual_machine.
    Retrieve IP address of ILO.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__IpIlo__' )
    logger = logging.getLogger( ls )

    # Retrieve dept_responsible key in JSON.
    IpIlo_raw1 = kwargs.get('ip_ilo')

    if ( IpIlo_raw1 == None ):

      # Now time to log issue and feed to blank...
      string = "Empty Gconf ip_ilo field for %s" % (fqdn)
      logger.warning( string )
      IpIlo = None

    else:

      # Remove bad chars from Gconf inputs.
      # Substitute any white space with underscore.
  
      IpIlo_raw2 = IpIlo_raw1.encode('ascii', 'ignore')
      IpIlo = re.sub( ' ', '_', IpIlo_raw2 )

    return IpIlo
