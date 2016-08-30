import httplib
import ssl
import encodings
import encodings.ascii
import re
import hashlib
import sre_compile
import threading

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

  def __init__(self):

    print "The SSL Certificate that you have might not be correct. Please try again with the correct one."
  

def cert_verifier(url_of_website, port_number):
  
  cert_from_server = ssl.get_server_certificate((url_of_website, port_number))
  cert_from_server = str(cert_from_server)
  with open('server.crt', 'r') as certfile:
    cert_with_client = certfile.read().replace('/n', '')
  cert_with_client = str(cert_with_client)
  server_cert_hash = hashlib.sha512(cert_from_server)
  client_cert_hash = hashlib.sha512(cert_with_client)
  return cmp(server_cert_hash.digest(), client_cert_hash.digest())
  #return 1

def get_status_of_website(url_of_website, port_number, method_used, web_page, ssl_flag):

############################################################################
## url_of_website : Is used to give the url of the website.               ##
## port_number : Set to '443' for using "https".                          ##
## web_page : Go to a specific webpage within the website server,         ##
##            leave blank or put "/" if no webpage.                       ##
## method_used : Method can be POST, GET or PUT. Depends on the user.     ## 
## ssl_flag : Set ssl_flag == True if the user wants to trust self-signed ##
##            certificate of the webserver else select ssl_flag == False  ##
##            if the user doesn't trust the certificate of the webserver  ##
##            and wants the certificate to be verified.                   ##
############################################################################

  if ssl_flag == True:
    try:
      cert_verification = cert_verifier(url_of_website, port_number)
      if cert_verification == 0:
        context = ssl._create_unverified_context()
        conn = httplib.HTTPSConnection(url_of_website, port_number, context=context)
        conn.request(method_used, web_page)
        response_to_request = conn.getresponse()
        return response_to_request.status, response_to_request.read()
    
      else:
        raise SSLError  
        #cert_not_verified = 34404
        #try_again = 'Please Try Again with a valid certificate'
        #return cert_not_verified, try_again

    except SSLError:
      print "SSL Certificate not correct, please try again with a valid certificate"
      return 1, "hello"
  
  else:
    conn = httplib.HTTPSConnection(url_of_website, port_number)
    conn.request(method_used, web_page)
    response_to_request = conn.getresponse()
    return response_to_request.status, response_to_request.read()

#if __name__ == '__main__':
  #main()