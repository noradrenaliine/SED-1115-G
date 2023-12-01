import math
def get_angles (cx,cy):
    
    ax = -50
    ay = 139.5
    la = 155
    lb = 155

    ac = math.sqrt( ((ax - cx)**2) + ((ay - cy)**2) )
    abase_c = math.sqrt(((ax - cx)**2) + cy**2)
    Abac = math.acos((la**2 + ac**2 - lb**2) / (2 * la * ac))  
    Aacb = math.asin((la * math.sin(Abac) / (lb)))
    Ayac = math.acos((ay**2 + ac**2 - abase_c**2) / (2*ay*ac))

    alpha = math.degrees(Abac + Ayac)
    beta = math.degrees(Abac + Aacb)
    
    return (alpha,beta)

'''
cx = 148.6
cy = 81.5

test = IK (cx, cy)
print (test)
'''