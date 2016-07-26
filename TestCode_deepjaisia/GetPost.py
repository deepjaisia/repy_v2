import httplib, urllib
mydata={"u_id": "12524","u_pass": "issue"}
params = urllib.urlencode(mydata)
#headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#path='http://localhost/Research/index.html'
conn = httplib.HTTPConnection("localhost",7070)
conn.request("POST", "/Research/index.html", params)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print data
conn.close()