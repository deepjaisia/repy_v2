# _*_ coding:utf-8 _*_

import httplib
import ssl
from encodings import __init__

#httplib.getattr = getattr
ssl.getattr = getattr

hasattr = hasattr
#__init__.getattr = getattr

def main():

  status_of_website = get_status_of_website()
  
def get_status_of_website(url_of_website):

  conn = httplib.HTTPSConnection(url_of_website)
  conn.request("GET", "/")
  response_to_request = conn.getresponse()
  return response_to_request.status, response_to_request.reason

if __name__ == '__main__':
  main()