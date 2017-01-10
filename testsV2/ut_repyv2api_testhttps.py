#pragma repy
#pragma error

new_dict = {1 : {1:'seattle.poly.edu', 2:'/', 3:'', 4: False},
            2 : {1:'www.google.com', 2:'/', 3:'', 4: True}}

#a = new_dict[1][1]
#log('a')           

for i in new_dict:
  try:
    httpsget(new_dict[i][1],new_dict[i][2],new_dict[i][3],new_dict[i][4])
    #httpsget('seattle.poly.edu', '/', '', True)
    pass
  except error:
    log('Error caught')