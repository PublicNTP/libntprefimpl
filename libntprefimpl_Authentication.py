#!/usr/bin/python3


from __future__ import print_function


class NtpReferenceImplementation_Authentication:
  """Authentication information required for priviliged operations.

  Retains the information about authentication type, key ID, and 
  password which is required for certain priviliged queries to an
  NTP Reference Implementation server.
  """

  
  # Supported server authentication types
  _knownAuthTypes = [
    'md5'
  ]


  def __init__(self, server):
    """Create new authentication object.

    Arguments:
    ----------
    server : :obj:`NtpReferenceImplementation`
      Reference to the top-level object for the server

    """
    self._server = server
    self._auth = None


  def setAuth(self, authType, authKeyId, authPassword):
    """Set authentication information for this server.

    Arguments:
    ----------
    authType : str
      Type of authentication info (e.g., "md5")
    authKeyId : int
      Which key ID the password pertains to
    authPassword : str
      The password to validate with the server

    Notes:
    ------
    If `authType` is not a supported authentication type, a 
      `RuntimeException` will be thrown

    """
      
    if authType not in self._knownAuthTypes:
      raise RuntimeError("Unknown auth type: {0}".format(authType))

    self._auth = {
      'type'      : authType,
      'keyId'     : authKeyId,
      'password'  : authPassword
    }


  def getAuth(self, field=None):
    """Retrieve the authentication info for this server.

    Arguments:
    ----------
    field : str, optional
      Which portion of authentication info to retrieve. 
 
      Valid values: `type`, `keyId`, `password`

    Returns:
    --------
    str, int, or :obj:`dict`
      If `field` is specified, will return the requested portion of 
      authentication info, else returns the entire dictionary with
      structure:

      { 
        "type": ...,
        "keyId": ...,
        "password": ...
      }

      Notes:
      ------
      If `field` is not one of the three valid values, a
      `RuntimeException` will be thrown.

    """
    if self._auth is None:
      return None

    if field is None:
      return self._auth
    
    if field not in self._auth:
      raise RuntimeError("Unknown auth field: {0}".format(field))

    return self._auth[field]
