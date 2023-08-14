#this code reads data from an arduino photoresistor and prints value to the terminal every one second
from pyfirmata import Arduino,util
import time
board = Arduino('COM26')
analog_input = board.get_pin('a:0:i')

it = util.Iterator(board)
it.start()
while True:
  
    analog_value = analog_input.read()
    print(analog_value)
    time.sleep(1)



#led = board.get_pin('d:8:o') 
