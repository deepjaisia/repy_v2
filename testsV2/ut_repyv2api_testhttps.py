#pragma repy
#from exception_hierarchy import RepyException

new_dict = [['seattle.poly.edu', '/', '', False], ['www.google.com','/','', False], 
            ['localhost','/','server.crt', True], ['localhost','/test_https.py.zip', 'server.crt', True],
            ['localhost', '/test_https.py', 'server1.crt', True], ['localhost', '/test_http.py', 'server.crt', True],
            ['localhst', '/test_https.py', 'server.crt', True]]		

for i in range(len(new_dict)):
  try:
    httpsget(new_dict[i][0],new_dict[i][1],new_dict[i][2],new_dict[i][3])
    #httpsget('seattle.poly.edu', '/', '', True)
  except Exception:
    log('Error caught at index position: ', i, '\n')