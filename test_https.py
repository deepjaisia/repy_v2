import httplib
import ssl
import encodings
from encodings import ascii
import re
import hashlib
import sre_compile
import threading
#from OpenSSL import SSL
#import sys

sre_compile.bytearray = bytearray
sre_compile.bytes = bytes

open = open

re.enumerate = enumerate

encodings.__import__ = __import__
encodings.hasattr = hasattr

httplib.hasattr = hasattr

ssl.getattr = getattr
ssl.delattr = delattr
#context = ssl.create_default_context()

#encodings.isinstance = isinstance

#def main():

  #status_of_website = get_status_of_website()

class SSLError(Exception):

  pass

class SSLFlagError(Exception):

  pass

def cert_verifier(url_of_website, server_certi):
  
  cert_from_server = ssl.get_server_certificate((url_of_website, 443))
  cert_from_server = str(cert_from_server)
  with open(server_certi, 'r') as certfile:
    cert_with_client = certfile.read().replace('/n', '')
  cert_with_client = str(cert_with_client)
  server_cert_hash = hashlib.sha512(cert_from_server)
  client_cert_hash = hashlib.sha512(cert_with_client)
  return cmp(server_cert_hash.digest(), client_cert_hash.digest())
  #return 1

def get_status_of_website(url_of_website, method_used, web_page, server_certi, ssl_flag):

############################################################################
## url_of_website : Is used to give the url of the website.               ##
## web_page : Go to a specific webpage within the website server,         ##
##            leave blank or put "/" if no webpage.                       ##
## method_used : Method can be POST, GET or PUT. Depends on the user.     ## 
## server_certi : This requires the user to save the server's certificate ##
##                in the current directory it's and provide the name of   ##
##                certificate when using the function call                ##
## ssl_flag : Set ssl_flag == True if the user wants to trust self-signed ##
##            certificate of the webserver else select ssl_flag == False  ##
##            if the user doesn't trust the certificate of the webserver  ##
##            and wants the certificate to be verified.                   ##
## Port Number is set to 443 by default for HTTPS Connection.             ##
############################################################################

  if ssl_flag == True:
    try:
      cert_verification = cert_verifier(url_of_website, server_certi)
      if cert_verification == 0:
        context = ssl._create_unverified_context()
        conn = httplib.HTTPSConnection(url_of_website, 443, context=context)
        conn.request(method_used, web_page)
        response_to_request = conn.getresponse()
        return response_to_request.status, response_to_request.read(), list(response_to_request.getheaders())
    
      else:
        raise Exception
        
    except Exception:
      #print "Hello"
      raise SSLError("The certificate you provided is not correct, please try with a valid certificate.")

  else:
    conn = httplib.HTTPSConnection(url_of_website, 443)
    conn.request(method_used, web_page)
    response_to_request = conn.getresponse()
    return response_to_request.status, response_to_request.read(), list(response_to_request.getheaders())

#if __name__ == '__main__':
  #main()