import config as cf
import requests

def thin( url_base ):
    """
    Make API call to Satellite v6.
    API endpoint hard coded with api/v2/hosts.
    Call hosts API with thin option for speed.
    Return a tuple with ret code and content.
    Return code hard set to 99 if empty after call.
    Content may be the error message returned by API
    or by used python modules such as requests...
    """

    # Contruct url API endpoint
    endpoint = cf.endpoint

    # Define specific parameters to pass to
    parameters = {
                   "thin": "true",
                   "per_page": 20000
                 } 
    # Make the call and handle exceptions.
    try:

      r = requests.get( url_base + endpoint, \
                        auth=(cf.sat_user,cf.sat_pass), \
                        verify=False, \
                        timeout = 5, \
                        params=parameters)

      # Get return code if any.
      rc = r.status_code

      # Store provided JSON only if ret code is 200
      if rc == 200:
        response = r.json()

      else:

        # Get modules error message
        r.raise_for_status()

    # Errors handlings for common types
    except ( requests.ConnectionError, \
             requests.URLRequired, \
             requests.HTTPError, \
             requests.Timeout ) as e:

      # First take care of return code.
      # Test it to be sure that's filled.
      try:

        rc

      except NameError:

        rc = 99
      
      # Then response should contain exception message
      response = e
 
    # Return both return code and response as a tuple
    return ( rc, response )

def details( url_base , hostid ):
    """
    Make API call to Satellite v6.
    Arguments are URL and  Satellite host ID as a string.
    API endpoint hard coded with api/v2/hosts/<id>.
    Return a tuple with ret code and content.
    Return code hard set to 99 if empty after call.
    Content may be the error message returned by API
    or by used python modules such as requests...
    """

    # Contruct url API endpoint
    endpoint = "%s/%s" % ( cf.endpoint, hostid )

    # Define specific parameters to pass to
    parameters = {
                   "per_page": 20000
                 } 
    # Make the call and handle exceptions.
    try:

      r = requests.get( url_base + endpoint, \
                        auth=(cf.sat_user,cf.sat_pass), \
                        verify=False, \
                        timeout = 5, \
                        params=parameters)

      # Get return code if any.
      rc = r.status_code

      # Store provided JSON only if ret code is 200
      if rc == 200:
        response = r.json()

      else:

        # Get modules error message
        r.raise_for_status()

    # Errors handlings for common types
    except ( requests.ConnectionError, \
             requests.URLRequired, \
             requests.HTTPError, \
             requests.Timeout ) as e:

      # First take care of return code.
      # Test it to be sure that's filled.
      try:

        rc

      except NameError:

        rc = 99
      
      # Then response should contain exception message
      response = e
 
    # Return both return code and response as a tuple
    return ( rc, response )
