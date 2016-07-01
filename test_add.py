import threading 

addlock = threading.Lock()
def test_addition(num):
  addlock.acquire()
  num = num + 10
  addlock.release()
  return num

