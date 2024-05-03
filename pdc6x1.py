''' Micropython driver v.1.0 for module PDC-6X1
    with controller ht1621 by https://github.com/chicory-ru/PDC-6X1_HT1621
'''

BIAS      = const(0x52)
SYS_DIS   = const(0x00)
SYS_EN    = const(0x02)
LCD_OFF   = const(0x04)
LCD_ON    = const(0x06)
RC256     = const(0x30)

COMMAND   = const(0x800)
WRITE     = const(0x14000)

abc = {'0':0x7D, '1':0x60, '2':0x3e, '3':0x7a, '4':0x63, '5':0x5b, '6':0x5f, 
       '7':0x70, '8':0x7f, '9':0x7b, 'A':0x77, 'B':0x4f, 'C':0x1d, 'D':0x6e,
       'E':0x1f, 'F':0x17, 'G':0x5d, 'H':0x47, 'I':0x05, 'J':0x68, 'K':0x27,
       'L':0x0d, 'M':0x54, 'N':0x75, 'O':0x4e, 'P':0x37, 'Q':0x73, 'R':0x06,
       'S':0x59, 'T':0x0f, 'U':0x6d, 'V':0x23, 'W':0x29, 'X':0x67, 'Y':0x6b,
       'Z':0x3c, '-':0x02, '.':0x80, '_':0x08, 'º':0x33, ' ':0x00}

class HT1621():
    def __init__(self, cs, wr, data):
        self.cs = cs
        self.wr = wr
        self.data = data
        self.bat = 0
        self.init()
    
    def init(self):
        for data in (SYS_EN, RC256, BIAS, LCD_ON):
            self.__data(COMMAND | data)
    
    def __data(self, data):
        self.cs(0)
        for num, i in enumerate(bin(data)):
            if num < 2:
                continue
            self.wr(0)
            self.data(int(i))
            self.wr(1)
        self.cs(1)
    
    def on(self):
        self.__data(COMMAND | LCD_ON)
    
    def off(self):
        self.__data(COMMAND | LCD_OFF)
    
    def battery(self, level:int) -> None:
        if 0 <= level <= 3 and type(level) is int: 
            self.bat = 0x400 + level*0x200
        else:
            self.print("Error ")
            raise Exception("Battery level must be 0, 1, 2 or 3")
     
    def print(self, num:int|float|str, decimal_places:int=1) -> None:
        
        if isinstance(num, float):
            if decimal_places < 0 or decimal_places > 3 or \
                                            type(decimal_places) is not int:
                self.print("Error ")
                raise Exception("The second argument can be 0, 1, 2 or 3")
            num = float(round(num, decimal_places))
            text = ''.join(reversed(f'      {num:.{decimal_places}f}')).upper()
        else:
            text = ''.join(reversed(f'      {num}')).upper()
        
        address = 0x000
        n = 0
        for n, i in enumerate(text):
            if i == '.':
                continue
            if len(text) > n+1 and text[n+1] == '.' and address < 0x600 or \
                                    address >= 0x600 and address <= self.bat:
                self.__data(WRITE | address | abc[i] | abc['.'])
            else:
                self.__data(WRITE | address | abc[i])
            if address == 0xa00:
                return
            address += 0x200

    def clear(self):
        self.__data(0x140000000000000)
         