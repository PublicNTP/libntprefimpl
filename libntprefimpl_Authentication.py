#!/usr/bin/python3

from __future__ import print_function

class NtpReferenceImplmentation_Authentication:

  _knownAuthTypes = {
    'md5'
  }

  def __init__(self, server):
    self._server = server
    self._auth = None

  def setAuth(self, authType, authKeyId, authPassword):
    if authType not in self._knownAuthTypes:
      raise RuntimeError("Unknown auth type: {0}".format(authType))

    self._auth = {
      'type'      : authType,
      'keyId'     : authKeyId,
      'password'  : authPassword
    }

  def getAuth(self, field=None):
    if self._auth is None:
      return None

    if field is None:
      return self._auth
    
    if field not in self._auth:
      raise RuntimeError("Unknown auth field: {0}".format(field))

    return self._auth[field]
