import httplib
import ssl
import encodings
from encodings import ascii
import re
import hashlib
import sre_compile
import threading
import exception_hierarchy
import os
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

############################################################################
## SSLError: This error is raised when the SSL Certificate is not correct ##
##           and the verification fails or the server is not present.     ##
## SSLFlagError: This error is raised when the the function does not      ##
##                receive a proper boolean value.                         ##
## CertiError: This error is raised when the user provides with a value   ##
##              in the certificate field when it meant to be left empty.  ##
## CertiEmptyError: This error is raised when the certificate provided    ##
##                   by the user is not present in the directory.         ##
############################################################################

class SSLError(exception_hierarchy.RepyException):

  pass

class SSLFlagError(exception_hierarchy.RepyException):

  pass

class CertiError(exception_hierarchy.RepyException):

  pass

class CertiEmptyError(exception_hierarchy.RepyException):

  pass

def cert_verifier(url_of_website, server_certi):
  
  try:  
    cert_from_server = str(ssl.get_server_certificate((url_of_website, 443)))
  except Exception:
  	raise SSLError("The server you are looking for is not present.")
  try:
    if not(os.path.exists(server_certi)):
      raise CertiEmptyError("There is no such file present.")    
  except CertiEmptyError as e:
    raise
  with open(server_certi, 'r') as certfile:
    cert_with_client = certfile.read().replace('/n', '')
  cert_with_client = str(cert_with_client)
  server_cert_hash = hashlib.sha512(cert_from_server)
  client_cert_hash = hashlib.sha512(cert_with_client)
  return cmp(server_cert_hash.digest(), client_cert_hash.digest())
  #return 1


def get_status_of_website(url_of_website, web_page, server_certi, ssl_flag):

############################################################################
## url_of_website : Is used to give the url of the website.               ##
## web_page : Go to a specific webpage within the website server,         ##
##            leave blank or put "/" if no webpage.                       ## 
## server_certi : This requires the user to save the server's certificate ##
##                in the current directory it's and provide the name of   ##
##                certificate when using the function call                ##
## ssl_flag : Set ssl_flag == True if the user wants to trust self-signed ##
##            certificate of the webserver else select ssl_flag == False  ##
##            if the user doesn't trust the certificate of the webserver  ##
##            and wants the certificate to be verified.                   ##
##                                                                        ##
## Port Number is set to 443 by default for HTTPS Connection.             ##
## Method used for fetching the information of the websites is set to     ##
## "GET" by default.                                                      ##
############################################################################

  if ssl_flag == True:
    try:
      cert_verification = cert_verifier(url_of_website, server_certi)
      if cert_verification != 0:
        raise SSLError("The certificate you provided is not correct, please try again with the proper certificate.")
      context = ssl._create_unverified_context()
      conn = httplib.HTTPSConnection(url_of_website, 443, context=context)
      conn.request("GET", web_page)
      response_to_request = conn.getresponse()
      return response_to_request.status, response_to_request.read(), response_to_request.getheaders()
     
    except SSLError as e:
      raise

  elif ssl_flag == False:
    try:
      if server_certi:
        raise CertiError("Please leave the certificate field empty in the call.")
      conn = httplib.HTTPSConnection(url_of_website, 443)
      conn.request("GET", web_page)
      response_to_request = conn.getresponse()
      return response_to_request.status, response_to_request.read(), response_to_request.getheaders()

    except CertiError as e:
      raise

  elif ssl_flag != True or False:
    raise SSLFlagError("Improper Boolean Value entered.")