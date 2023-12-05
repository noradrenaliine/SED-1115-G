import machine
import time
piny = machine.ADC(27)
pinx = machine.ADC(26)
yval = 0
xval = 0
DegreeX = 0
DegreeY = 0
def covernt_potentionmeter_to_x(xval):
    convertX = 220/65535
    xval = convertX * DegreeX
    print ("X Coordinate:" + str(xval), end = '\r')

    return xval

def covernt_potentionmeter_to_y(yval):
    convertY = 280/65535
    yval = convertY * DegreeY
    print ("                             Y Coordinate:" + str(yval), end = '\r')

    return yval
def read_potntionmeter(DegreeX,DegreeY):
    while True:
        if pinx.read_u16() > 0:
            DegreeX = pinx.read_u16()
            covernt_potentionmeter_to_x(xval)
            
            time.sleep(0.1)
        if piny.read_u16() > 0:
            DegreeY = piny.read_u16()
            covernt_potentionmeter_to_y(yval)
        return DegreeX,DegreeY


read_potntionmeter(DegreeX,DegreeY)
        
    

    
        







