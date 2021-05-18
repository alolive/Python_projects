import config as cf
import logging,json,glob,os

def create( group_name ):
    """
    First arg is the group name to be created.
    Create empty snippet files in output dir.
    Also add specifications to vars in order to
    provide explanations.
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__create__' )
    logger = logging.getLogger( ls )

    # Build value default specification JSON for group.

    t = "evaluated"
    s = "Meta environment to ease perimeter access"
    d = "Based on a static gconf environment values list"
    b = "yes"

    json_spec1 = { "type": t,"source": s,"description": d,\
                   "built-in-group": b}

    # Build meta group frame with empty json vars.
    MyMetaGroupVars = { "children" : [], \
                       "hosts" : [], \
                       "vars" : { "meta_env" : group_name,\
                                  "meta_env_value" : json_spec1 } }

    # Add group name. 
    MyMetaGroup = { group_name : MyMetaGroupVars }

    # Dump to file for later use.
    dump2file ( group_name , MyMetaGroup )

    # Log meta group creation phase as info.
    string1 = "Meta group snippet grp_meta"
    string = "%s_%s.json created." % ( string1 , group_name )
    logger.info( string )

def dump2file ( group_name , json_meta_group ):
    """
    First arg is the group name Satellite snippet file to
    dump to. Second is the JSON content by itself.
    Can not only be use at group creation but also after
    JSON feeding with hostnames matching criterias. 
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__dump2file__' )
    logger = logging.getLogger( ls )

    oufig = "%s/grp_meta_%s.json" % ( cf.output_dir, group_name )

    # Open it for writing.
    fd_oufi = open(oufig, 'w' )

    # Write result in output file.
    for line in json.dumps ( json_meta_group, sort_keys=True, indent=4 ):

      fd_oufi.write ( line )

    fd_oufi.write ('\n')

def populate ( json_meta_group ):
    """
    Add members to meta groups regarding hard defined 
    lists in config.py module.
    """

    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__populate__' )
    logger = logging.getLogger( ls )

    # Extract meta group name info ie ENV.
    for k in json_meta_group.keys():

       meta_group = k

    # Retrieve meta_group list from config module.
    string_list = "cf.%s" % ( meta_group )
    list = eval( string_list ) 
    
    # Add every members as children in JSON.
    index = 0
    for index in range( len( list ) ):

      json_meta_group[meta_group]['children'].append( list[index] )
