import config as cf
import logging,re,json,time

def bunch ( fqdn, **kwargs ):
    """
    First arg is host FQDN we want to get sat bunch facts.
    Second arg is the per host API output JSON.
    We want to build a Satellite facts databases that
    will be accessed in next inventory factory steps.
    Hence only snippet of keys will be kept.
    """

    MyHc = hostcollections ( fqdn, **kwargs )
    MySource = capsule ( fqdn, **kwargs )
    MyModel = hardware ( fqdn, **kwargs )
    MyIPs = iplist ( fqdn, **kwargs )
    (MyOsMajor, MyOsMinor) = osmajmin ( fqdn, **kwargs )
    MyTS = round( time.time () / 3600 )

    MySatFactsVars = { "host_collections": MyHc, \
                   "capsule": MySource, \
                   "os_major": MyOsMajor, \
                   "os_minor": MyOsMinor, \
                   "ip_address": MyIPs, \
                   "hardware_type": MyModel, \
                   "timestamp": MyTS \
                   }

    MySatFacts = { fqdn : MySatFactsVars }
  
    return MySatFacts

def hostcollections ( fqdn, **kwargs ):
    """
    First arg is host FQDN we want to get sat bunch facts.
    Second arg is the per host API output JSON.
    Extract and return host collections from JSON.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__hostcollections__' )
    logger = logging.getLogger( ls )

    # Retrieve host collections part of JSON.
    hc = kwargs.get('host_collections')

    try :

      MyHc = hc[0]['name']

    except:

      MyHc = None
      # Feed log file with issue.
      string = "Empty host collections for %s" % (fqdn)
      logger.warning( string )

    return MyHc

def capsule ( fqdn, **kwargs ):
    """
    First arg is host FQDN we want to get sat bunch facts.
    Second arg is the per host API output JSON.
    Extract and return source contents (capsule) from JSON.
    """
    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__capsule__' )
    logger = logging.getLogger( ls )

    # Retrieve selected parts of JSON.
    cfa = kwargs.get('content_facet_attributes', None)

    try :

      mysource = cfa['content_source']['name']

      # Keep only short name and flag as content_source
      # to avoid future groupname with same name as host.
      mysource1 = re.sub( '\..*$', '', mysource )
      MySource = re.sub( '^', 'content_source_', mysource1 )

    except:

      MySource = None
      # Feed log file with issue.
      string = "Empty source content capsule for %s" % (fqdn)
      logger.warning( string )

    return MySource

def hardware ( fqdn, **kwargs ):
    """
    First arg is host FQDN we want to get sat bunch facts.
    Second arg is the per host API output JSON.
    Extract and return hardware type from JSON.
    """
    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__hardware__' )
    logger = logging.getLogger( ls )

    # Retrieve selected parts of JSON.
    facts = kwargs.get('facts', None)

    try :

      # Get model type and remove any blank.
      MyMod = facts['dmi::system::product_name']
      MyModel = re.sub( ' ', '_', MyMod )

      # Special care for IBM boxes... Many thanks big blue.
      if ( re.search ( "_x3650_M3", MyModel ) ):

        # Rewrite MyModel to get rd of serial num...
        MyModel = "IBM_x3650_M3"

      if ( re.search ( "_x3650_M4", MyModel ) ):

        # Rewrite MyModel to get rd of serial num...
        MyModel = "IBM_x3650_M4"

    except:

      MyModel = None
      # Feed log file with issue.
      string = "Empty hardware model type for %s" % (fqdn)
      logger.warning( string )

    return MyModel

def iplist ( fqdn, **kwargs ):
    """
    First arg is host FQDN we want to get sat bunch facts.
    Second arg is the per host API output JSON.
    Extract and return all host IP in list format from JSON.
    """
    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__iplist__' )
    logger = logging.getLogger( ls )

    # Retrieve selected parts of JSON.
    facts = kwargs.get('facts', None)

    # We have to build and populate a list for IP
    MyIPs = []
    index = 0
   
    try:

      for key in facts.keys ():
  
        # Looking for specific JSON part to get IPs.
        result = re.search( "net::interface.*::ipv4_address$" , key)
        if result :
  
          ip = facts[key]
          
          # Insert only if not "Unknown" as seen in some outputs...
  
          if ( ip != "Unknown" ):
  
            MyIPs.insert( index, ip )
  
          index = index + 1

    except:

      # Nothing found... Got to log as an issue !
      if ( index == 0 ):
  
        string = "Empty satellite IP list for %s" % (fqdn)
        logger.warning( string )
  
    return MyIPs

def osmajmin ( fqdn, **kwargs ):
    """
    First arg is host FQDN we want to get sat bunch facts.
    Second arg is the per host API output JSON.
    Extract and return os major and minor from JSON.
    Return as a tuple.
    """
    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__osmajmin__' )
    logger = logging.getLogger( ls )

    # Retrieve selected parts of JSON.
    facts = kwargs.get('facts', None)

    # First try in facts JSON subpart.

    try:

      MyOs = facts['distribution::version']

    except:

      MyOs = None

    if ( MyOs == None ):

      # Then try the operatingsystem_name part of JSON.

      try:

        MyOs =  kwargs.get('operatingsystem_name', None)

      except:

        MyOs = None

    if ( MyOs == None ):

      # Now time to log issue and feed to blank...
      string = "Empty OS versions for %s" % (fqdn)
      logger.warning( string )
      MyOsMajor = MyOsMinor = None

    else:

      # Extract major minor releases.
      MyOsMaj = re.sub( '\..*', '', MyOs )
      MyOsMaj_1 = re.sub( 'RHEL Server ', '', MyOsMaj )
      MyOsMajor = re.sub( 'RedHat ', '', MyOsMaj_1 )
      MyOsMinor = re.sub( '^.*\.', '', MyOs )
  
    return ( MyOsMajor, MyOsMinor )
