#!/usr/bin/python3


from __future__ import print_function
import pprint


class NtpReferenceImplementation_Authentication:
  """Authentication information required for priviliged operations.

  Retains the information about authentication type, key ID, and 
  password which is required for certain priviliged queries to an
  NTP Reference Implementation server.
  
  """

  #: Supported server authentication types
  _knownAuthTypes = [
    'md5'
  ]

  AUTH_TYPE_MD5 = _knownAuthTypes[0] #: Authentication type of "md5"

  def __init__(self, serverHostname):
    """Create new authentication object. 

    Arguments:
    ----------
    serverHostname : str
      Hostname or IP of the server
     
    """
    self._auth = None
    self._serverName = serverHostname


  def __repr__(self):
    """String representation of the object. """
    if self._auth is not None:
      authString = pprint.pformat(self._auth)
    else:
      authString = "(not set)"

    return "NtpReferenceImplementation_Authentication(hostname=\"{0}\", auth={1})".format(
      self._serverName, authString)


  def setAuth(self, authType, authKeyId, authPassword):
    """Set authentication information for this server.

    Arguments:
    ----------
    authType : str
      Type of authentication info (e.g., AUTH_TYPE_MD5)
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


  def getAuth(self):
    """Retrieve all authentication info for this server.

    Returns:
    --------
    :obj:`dict` or None
      If authentication info has not been set, returns None.
      Else, returns dictionary with structure:
      { 
        "type": "md5",
        "keyId": <int>,
        "password": <str>
      }

    """
    if self._auth is None:
      return None

    return self._auth


  def _getAuthField(self, authField):
    """ Get one auth field

    Arguments:
    ----------
    authFieldIndex : str
      Valid key in `self._auth`

    Returns:
    --------
    None or requested field
      If auth has been set, returns specified field, else none

    """
    if self._auth is not None:
      return self._auth[ authField ]
    else:
      return None


  def getAuthType(self):
    """ Get the authentication type set for this server

    Returns:
    --------
      str or None
        Returns authentication type if set, else None

    """
    return self._getAuthField('type')


  def getAuthKeyId(self):
    """ Get the authentication key ID set for this server

    Returns:
    --------
      int or None
        Returns authentication key id if set, else None

    """
    return self._getAuthField('keyId')


  def getAuthPassword(self):
    """ Get the authentication password set for this server

    Returns:
    --------
      str or None
        Returns authentication password if set, else None

    """
    return self._getAuthField('password')
