import config as cf
import logging,json,glob,os

def GetJson( group_name ):
    """
    First arg is the per value DMZ group name
    snippet file to be opened.  Return a tuple with
    opening state as a boolean and a JSON dictionnary
    name associated with snippet.
    """

    # Set opening to false by default.
    opened = 0

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__GetJson__' )
    logger = logging.getLogger( ls )

    try:

      # Open group name  as a database.
      infig = "%s/grp_dmz_%s.json" % (cf.input_dir , group_name )
      fd_infi = open( infig , 'r' )
      dmzsnip_json = json.loads( fd_infi.read() )

      # Set boolean as success.
      opened = 1
  
    except:

      # Issue with opening.
      dmzsnip_json = None

    return ( opened , dmzsnip_json )

def create( key , group_name, json_value_specs ):
    """
    First arg is the key name to be set as var in group.
    Second arg is the group name (value) of inventory to
    create.  Typically, group_name will be a value with
    built-in group attributes set to yes. 
    Last arg will be set as var for whole group members. 
    Create empty snippet files in output dir.
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__create__' )
    logger = logging.getLogger( ls )

    vsk = "%s_value" % ( key )
    MyVars = { key : group_name, \
               vsk : json_value_specs }

    # Build group frame with associated json vars.
    MyDMZGroupVars = { "children" : [], \
                       "hosts" : [], \
                       "vars" : MyVars }

    # Add group name. 
    MyDMZGroup = { group_name : MyDMZGroupVars }

    # Dump to file for later use.
    dump2file ( group_name , MyDMZGroup )

    # Log DMZ group creation phase as info.
    string1 = "DMZ group snippet grp_dmz"
    string = "%s_%s.json created." % ( string1 , group_name )
    logger.info( string )

def dump2file ( group_name , json_group ):
    """
    First arg is the group name DMZ snippet file to
    dump to. Second is the JSON content by itself.
    Can not only be use at group creation but also after
    JSON feeding with hostnames matching criterias. 
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__dump2file__' )
    logger = logging.getLogger( ls )

    oufig = "%s/grp_dmz_%s.json" % ( cf.output_dir, group_name )

    # Open it for writing.
    fd_oufi = open(oufig, 'w' )

    # Write result in output file.
    for line in json.dumps ( json_group, sort_keys=True, indent=4 ):

      fd_oufi.write ( line )

    fd_oufi.write ('\n')

def populate ( fqdn , dmz_snip ):
    """
    First arg is the fqdn of host to insert in group held
    in second arg as JSON dmz_snip dictionnary.
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__populate__' )
    logger = logging.getLogger( ls )

    # Extract the core group info of JSON.
    for k in dmz_snip.keys():

       group_core = dmz_snip[k]

    # Append fqdn to group hosts list
    group_core['hosts'].append( fqdn )

def delete ():
    """
    Delete all grp_dmz.*.json files to clean place
    before the cumulative processus of creation.
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__delete__' )
    logger = logging.getLogger( ls )

    path = "%s/grp_dmz_*.json" % ( cf.output_dir )
    files = glob.glob( path )

    for f in files:

      os.remove( f )

    string = "All previous DMZ groups in %s removed." % ( cf.output_dir )
    logger.warning( string )

    return ()

