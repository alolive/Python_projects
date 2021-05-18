import config as cf
import logging,json,os,re

def bunch( fqdn ):
    """
    Arg is host FQDN. Function will first query DNS for IP.
    Satellite bunch facts files may also be use to retrieve
    IP from. 
    Return retcode and ansible_host JSON facts as a tuple.
    """
  
    # Set name of logger with calling details.
    ls = "%s by %s" % ( __name__ , '__bunch__' )
    logger = logging.getLogger( ls )

    try:

      # Open SJSON as a database.
      infis = "%s/%s.sjson" % (cf.input_dir , fqdn )
      fd_infi = open( infis , 'r' )
      sjson_host = json.loads( fd_infi.read() )

      # Query DNS first.
      MyAH = dnsquery ( fqdn )

      # Retrieve if void directly from ip list in sjon file.
      if ( MyAH == None ):

         MyAH = IPtopo ( fqdn, sjson_host )

      icmp = ICMPcheck ( MyAH )
      if ( icmp != 0 ):
  
        # log ping default on ansible_host value...
        string = "ansible_host ( %s ) not pinging for host %s" % ( MyAH, fqdn )
        logger.error( string )

      MyAHFactsVars = { "ansible_ssh_host" : MyAH }
      MyAHFacts = { fqdn : MyAHFactsVars }
      rc = 0

    except IOError as err:

      # File not found so time to log issue.
      string = "Error during ansible_host evaluation phase for below host."
      logger.error( string )
      logger.error( err )
      rc = 1
      MyAHFacts = {}
   
    return (rc, MyAHFacts)

def dnsquery( fqdn ):
    """
    First args is host FQDN.  Algorithm is based on DNS as
    a primary source. If FQDN does not contain "caisse-epargne.fr"
    then query for an admin DNS host entry with form "a-".
    Please note exception for bunker box belonging to dom103 as
    admin access have to be done through dom101 DNS resolution...
    Else issue a query on straight FQDN.
    Return a string.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__dnsquery__' )
    logger = logging.getLogger( ls )

    # DNS retrieve we'll be ensure with dig.
    cmd_to_query = "/usr/bin/dig +short"

    # Determine wheter or not we belong to caisse-epargne.
    if ( re.search( "caisse-epargne.fr", fqdn ) ):
 
      ans_host = fqdn 

    elif ( re.search( "dom103" , fqdn ) ):
     
      # Take care of bunker also...
      ans_host1 = re.sub( "dom103", "dom101", fqdn )
      ans_host = "a-%s" % ( ans_host1 )

    else:

      ans_host = "a-%s" % ( fqdn )

    # Query and read output !
    string = "%s %s" % ( cmd_to_query, ans_host )
    dnsquery = os.popen ( string ).read()

    # If query result is void, set ansible_host to none.
    # And log it as an issue...
    if ( dnsquery == "" ):

      string = "Empty DNS reply for %s" % ( ans_host )
      logger.warning( string )
      ans_host = None

    return ans_host

def IPtopo ( fqdn, json_host ):
    """
    First args is host FQDN. Second is per host satellite JSON.
    Function will evaluate the "best" ip to be flagged as
    ansible_host depending on network topology best practices.
    Will first search for something starting with 114, then
    search for 113 starting and finally return first found
    if no match in list.
    Should be called only if DNS reply's void.
    """

    # Set name of logger with calling details
    ls = "%s by %s" % ( __name__ , '__IPtopo__' )
    logger = logging.getLogger( ls )

    # Set not found as default.
    found = 0

    # Full sat ip list browse.
    for index in range ( len ( json_host[fqdn]['ip_address'] ) ):
   
      ip = json_host[fqdn]['ip_address'][index]
      if ( re.search ( '^114', ip ) ):
     
        # We found something starting with 114.
        found = 1
        IPtopo = ip
  
      elif ( re.search ( '^113', ip ) ):

    
        # We found something starting with 113.
        found = 1
        IPtopo = ip

    # Did we find something nice ?
    if ( found == 0 ):

      try :

        # We'll get the first IP of list except if it's
        # a bunker one ie starting with 192.168...
        # If bunker switch to second list entry !

        IPtopo = json_host[fqdn]['ip_address'][0]
        if ( re.search ( '^192.168', IPtopo ) ):

          IPtopo = json_host[fqdn]['ip_address'][1]

      except:

        # Not even an IP in satellite list. Throw a
        # critical flag in log as we can not determine
        # ansible_host...
        string = "Empty IP ansible_host for %s" % ( fqdn )
        logger.critical( string )
        IPtopo = None

    return IPtopo

def ICMPcheck ( ansible_host ):
    """
    First args is hostname or IP we want to check ICMP.
    Return a boolean. 0 will mean true.
    """

    # Just ping and get return code !
    cmd_to_query = "/usr/bin/ping -c1 -w 1 -W 1"
    cmd_redirection = "> /dev/null 2>&1"
    string = "%s %s %s" % ( cmd_to_query, ansible_host, cmd_redirection )
    ICMPcheck = os.system( string )

    return ICMPcheck

def SSHcheck ( ansible_host ):
    """
    First args is hostname or IP we want to ensure that almost
    ssh remote 22 port is alive.
    Return a boolean.
    """
  
    # Not yet implemented.

    return SSHcheck
