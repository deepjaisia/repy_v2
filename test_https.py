import httplib

def getStatusOfWebsite(urlOfWebsite):
  
  conn = httplib.HTTPSConnection(urlOfWebsite)
  conn.request("GET", "/index.html")
  responseToRequest = conn.getresponse()
  return responseToRequest.status, responseToRequest.reason

