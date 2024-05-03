import machine
import time
import pdc6x1

cs = machine.Pin('X5', mode=machine.Pin.OUT, value=1)
wr = machine.Pin('X6', mode=machine.Pin.OUT, value=1)
data = machine.Pin('X8', mode=machine.Pin.OUT, value=1)

lcd = pdc6x1.HT1621(cs, wr, data)
lcd.clear()
lcd.battery(3) # Battery level must be 0, 1, 2 or 3

lcd.print("Error. ")
time.sleep(5)

# The second argument is the number of decimal places.
# Can be 0, 1(default), 2 or 3.
lcd.print(123.456789, 2)
time.sleep(5)

# You need to ensure that your values fit on the display.
#  If you send the number 1234567,
# then 234567 will be printed because it prints from right to left .
for i in range(99999):
    lcd.print(-i)
    
lcd.off()