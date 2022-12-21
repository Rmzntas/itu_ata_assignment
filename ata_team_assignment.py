from dronekit import connect, VehicleMode, LocationGlobalRelative
import cv2
import time
import math
import pymavlink
import datetime


class PLANE():
    def __init__(self,connection_address):
        self.plane=connect(connection_address,wait_ready=True)
        if self.plane:
            print("Connection is successful")
        
    def arm_takeoff(self):   # arming and starting mission

        print("Basic pre-arm checks")


        while not self.plane.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)
        
        print("Arming motors")
       
        self.plane.arm(wait=True)
        if self.plane.armed:
            print ("plane has armed!!!")  


        self.plane.mode = VehicleMode("AUTO")

        print("Taking off!")
        
    def takeCommands(self):     # commands from mission planner
        cmds=self.plane.commands
        cmds.download()
        cmds.wait_ready()
        if cmds:
            print("Commands were taken!")
    
    def flightlogs(self): 
       
        self.file=open('flightlogs.txt','a')
        
        now=datetime.datetime.now()

        self.file.write("Time: %s\n" % now)
        self.file.write("Airspeed: %s m/s\n" % self.plane.airspeed)
        self.file.write("Euler Angels: %s\n" % self.plane.attitude)
        self.file.write("Relative Altitude: %s\n" % self.plane.location.global_relative_frame.alt)
        self.file.write("Longitute: %s\n" %self.plane.location.global_relative_frame.lon)
        self.file.write("Latitude: %s\n\n" % self.plane.location.global_relative_frame.lat)    #1 row space
        self.file.close()

        print ('Time:', now)
        print ('Airspeed:', self.plane.airspeed)
        print ('Euler Angels:' ,self.plane.attitude)
        print ('Realitive Altitude:', self.plane.location.global_relative_frame.alt)
        print ('Longitude', self.plane.location.global_relative_frame.lon)
        print ('Latitude:', self.plane.location.global_relative_frame.lat)



# main


ata=PLANE('tcp:127.0.0.1:5762') 

ata.takeCommands()   

ata.arm_takeoff()      

end=1
kamera=1

while end:
    ata.flightlogs()

    if ata.plane.commands.next==3: #when it is second wp
        
        camera = cv2.VideoCapture(0) 
     
        starting_time = time.time
        
        while True:
            
            ret, video = camera.read()
            cv2.imshow("Bilgisayar Kamerasi", video)
        
            end_time=time.time
            if (end_time-starting_time)>=8:
                camera.release()
                cv2.destroyAllWindows()
                break

    if ata.plane.commands.next==5: 
        print("Returning to Launch")        
        ata.mode = VehicleMode("RTL")

    time.sleep(1)



    
    