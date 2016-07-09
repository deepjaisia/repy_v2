import httplib
import ssl
from encodings import __init__

httplib.getattr = getattr
ssl.getattr = getattr

httplib.hasattr = hasattr
#__init__.getattr = getattr

def getStatusOfWebsite(urlOfWebsite):

  conn = httplib.HTTPSConnection(urlOfWebsite)
  conn.request("GET", "/index.html")
  responseToRequest = conn.getresponse()
  return responseToRequest.status, responseToRequest.reason

