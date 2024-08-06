#!/usr/bin/python

from hblt import scan as hblt
####### packages needed for the GUI ####
from tkinter import *
import tkinter.font

## GUI DEFINITIONS ##
win = Tk()
win.title("HBLT")
myFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

#Initiate web camera
#hblt.CamInit(cam_no=0, x_res=720, y_res=480)

#GUI starts below!
try:
        
        #Labels
        lbl = Label(win, text="Camera no. (0 or 1)", font = myFont)
        lbl.grid(row=1,column=1)
        
        #Labels
        large_font = ('Verdana', 15)
        e0 = Entry(win, width = 6, font=large_font)
        e0.insert(10, "1")
        e0.grid(row=1, column=2)
                
        lbl = Label(win, text="Camera coordinates: (X, W, Y, H)", font = myFont)
        lbl.grid(row=2,column=1)
        
        #Cam button
        CamButtonOn = Button(win, text = 'Acq.', font = myFont, command = lambda: hblt.CamAreaOnThread(x0=int(e11.get()), xw=int(e8.get()), y0=int(e9.get()), yh=int(e10.get()), cam_no = int(e0.get())), bg = 'green2', height = 1, width = 6)
        #CamButtonOn = Button(win, text = 'Acq.', font = myFont, command = lambda: hblt.CamAreaCheck(x0=int(e11.get()), xw=int(e8.get()), y0=int(e9.get()), yh=int(e10.get())), bg = 'green2', height = 1, width = 6)
        CamButtonOn.grid(row=2,column=6)

        #Labels
        large_font = ('Verdana', 15)
        e11 = Entry(win, width = 6, font=large_font)
        e11.insert(10, "140")
        #e11.insert(10, "0")
        e11.grid(row=2, column=2)

        #Labels
        large_font = ('Verdana', 15)
        e8 = Entry(win, width = 6, font=large_font)
        #e8.insert(10, "720")
        e8.insert(10, "500")
        e8.grid(row=2, column=3)
        
        #Labels
        large_font = ('Verdana', 15)
        e9 = Entry(win, width = 6, font=large_font)
        e9.insert(10, "80")
        #e9.insert(10, "0")
        e9.grid(row=2, column=4)

        #Labels
        large_font = ('Verdana', 15)
        e10 = Entry(win, width = 6, font=large_font)
        e10.insert(10, "410")
        #e10.insert(10, "480")
        e10.grid(row=2, column=5)

        #Labels        
        lbl = Label(win, text="Sample Name", font = myFont).grid(row=10,column=1)
        large_font = ('Verdana', 15)
        e1 = Entry(win, width = 10, font = large_font)
        e1.insert(10, "Default")
        e1.grid(row=10, column=2)
        #PrintButton = Button(win, text = 'PRINT', font = myFont, command = lambda: hblt.printparam(e1.get()), bg = 'bisque2', height = 1, width = 6).grid(row=10, column=3)
       
        #Labels, No. Acq. Projections
        lbl = Label(win, text="No. Projections", font = myFont).grid(row=11,column=1)
        large_font = ('Verdana', 15)
        
        e6 = Entry(win, width = 6, font = large_font)
        e6.insert(10, "200")
        e6.grid(row=11, column=2)
        
        #Labels, No. Acq. Projections
        lbl = Label(win, text="No. References", font = myFont).grid(row=12,column=1)
        large_font = ('Verdana', 15)

        e7 = Entry(win, width = 6, font = large_font)
        e7.insert(10, "20")
        e7.grid(row=12, column=2)

        #Acq. Rep. button
        ScanButton = Button(win, text = 'START', font = myFont, command = lambda: hblt.StartScan(x0=int(e11.get()), xw=int(e8.get()), y0=int(e9.get()), yh=int(e10.get()), no_projs=int(e6.get()), manual_sample_name = e1.get()), bg = 'green2', height = 1, width = 6)
        ScanButton.grid(row=11,column=3)

        #Acq. Manual Ref. scan button
        RefButton = Button(win, text = 'FLATS', font = myFont, command = lambda: hblt.StartRefScan(x0=int(e11.get()), xw=int(e8.get()), y0=int(e9.get()), yh=int(e10.get()), no_refs=int(e7.get()), manual_sample_name = e1.get()), bg = 'yellow2', height = 1, width = 6)
        RefButton.grid(row=12,column=3)

        #Acq. Manual Dark scan button
        #ManDarkButton = Button(win, text = 'DARKS', font = myFont, command = lambda: hblt.ManualDarkScan(x0=int(e7.get()), xw=int(e8.get()), y0=int(e9.get()), yh=int(e10.get()), manual_sample_name = e1.get()), bg = 'blue2', height = 1, width = 6)
        #ManDarkButton.grid(row=11,column=5)

        #Labels
        lbl = Label(win, text="Program:", font = myFont)
        lbl.grid(row=14,column=1)

        #exit Button
        exitButton = Button(win, text = 'CLOSE', font = myFont, command = hblt.close, bg = 'red2', height = 1, width = 6)
        exitButton.grid(row=14, column=2)#columnspan=1)

        #exit cleanly, i.e. if the LED is on it shuts down when exiting
        win.protocol("WM_DELETE_WINDOW", hblt.close)
   
        #loop forever, keeps the GUI running forever
        win.mainloop()
        
except KeyboardInterrupt:
        print("GUI interrupted via Ctrl+C command!")
        hblt.close()
#except NameError:
#        if area_cr is None:
#                print("Please set capture area (by Turning on the camera), prior to starting a scan!")
#except:
        #close()
#        print("GUI closed normally or via exception!")
