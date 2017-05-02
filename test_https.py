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
import socket
import OpenSSL
from OpenSSL import crypto
#import sys

sre_compile.bytearray = bytearray
sre_compile.bytes = bytes

crypto.__import__ = __import__

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

class ServerError(exception_hierarchy.RepyException):

  pass


def cert_verifier(url_of_website, port_number, server_certi):
  
  #Checks if the server is listening or not. if not listening an error is raised.
  try:  
    cert_from_server = ssl.get_server_certificate((url_of_website, port_number))
    cert_from_server_str = str(cert_from_server)
  except socket.error as (err_no,err_msg):
    if err_no == 111:
      raise ServerError(err_msg + ", check if the server with specified 'Port Number' is running properly or not.")

  #Checks if the certificate provided by the user is present or not. If not raise an error is raised.
  try:
    if not(os.path.exists(server_certi)):
      raise CertiEmptyError("There is no such certificate present, check directory again for self-signed certificate.")    
  except CertiEmptyError as e:
    raise

  #Checks Server Certficate if it has been expired or not
  x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_from_server)
  cert_verifier_param1 = x509.has_expired()

  cert_verifier_param1 = True

  #Opens the server certificate provided by user and compares it byte by byte to the certificate fetched from the server. 
  with open(server_certi, 'r') as certfile:
    cert_with_client = certfile.read().replace('/n', '')
  cert_with_client = str(cert_with_client)
  server_cert_hash = hashlib.sha512(cert_from_server_str)
  client_cert_hash = hashlib.sha512(cert_with_client)
  cert_verifier_param2 = cmp(server_cert_hash.digest(), client_cert_hash.digest())
  
  if cert_verifier_param1 == True:
    raise CertiError("The certificate received from the server has been expired")
  elif cert_verifier_param2 != 0:
    raise CertiError("The certificate received from the server and provided do not match, please try again.")
  else:
    return
  #return 1


def get_status_of_website(url_of_website, web_page, port_number, server_certi, ssl_flag):

############################################################################
## url_of_website : Is used to give the url of the website.               ##
## web_page : Go to a specific webpage within the website server,         ##
##            leave blank or put "/" if no webpage.                       ## 
## server_certi : This requires the user to save the server's certificate ##
##                in the current directory it's and provide the name of   ##
##                certificate when using the function call                ##
## port_number : Specify the port number to connect to, pass "0" if       ##
##               you don't want to pass port number. Default set to 443   ##
## ssl_flag : Set ssl_flag == True if the user wants to trust self-signed ##
##            certificate of the webserver else select ssl_flag == False  ##
##            if the user doesn't trust the certificate of the webserver  ##
##            and wants the certificate to be verified.                   ##
##                                                                        ##
## Method used for fetching the information of the websites is set to     ##
## "GET" by default.                                                      ##
############################################################################

  if port_number == 0:
  	port_number = 443
  
  try:
    if ssl_flag == True:
      cert_verifier(url_of_website, port_number, server_certi)
      context = ssl._create_unverified_context()
      conn = httplib.HTTPSConnection(url_of_website, port_number, context=context)
    elif ssl_flag == False:
      if server_certi:
        raise CertiError("Please leave the certificate field empty in the call.")	
      conn = httplib.HTTPSConnection(url_of_website, port_number)

    conn.request("GET", web_page)
    response_to_request = conn.getresponse()
    return response_to_request.status, response_to_request.read(), response_to_request.getheaders()
     
  except SSLError:
    raise
  except CertiError:
    raise
  except socket.gaierror as (err_no, err_msg):
    if err_no == -2:
      raise SSLError(err_msg)
  except ssl.SSLError as (err_no, err_msg):
    if err_no == 1:
      #raise CertiError(err_msg)
      raise CertiError("Certificate verification failed.")
  except ssl.CertificateError as (err_msg, err_1):
    raise CertiError(err_msg)