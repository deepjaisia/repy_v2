#pragma repy
#from exception_hierarchy import RepyException

new_dict = [['seattle.poly.edu', '/', 'server.crt', True], ['www.google.com','/','server.crt', False]]
#new_dict = {1 : {1:'seattle.poly.edu', 2:'/', 3:'', 4: False},
#            2 : {1:'www.google.com', 2:'/', 3:'', 4: True}}

#a = new_dict[1][1]
#log('a')           

for i in range(len(new_dict)):
  try:
    httpsget(new_dict[i][0],new_dict[i][1],new_dict[i][2],new_dict[i][3])
    #httpsget('seattle.poly.edu', '/', '', True)
  except Exception:
    log('Error caught at: ', i, '\n')