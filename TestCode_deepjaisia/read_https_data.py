import httplib

def fetch_https_data(url_of_website):
  conn = httplib.HTTPSConnection(url_of_website)
  conn.request("GET", "/")
  conn_response = conn.getresponse()
  return conn_response.read()

https_data = fetch_https_data('www.google.com')
print https_data