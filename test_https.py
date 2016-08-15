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
#context = ssl.create_default_context()

#encodings.isinstance = isinstance

#def main():

  #status_of_website = get_status_of_website()
  
def get_status_of_website(url_of_website, port_number, method, web_page, ssl_flag):

#############################################################################################################
## url_of_website: Is used to give the url of the website                                                  ##
## port_number: Set to 80 if accessing the website using "http" and set to 443 if using "https"            ##
## web_page: Give the webpage within the the website, leave blank or put "/" if no webpage                 ##
## method: Method can be POST, GET or PUT. Depends on the user.                                            ## 
## ssl_flag: Set ssl_flag == "T" if the user trusts unknown certificate of the party else ssl_flag == "F"  ##
#############################################################################################################

  if ssl_flag == "T":
    context = ssl._create_unverified_context()
    conn = httplib.HTTPSConnection(url_of_website, port_number, context=context)
    conn.request(method, web_page)
    response_to_request = conn.getresponse()
    return response_to_request.status, response_to_request.read()

  else:
    conn = httplib.HTTPSConnection(url_of_website, port_number)
    conn.request(method, web_page)
    response_to_request = conn.getresponse()
    return response_to_request.status, response_to_request.read()

#if __name__ == '__main__':
  #main()