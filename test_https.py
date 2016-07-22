import httplib
import ssl
import encodings
from encodings import ascii

#httplib.getattr = getattr
ssl.getattr = getattr

encodings.hasattr = hasattr

#def main():

  #status_of_website = get_status_of_website()
  
def get_status_of_website(url_of_website):

  conn = httplib.HTTPSConnection(url_of_website)
  conn.request("GET", "/")
  response_to_request = conn.getresponse()
  return response_to_request.reason
  #response_to_request.status, 

#if __name__ == '__main__':
  #main()