#!/usr/bin/python

import cv2
from time import sleep, time, time
import time
import datetime
import PIL.Image
import os
from sys import exit
import numpy as np

####### package for threading
import threading

####### copy files
#from shutil import copyfile
import shutil

import tifffile as tiff
from tifffile import imsave

#global no_flats
#global no_darks
#global tomo_reps
no_flats = 10
no_darks = 10

global sample_name_text

def printparam(sample_name_text):
    print(sample_name_text)
 
def Initiate_new_scan(manual_sample_name):

        try:
                localtime = time.localtime(time.time())
                #save the files in the following folder
                global sample_folder_date
                sample_folder_date = str("%04d" % (localtime.tm_year,)) + str("%02d" % (localtime.tm_mon, )) + str("%02d" % (localtime.tm_mday,))
                print(sample_folder_date)

                global sample_folder

                #for Windows
		#path_out = 'C:/Users/emanuel/HBLT_scans/'

		#for Mac
                path_out = '/Users/emanuel/Documents/Python/HBLT_scans/'

                sample_folder = path_out + sample_folder_date + '/' + manual_sample_name + '/' 
                
                print(str(sample_folder))
                
                if not os.path.exists(sample_folder):
                        os.makedirs(sample_folder)

        except KeyboardInterrupt:
                close()
        except:
                print("Error with creating new sample folder! Exiting program.")
                close()

def CamAreaOnThread(x0, xw, y0, yh, cam_no):
        try:
                global t1
                t1 = threading.Thread(name="Hello", target=lambda: CamAreaCheck(x0, xw, y0, yh, cam_no))
                t1.start()
        except KeyboardInterrupt:
                #time.sleep(2)
                #t1.raise_exception() 
                #t1.join()
                close()
        except:
                print("Error with Threading for the web camera! Exiting program!")
                #t1.raise_exception() 
                #t1.join()
                close()

def CamInit(cam_no, x_res, y_res):
        try:
                global cap
                cap = cv2.VideoCapture(cam_no)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, x_res)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, y_res)
                cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

                print("Camera initiated!")
                
        except KeyboardInterrupt:
                close()
        except:
                print("Error with initiating the camera! Exiting program!")
                close()
    
def CamAreaCheck(x0, xw, y0, yh, cam_no):
        try:
                #Initiate web camera
                #set cam no to either 0 or 1 etc. depending on which port the USB or piwebcam is using
                CamInit(cam_no, x_res=720, y_res=480)

                print("camera coordinates", y0,yh,x0,xw)
                print("Is the camera thread on or off?", t1.is_alive())
               
                while(True):
                    # Capture frame-by-frame
                    vret, vframe = cap.read()
                    vframe = vframe[y0:yh, x0:xw]

                    # Our operations on the frame come here.
                    # If used, changes the frame from color to black and white. 
                    #vframe = cv2.cvtColor(vframe, cv2.COLOR_BGR2GRAY)
                    
                    # Display the resulting vframe
                    cv2.imshow('Acquisition Camera',vframe)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                # When everything done, release the capture
                #t1.join()
                #cap.release()
                cv2.destroyAllWindows()
                print("Camera stopped!")
                #t1.join()
                print("Is the camera thread on or off?", t1.is_alive())

        except KeyboardInterrupt:
                close()
        except:
                print("2nd Error with Live view of the camera! Exiting program!")
                close()

def StartScan(x0, xw, y0, yh, no_projs, manual_sample_name):

    """
    Starts the scan with the respective scanning parameters.

    Parameters
    ----------
    x0 : ndarray
        x coordinate
        
    """

    try:

            time_start = datetime.datetime.now()
            
            Initiate_new_scan(manual_sample_name)
            
            #no_projs = 300
            d = 0
            
            print("Starting Tomo scan.")
            
            for i in range(no_projs):

                    # real acquisition
                    retproj, frameproj = cap.read()

                    #crop image                
                    #    frameproj = frameproj[y0:yh, x0:xw]
                    d = d + 1

                    cv2.imwrite(sample_folder + "tomo_%04d" % (d,) + ".tif", frameproj)
                    #print('Acquired projection', i)
                    #sleep(delay)

            time_end = datetime.datetime.now()
            time_total = time_end - time_start
            print("Tomo scanning toke: ")
            print(time_total)
            myDisplay.quit()
            led_onoff_green(ledpower = False)

    except KeyboardInterrupt:
            print("Scan interrupted via Ctrl+C command!")
            close()
    except NameError:
            if sample_folder is None:
                    print("Please create a new sample folder, prior to starting a scan!")

def StartRefScan(x0, xw, y0, yh, no_refs, manual_sample_name):
        try:

                #create new folder
                Initiate_new_scan(manual_sample_name)

                print("Starting Reference scan.")
                
                d = 0
                #no_refs = 20

                for i in range(no_refs):

                        #real acquisition
                        retproj, frameflat = cap.read()

                        #crop image                
                        #frameflat = frameflat[y0:yh, x0:xw]
                        d = d + 1

                        cv2.imwrite(sample_folder + "flat_%04d" % (d,) + ".tif", frameflat)
                        #print('Acquired flat field', i)
                        #sleep(delay)
                
                print("Reference scanning done!")
                
                myDisplay.quit()

        except KeyboardInterrupt:
                print("Scan interrupted via Ctrl+C command!")
                close()
        except NameError:
                if sample_folder is None:
                        print("Please create a  new sample folder, prior to starting a scan!")

def close():
    # when clicking the exit button, clean up GPIO, close windows, close myDisplay, 
    try:
	#clean up
        #exit cleanly, i.e. if the LED is on it shuts down when exiting
        win.destroy()
        #close active threads
        cleanup_stop_thread()
        #Close the Pi Camera window, MAYBE WORKING!?
        cv2.destroyAllWindows()
        frameflat.close()
        framerep.close()
        frametest.close()
        vframe.close()
        frameproj.close()
        rawCapture.close()
        print("Program closed correctly!")
    except KeyboardInterrupt:
        print("Program closed via Ctrl+C command!")
    except:
        print("Nothing to clean up!")
        
    print("Script closed!")
    exit()
