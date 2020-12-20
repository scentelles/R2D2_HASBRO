#!/usr/bin/env python3
from bluepy import btle
import time
import threading
import sys
from threading import Timer


ledThreads = {}
MAC_ADDRESS_R2D2 = "c8:01:d5:69:5e:a4"

Service_UUID         = "dab91435-b5a1-e29c-b041-bcd562613be4"
Characteristic_UUID  = "dab91383-b5a1-e29c-b041-bcd562613be4"
                       
Service1_UUID        = "dab91435-b5a1-e29c-b041-bcd562613be4"
Characteristic1_UUID = "dab91382-b5a1-e29c-b041-bcd562613be4"

ACTION00 = 0x09
ACTION23 = 0x0A

ACTION21 = 0x04 #whistle love
ACTION22 = 0x05
#06 sympa
ACTION24 = 0x0C
ACTION25 = 0x0D
ACTION01 = 0x15
ACTION02 = 0x16
ACTION03 = 0x17
ACTION04 = 0x18
ACTION05 = 0x19
ACTION06 = 0x1A
ACTION07 = 0x1B
ACTION08 = 0x1C
ACTION09 = 0x1D

ACTION10 = 0x1F

ACTION11 = 0x29

ACTION12 = 0x2B
ACTION13 = 0x2C

ACTION14 = 0x2E

ACTION15 = 0x30

ACTION16 = 0x32

ACTION17 = 0x34

ACTION18 = 0xD9
ACTION19 = 0xCF

DANSE1   = 0xCA # => danse cantina
DANSE2   = 0xC5

ACTION20 = 0xC9



ACTION26 = 0x20
ACTION27 = 0x22
ACTION28 = 0x23



class MonThread (threading.Thread):
    def __init__(self, macAddress, name):     
        threading.Thread.__init__(self) 
        print(macAddress)
        self.macAddress = macAddress
        self.connected = 0

        self.dev = 0
        self.service = 0
        self.char = 0


        self.name = name


    #===========  Moves and actions   
    def turnHeadLeft(self):
            self.char.write(bytes([0x13,0x2]))

    def turnHeadRight(self):
            self.char.write(bytes([0x13,0x1]))

    def triggerAction(self,Id):
            self.char.write(bytes([0x17,0x02,Id,0x01]))
	
    def turnRight(self,duration):
            self.char.write(bytes([0x12,0x02,0x06]))
            self.char.write(bytes([0x14,0x01]))
            time.sleep(duration)
            self.char.write(bytes([0x18,0x14]))

    def turnLeft(self,duration):
            self.char.write(bytes([0x12,0x02,0x08]))
            self.char.write(bytes([0x14,0x01]))
            time.sleep(duration)
            self.char.write(bytes([0x18,0x14]))

    def moveFwd(self,duration):
            self.char.write(bytes([0x12,0x02,0x07]))
            self.char.write(bytes([0x14,0x01]))
            time.sleep(duration)
            self.char.write(bytes([0x18,0x1C]))

    def moveBkwd(self,duration):
            self.char.write(bytes([0x12,0x02,0x07]))
            self.char.write(bytes([0x14,0x02]))
            time.sleep(duration)
            self.char.write(bytes([0x18,0x1C]))


    #============  Connection

    def connect(self):
                    print("trying to connect to " + self.name)
                    try:
                        self.dev = btle.Peripheral(self.macAddress, btle.ADDR_TYPE_RANDOM)
                        print("Connecting to device")

                        self.service = self.dev.getServiceByUUID(Service_UUID)
                        self.char = self.service.getCharacteristics(Characteristic_UUID)[0]  


                        self.connected = 1
                        print("Connected successfully to " + self.name)
                    except:
                        print ("connection failed")
                        self.connected = 0  
		


    #=================== Main action loop. Update here for custom behavior    
    def run(self):
 
        if (self.connected == 0):
            self.connect()

        while 1:
            if (self.connected):

                    try:	
                        time.sleep(2)
			
                        self.turnHeadLeft()
                        time.sleep(4)
                        self.turnHeadRight()	
                        time.sleep(4)
                        self.moveFwd(4)
                        self.triggerAction(DANSE1)	
                        time.sleep(10)
                        self.turnRight(4)				
			
                    except Exception as e:
                        print("DISCONNECTED!!!!!!!")
                        print('Exception : Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                        exit()

                        self.connected = 0
                        self.connect()
                        time.sleep(1)



#=============================================================
#       MAIN PROGRAM
#=============================================================


#define and start thread triggering R2D2 actions
m = MonThread(MAC_ADDRESS_R2D2, "R2D2") 
m.start()                  


while(1):

    if(m.connected):
        try:	
            #Send this command periodically to keep connection with R2D2
            m.char.write(bytes([0x50,0x8D]))
            time.sleep(1)
            print ("R2D2, please do not disconnect!")
	  
        except Exception as e:
            print("DISCONNECTED!!!!!!!")
            print('Exception : Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            m.connected = 0
            m.connect()
            time.sleep(1)

	


