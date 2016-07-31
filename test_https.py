import httplib
import ssl
import encodings
import encodings.ascii
import re

re.enumerate = enumerate

encodings.__import__ = __import__
encodings.hasattr = hasattr

httplib.hasattr = hasattr

ssl.getattr = getattr
ssl.delattr = delattr

#encodings.isinstance = isinstance

#def main():

  #status_of_website = get_status_of_website()
  
def get_status_of_website(url_of_website):

  conn = httplib.HTTPSConnection(url_of_website)
  conn.request("GET", "/")
  response_to_request = conn.getresponse()
  return response_to_request.reason, response_to_request.read() 

#if __name__ == '__main__':
  #main()