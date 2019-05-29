import serial
import os, time

port = "COM4"  # Raspberry Pi 2
def parseGPS(data):
    if data.find(b'GGA') > 0:
        s = data.split(b",")
        if s[5] == '0':
            print ("no satellite data available")
            return
        lat = decode(s[2])
        if lat == "null":
            return
        dirLat = s[3]
        lon = decode(s[4])
        dirLon = s[5]
        alt = s[9] + b" m"
        sat = s[7]
        l=s[2]
        lo=s[4]
        new_lat=float(l)
        new_lon=float(lo)
        lat_in_degrees = convert_to_degrees(new_lat)    #get latitude in degree decimal format
        long_in_degrees = convert_to_degrees(new_lon) #get longitude in degree decimal format
        #return 'http://maps.google.com/?q={lat_in_degrees},{long_in_degrees}'
        return 'http://maps.google.com/?q=%s,%s' % (lat_in_degrees,long_in_degrees)

def decode(coord):
    if len(coord) == 0 :
       # print('gps connection lost decode')
        return "null"
    v = coord.split(b".")
    head = v[0]
    tail =  v[1]
    deg = head[0:-2]
    min = head[-2:]
    d=int(deg)
    m=int(min)
    t=int(tail)
    return str(d)+'°'+str(m)+"."+str(t)+"'"

def decimal_degrees(degrees, minutes):
    return float(degrees) + float(minutes)/60 

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position    
def send_msg(message,port):
    numbers = ['9823852573','7083242177','8605787307']
    MyString="AT"+"\r\n"
    #port = serial.Serial("COM4", baudrate=115200, timeout=1)
    print("hello")
    port.write(bytes(MyString, 'UTF-8'))
    rcv = port.read(10)
    print (rcv)
    time.sleep(.1)
    MyString="ATE0"+"\r\n"
    port.write(bytes(MyString, 'UTF-8'))      # Disable the Echo
    rcv = port.read(10)
    print (rcv)
    time.sleep(.1)
    MyString="AT+CMGF=1"+"\r\n"
    port.write(bytes(MyString, 'UTF-8'))  # Select Message format as Text mode
    rcv = port.read(10)
    print (rcv)
    time.sleep(.1)
    MyString="AT+CNMI=2,1,0,0,0"+"\r\n"
    port.write(bytes(MyString, 'UTF-8'))   # New SMS Message Indications
    rcv = port.read(10)
    print (rcv)
    time.sleep(.1)
    for i in numbers:
        
        recipient=i
        content=message
        MyString='''AT+CMGS="''' +recipient + '''"\r\n'''
        port.write(bytes(MyString,'UTF-8'))
        time.sleep(1)
        MyString=content + "\r\n"
        port.write(bytes(MyString,'UTF-8')) 
        rcv = port.read(10)
        print (rcv)
        port.write(bytes("\x1A",'UTF-8')) # Enable to send SMS
        for i in range(10):
            rcv = port.read(10)
            print (rcv)
        time.sleep(3)

def gps_driver():
    check=0
    ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
    MyString='AT'+'\r\n'
    ser.write(bytes(MyString,'UTF-8'))            
    rcv = ser.read(100)
    print(rcv)
    time.sleep(.1)
    MyString='AT+CGNSPWR=1'+'\r\n'
    ser.write(bytes(MyString,'UTF-8'))             # to power the GPS
    rcv = ser.read(100)
    print(rcv)
    time.sleep(.1)
    MyString='AT+CGNSIPR=115200'+'\r\n'
    ser.write(bytes(MyString,'UTF-8')) # Set the baud rate of GPS
    rcv = ser.read(100)
    print(rcv)
    time.sleep(.1)
    MyString='AT+CGNSTST=1'+'\r\n'
    ser.write(bytes(MyString,'UTF-8'))    # Send data received to UART
    rcv = ser.read(100)
    print(rcv)
    time.sleep(.1)
    MyString="'AT+CGNSINF'+'\r\n'"
    ser.write(bytes(MyString,'UTF-8'))       # Print the GPS information
    i=0;
    flag=1;
    while i<40:
        data = ser.readline()
        link= parseGPS(data)
        #print(link)
        if link == None :
            check+=1
           
        if flag==1 and link:
            print(link)
            MyString='AT+CGNSTST=0'+'\r\n'
            ser.write(bytes(MyString,'UTF-8'))    # Send data received to UART
            rcv = ser.read(100)
            print("sending to func")
            send_msg(link,ser)
            flag+=1
        i+=1
    if check!=0 and flag==1:
        print('gps connection lost decode')
#Serial4.py
#Displaying Serial4.py.
gps_driver()        

