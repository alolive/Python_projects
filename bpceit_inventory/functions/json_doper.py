import config as cf
import logging,json

def dump2file ( fqdn, source, json_host ):
    """
    First args is host FQDN.  Second is the source JSON to dump.
    Can be sat, gconf, dmz, ah. Third is JSON by itself to dump.
    """
      
    # Contruct ouput file name depending on source.
    if ( source == "sat" ) :
      oufis = "%s/%s.sjsond" % ( cf.output_dir, fqdn )
  
    if ( source == "gconf" ):
      oufis = "%s/%s.gjsond" % ( cf.output_dir, fqdn )

    if ( source == "dmz" ):
      oufis = "%s/%s.ejsond" % ( cf.output_dir, fqdn )

    if ( source == "ansh" ):
      oufis = "%s/%s.ajsond" % ( cf.output_dir, fqdn )

    # Open it for writing.
    fd_oufi = open( oufis, 'w' )

    # Write result in output file.
    for line in json.dumps ( json_host, sort_keys=True, indent=4 ):

      fd_oufi.write ( line )

    fd_oufi.write ('\n')
    fd_oufi.close()
    
def whole( fqdn, source, value_specs ):
    """
    First args is host FQDN.  Second is the source JSON to open.
    Can be sat, gconf, dmz, ah. Third is JSON dictionary for
    each keys specification. That whole function will add 
    the provided value details for each keys found.
    Result should be dumped through dump2file.
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__whole__' )
    logger = logging.getLogger( ls )

    # Try to open source related file to enrich. Log if errors.
    try:

      if ( source == "sat" ) :
        infis = "%s/%s.sjson" % (cf.input_dir , fqdn )

      if ( source == "gconf" ):
        infis = "%s/%s.gjson" % (cf.input_dir , fqdn )
  
      if ( source == "dmz" ):
        infis = "%s/%s.ejson" % (cf.input_dir , fqdn )

      if ( source == "ansh" ):
        infis = "%s/%s.ajson" % (cf.input_dir , fqdn )

      fd_infi = open( infis , 'r' )
      json_host = json.loads( fd_infi.read() )

      for key in json_host[fqdn].keys():

        key_doped = "%s_value" % ( key )
        json_host[fqdn][ key_doped ] = value_specs
      
      retcode = 0
      return ( retcode, json_host )

    except IOError as err:
 
      # File not found so time to log issue.
      string = "Error during %s doping phase for below host." % ( source )
      logger.error( string )
      logger.error( err )

      retcode = 1
      return ( retcode, "" )
