#!/usr/bin/env python
# coding: utf-8

# # V Hive GUI 
# 
# 
# # Libraries & Globals:


# In[1]:


# must use sys and if statement for importing tkinter to avoid
# inconsistent error with loading the background image file:
import sys
if "tkinter" not in sys.modules:
    from tkinter import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, time
import time as tm
import relay
import arduinoComms
from board import Board

# data packages for Sensors page:
import numpy as np
import pandas as pd

# Packages for camera:
import camera
#import os
#import pygame

#from pygame.locals import *
#import pygame.camera

# global declarations:
# font syles:d
ft1 = ('consolas', 13)
ft2 = ('consolas', 18)

#def getnewWebcam():
    
light_start = time(18)
light_end = time(8)

def update(window):

    global updateHandle
    
    global light_start
    global light_end
    
    current_time = datetime.now().time();
    
    if ((light_start <= light_end and current_time > light_start and current_time < light_end) or (light_start > light_end and (current_time > light_start or current_time < light_end))):
        if (not (relay.l_board.value)):
            print("lights on")
            relay.TogglePower(relay.l_board)
    elif (relay.l_board.value):
        print("lights off")
        relay.TogglePower(relay.l_board)
        
    updateHandle = window.after(10, update, window)
    
def closeWindow(window):
    
    global updateHandle
    
    window.after_cancel(updateHandle)
    window.destroy()

# # Sensor Page:

# In[2]:


def sensors():
    
    def closeSP():
        closeWindow(sp)
        
    def homeSP():
        closeWindow(sp)
        home()
        
    def Graph():
        df = pd.read_csv('sensor_output.csv', names=["Date", "TempC", "TempF", "RH"],index_col=0,parse_dates = True)
        temprh = df.plot(use_index=False)
        temprh.set_xlabel("time (minutes)")
        plt.show()

    def printLatest():
        df = pd.read_csv('sensor_output.csv', names=["Date", "Temp (C)", "Temp (F)", "RH (%)"],index_col=0,parse_dates = True)
        label_current = Label(sp, text=df.tail(1))
        label_current.pack()

    sp=Tk()
    sp.geometry("800x450")
    sp.title("Sensor Data")
    sp.resizable(0,0)
    
    # place background: 
    im = Image.open("bg_gradient1.png")
    bg = ImageTk.PhotoImage(im) 
    canvas = Canvas(sp, width=800, height=450)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor='nw', image=bg)

    l_bg = Label(sp, image = bg)
    l_bg.place(x=0,y=0) 

    Frame(sp,width=700,height=350,bg='white').place(x=50,y=50)
    header = Label(sp,text = "Sensor Data", bg='white', font = ft2).place(x=310, y=60)

    graph_bt = Button(sp,width=15,height=2,fg="white", bg="#5b9aa0", border=0,  font = ft1, text = "draw graph", command = Graph)
    graph_bt.place(x=400, y=130)

    button_grab_current = Button(sp, text = "get current") #, command = printLatest)
    button_grab_current.place(x=400, y=300)

    #nute_pwr_lb1 = Label(pp,text = "Nutrient Pump",bg='white',font = ft2).place(x=100, y=250)
    #nute_pwr_lb2 = Label(pp,text = "Current state:          "+nute_state,bg='white',font = ft1).place(x=100, y=290)
    #nute_pwr_bt = Button(pp,width=15,height=2,fg="white", bg="#5b9aa0", border=0,  font = ft1, text="Toggle Power").place(x=400,y=250)
    # command = toggle power to pumps, rewrite nute_pwr_lb2

    home_bt = Button(sp,width=10,height=2,fg="white", bg="#5b9aa0", border=0, font = ft1,text="H O M E", command = homeSP).place(x=625,y=260)
    # command = return to main_page

    quit_bt = Button(sp,width=10,height=2,fg="white", bg="#5b9aa0", border=0, font = ft1, text="Q U I T", command = closeSP).place(x=625,y=325)
    # command = end program

    sp.after(0, update, sp)
    sp.mainloop()


# # Pump Page:
# ## FIXME: Need to add separate function for drawing toggle labels & pump states.

# In[3]:

def pumps():   
        
    # these will be replaced with "get(data_from_pi)"
    air_state = "ON"; nute_state = "ON"
    
    def closePP():
        closeWindow(pp)
    
    def homePP():
        closeWindow(pp)
        home()
        
    def nuteAreYouSure():        
        result = True
        if relay.nutrient_pump.value :
            result = messagebox.askokcancel("WARNING", "Turning off the nutrient pump while plants are in system is not recommended. Press OK to change state of pump.   ")
        if result:
            if relay.nutrient_pump.value:
                relay.TogglePower(relay.nutrient_pump)
                nute_state = "OFF" 
                nute_pwr_lb2.config(text = "Current state:          "+nute_state)
            else:
                relay.TogglePower(relay.nutrient_pump)
                nute_state = "ON"
                nute_pwr_lb2.config(text = "Current state:          "+nute_state)
    
    def airAreYouSure():        
        result = True
        if relay.air_pump.value :
            result = messagebox.askokcancel("WARNING", "Turning off the air pump while plants are in system is not recommended. Press OK to change state of pump.   ")
        if result:
            if relay.air_pump.value:
                relay.TogglePower(relay.air_pump)
                air_state = "OFF" 
                air_pwr_lb2.config(text = "Current state:          "+air_state)
            else:
                relay.TogglePower(relay.air_pump)
                air_state = "ON"
                air_pwr_lb2.config(text = "Current state:          "+air_state)
    
    pp=Tk()
    pp.geometry("800x450") # change to 800 x 450
    pp.title("Pump Controls")
    pp.resizable(0,0)

    # place background: 
    im = Image.open("bg_gradient1.png")
    bg = ImageTk.PhotoImage(im) 
    canvas = Canvas(pp, width=800, height=450)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor='nw', image=bg)
    
    # do not move this frame line:
    Frame(pp,width=700,height=350,bg='white').place(x=50,y=50)

    header = Label(pp,text = "Pump Controls", bg='white', font = ft2).place(x=250, y=60)

    # air_state will change on click of nute_pwr_button
    
    air_pwr_lb1 = Label(pp,text = "Air Pump",bg='white',font = ft2).place(x=100, y=130)
    air_pwr_lb2 = Label(pp,text = "Current state:          "+air_state,bg='white',font = ft1)
    air_pwr_lb2.place(x=100, y=170)
    air_pwr_bt = Button(pp,width=15,height=2,fg="white", bg="#5b9aa0", border=0,  font = ft1, text="Toggle Power", command=airAreYouSure)
    air_pwr_bt.place(x=400,y=130)
    

    # nute_state will change on click of nute_pwr_button
    
    nute_pwr_lb1 = Label(pp,text = "Nutrient Pump",bg='white',font = ft2).place(x=100, y=250)
    nute_pwr_lb2 = Label(pp,text = "Current state:          "+nute_state,bg='white',font = ft1)
    nute_pwr_lb2.place(x=100, y=290)
    nute_pwr_bt = Button(pp,width=15,height=2,fg="white", bg="#5b9aa0", border=0,  font = ft1, text="Toggle Power", command=nuteAreYouSure)
    nute_pwr_bt.place(x=400,y=250)
    # command = toggle power to pumps, rewrite nute_pwr_lb2

    home_bt = Button(pp,width=10,height=2, fg="white", bg="#5b9aa0", border=0, font=ft1, text="H O M E", command=homePP)
    home_bt.place(x=640,y=340)

    pp.after(0, update, pp)
    pp.mainloop()


# # Lights Page:
# #### FIXME: Needs working time/DLI calculation. Needs integration with actual light controls. 
# #### Print which L-board is currently selected. Grey out the button when it is pressed/"selected."
# #### make the G-boards slightly opaque in this screen

# In[4]:


def lights():
    
    global light_start
    global light_end
    
    # lights
    def closeLP():
        closeWindow(lp)
    def homeLP():
        closeWindow(lp)
        home()
    def setTimes():
    
        global light_start
        global light_end
        
        try:
            light_start = time.fromisoformat(start_v.get())
            light_end = time.fromisoformat(off_v.get())
        except ValueError as e:
            messagebox.showwarning("Invalid Value", e)
        
        cur_time.config(text = "on: " + light_start.isoformat() + " off: " + light_end.isoformat())


    def resetTimes():
    
        global light_start
        global light_end
        
        light_start = time(hour=8, minute=0)
        light_end = time(hour=22, minute=0)
        cur_time.config(text = "on: " + light_start.isoformat() + " off: " + light_end.isoformat())
        
        start_v.set(light_start.isoformat())
        off_v.set(light_end.isoformat())


    lp=Tk()
    lp.geometry("800x450")
    lp.title("Light Controls")
    lp.resizable(0,0)

    # place background: 
    im = Image.open("bg_gradient1.png")
    bg = ImageTk.PhotoImage(im) 
    canvas = Canvas(lp, width=800, height=450)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor='nw', image=bg)  

    dz = 0; dx = 0

    Frame(lp,width=700,height=350,bg='white').place(x=50,y=50)

    header = Label(lp, text="Light Controls", bg='white')
    header.config(font=ft2)
    header.place(x=250, y=60)

    # the boards:
    g1_lpt = Button(lp, text=" G1 ", width=2, height=9, fg="white", bg="#adabad", border=0)
    g1_lpt.config(font=ft1)
    g1_lpt.place(x=140,y=110)

    l1_lpt = Button(lp, text=" L1 ", width=2, height=9, fg="white", bg="#b73c9c", border=0)
    l1_lpt.config(font=ft1)
    l1_lpt.place(x=190,y=110)

    g2_lpt = Button(lp, text=" G2 ", width=2, height=9, fg="white", bg="#adabad", border=0)
    g2_lpt.config(font=ft1)
    g2_lpt.place(x=240,y=110)

    l2_lpt = Button(lp, text=" L2 ", width=2, height=9, fg="white", bg="#adabad", border=0)
    l2_lpt.config(font=ft1)
    l2_lpt.place(x=290,y=110)

    g3_lpt = Button(lp, text=" G3 ", width=2, height=9, fg="white", bg="#adabad", border=0)
    g3_lpt.config(font=ft1)
    g3_lpt.place(x=340,y=110)

    cur = Label(lp, text="Current Schedule:", bg='white')
    cur.config(font=ft1)
    cur.place(x=80, y=310)
    
    timeon = light_start.isoformat(); timeoff = light_end.isoformat()
    cur_time = Label(lp, text="on: " + timeon + " off: " + timeoff, bg='white')
    cur_time.config(font=ft1)
    cur_time.place(x=80, y=330)

    cur = Label(lp, text="Calculated DLI: 14", bg='white')
    cur.config(font=ft1)
    cur.place(x=80, y=360)

    set_time = Label(lp, text="Set time range ", bg='white')
    set_time.config(font=ft1)
    set_time.place(x=390, y=160)

    set_ex = Label(lp, text="Example: 06:00 - 22:00 ", bg='white')
    set_ex.config(font=ft1)
    set_ex.place(x=390, y=190)

    start_time = Label(lp, text="ON:  ", bg='white')
    start_time.config(font=ft1)
    start_time.place(x=390, y=220)

    start_v=StringVar()
    
    start_e=Entry(lp,width=8, border=1, textvariable=start_v)
    start_e.config(font=ft1)
    start_e.place(x=430,y=220)

    off_time = Label(lp, text="OFF:  ", bg='white')
    off_time.config(font=ft1)
    off_time.place(x=390, y=250)
    
    off_v=StringVar()

    start_v.set(light_start.isoformat())
    off_v.set(light_end.isoformat())

    off_e=Entry(lp,width=8, border=1, textvariable=off_v)
    off_e.config(font=ft1)
    off_e.place(x=430,y=250)

    #lhs = Radiobutton(lp, text="L", bg = "white")
    #lhs.place(x=390,y=120)

    #rhs = Radiobutton(lp, text="R", bg = "white")
    #rhs.place(x=420,y=120)

    #both = Radiobutton(lp, text="Both", bg = "white")
    #both.place(x=450,y=100)



    confirm_lpt = Button(lp, text="CONFIRM", width=7, height=1, fg="white", bg="green", border=0, command=setTimes)
    confirm_lpt.config(font=ft1)
    confirm_lpt.place(x=350,y=340)

    reset_lpt = Button(lp, text="RESET", width=7, height=1, fg="white", bg="red", border=0, command=resetTimes)
    reset_lpt.config(font=ft1)
    reset_lpt.place(x=430,y=340)

    home_lpt = Button(lp, text="H O M E", width=10, height=2, fg="white", bg="#5b9aa0", border=0, command = homeLP)
    home_lpt.config(font=ft1)
    home_lpt.place(x=640,y=340)

    help_lpt = Button(lp, text="?", width=2, height=1, fg="white", bg="#5b9aa0", border=0)
    help_lpt.config(font = ft1)
    help_lpt.place(x=690,y=60)

    lp.after(0, update, lp)
    lp.mainloop()


# # Vision:

# In[5]:


def vision():   
    
    def closeVP():
        closeWindow(vp)
        
    def homeVP():
        closeWindow(vp)
        home()
    
    def displayWebcam():
        im = Image.open("picture.png")
        latest_webcam = ImageTk.PhotoImage(im) 
        cam_canvas = Canvas(vp, width=300, height=300)
        cam_canvas.place(x=50, y=50)
        cam_canvas.create_image(0, 0, anchor="nw", bg="white",
                                highlightthickness=0, relief='ridge', image=latest_webcam)
    
    vp=Tk()
    vp.geometry("800x450") 
    vp.title("V Hive Vision")
    vp.resizable(0,0)

    # place background: 
    im = Image.open("bg_gradient1.png")
    bg = ImageTk.PhotoImage(im) 
    canvas = Canvas(vp, width=800, height=450)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor='nw', image=bg)

    # do not move this frame line:
    Frame(vp,width=700,height=350,bg='white').place(x=50,y=50)
    header = Label(vp, text = "V-Hive Vision", bg='white', font = ft2).place(x=250, y=60)

    # webcam image:
    camera.getnewWebcam()
    displayWebcam()
    
    home_bt = Button(vp,width=10,height=2,fg="white", bg="#5b9aa0", border=0, font = ft1,text="H O M E", command = homeVP)
    home_bt.place(x=640,y=340)

    #vp.after(3000, getnewWebcam())
    #vp.after(3100, displayWebcam())
    vp.mainloop()


# # Board Page

extended = False

boardList = [Board(), Board(), Board()]

boardSelect = 0

dx = 0

def boards():
    
    def closeBP():
        closeWindow(bp)
    
    def homeBP():
        closeWindow(bp)
        home()
    
    def boardInstructions():
        messagebox.showinfo("Directions:", "Select the board you wish to move, then change dx to the desired lateral distance in inches. Negative dx moves the board to the left and positive dx moves the board to the right.")
    
    def sendStop():
        arduinoComms.send("s")

    def sendExtend():
        global extended
        arduinoComms.flush()
        print(arduinoComms.send("r "+str(boardList[boardSelect].pos)+" 2000"))
        print(arduinoComms.readLine())
        print(arduinoComms.readLine())
        print(arduinoComms.send("h" if extended else "f25"))
        print(arduinoComms.readLine())
        print(arduinoComms.readLine())
        dz_bt.config(text="R E T R A C T" if extended else "E X T E N D")
        extended = not extended
        
    def sendZero():
        arduinoComms.send("u")
        
    def printPos():
        global boardSelect
        selected_pos.config(text="current position: " + str(boardList[boardSelect].pos))
        
    def selectBoard1():
        global boardSelect
        boardSelect = 0
        printPos()
    def selectBoard2():
        global boardSelect
        boardSelect = 1
        printPos()
    def selectBoard3():
        global boardSelect
        boardSelect = 2
        printPos()
        
    def printdx():
        dx_lb.config(text="dx: " + str(dx))
        
    def incdx():
        global dx
        dx += 1
        printdx()
        
    def decdx():
        global dx
        dx -= 1
        printdx()
        
    def sendScan():
        arduinoComms.flush()
        arduinoComms.send("f5")
        arduinoComms.readLines(2)
        arduinoComms.send("p")
        print(arduinoComms.readLine())
        boardList[0].pos = -float(arduinoComms.readLine())
        boardList[1].pos = -float(arduinoComms.readLine())
        boardList[2].pos = -float(arduinoComms.readLine())
        print(arduinoComms.readLine())
        arduinoComms.send("r0")
        print(arduinoComms.readLine())
        print(arduinoComms.readLine())
        arduinoComms.send("h")
        arduinoComms.readLines(2)
        
    def moveBoard():
        arduinoComms.flush()
        print(arduinoComms.send("f5"))
        print(arduinoComms.readLine())
        print(arduinoComms.readLine())
        print(arduinoComms.send("r"+"%.2f" % (boardList[boardSelect].pos-3)))
        print(arduinoComms.readLine())
        print(arduinoComms.readLine())
        print(arduinoComms.send("f0"))
        print(arduinoComms.readLine())
        print(arduinoComms.readLine())
        print(arduinoComms.send("R3.5 300"))
        print(arduinoComms.readLine())
        print(arduinoComms.readLine())
        arduinoComms.send("F5")
        arduinoComms.readLines(2)
        print(arduinoComms.send("R"+str(dx-.5)))
        print(arduinoComms.readLine())
        print(arduinoComms.readLine())
        arduinoComms.send("B5")
        arduinoComms.readLines(2)
        relay.TogglePower(relay.solenoid)
        print(arduinoComms.send("F1"))
        print(arduinoComms.readLine())
        print(arduinoComms.readLine())
        relay.TogglePower(relay.solenoid)
        arduinoComms.send("f5")
        arduinoComms.readLines(2)
        arduinoComms.send("r0")
        arduinoComms.readLines(2)
        arduinoComms.send("h")
        arduinoComms.readLines(2)
        boardList[boardSelect].pos += dx
    bp=Tk()
    bp.geometry("800x450")
    bp.title("Board Controls")
    bp.resizable(0,0)

    # place background: 
    im = Image.open("bg_gradient1.png")
    bg = ImageTk.PhotoImage(im) 
    canvas = Canvas(bp, width=800, height=450)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor='nw', image=bg) 

    dz = 0;

    Frame(bp,width=700,height=350,bg='white').place(x=50,y=50)

    header = Label(bp, text="Board Controls", bg='white')
    header.config(font=ft2)
    header.place(x=250, y=50)

    coord = Label(bp, text="0 ------------------------- 48", bg='white')
    coord.config(font=ft1)
    coord.place(x=120, y=80)


    # the boards:
    g1_bt = Button(bp, text=" G1 ", width=2, height=9, fg="white", bg="#3caa38", border=0, command=selectBoard1)
    g1_bt.config(font=ft1)
    g1_bt.place(x=140,y=110)

    l1_bt = Button(bp, text=" L1 ", width=2, height=9, fg="white", bg="#b73c9c", border=0, command=selectBoard2)
    l1_bt.config(font=ft1)
    l1_bt.place(x=190,y=110)

    g2_bt = Button(bp, text=" G2 ", width=2, height=9, fg="white", bg="#3caa38", border=0, command=selectBoard3)
    g2_bt.config(font=ft1)
    g2_bt.place(x=240,y=110)

    l2_bt = Button(bp, text=" L2 ", width=2, height=9, fg="white", bg="#adabad", border=0)
    l2_bt.config(font=ft1)
    l2_bt.place(x=290,y=110)

    g3_bt = Button(bp, text=" G3 ", width=2, height=9, fg="white", bg="#adabad", border=0)
    g3_bt.config(font=ft1)
    g3_bt.place(x=340,y=110)


    selected_pos = Label(bp, text="current position: 0", bg='white')
    selected_pos.config(font=ft1)
    selected_pos.place(x=140, y=310)
    
    # dz and dx hold integer values of inches
    dz_bt = Button(bp, text="E X T E N D", width=12, height=2, fg="white", bg="#f26d83", border=0, command=sendExtend)
    dz_bt.place(x=240, y=340)
    # on click: change button text to "R E T R A C T"

    dx_lb = Label(bp,text = "dx:  " + str(dx),bg='white')
    dx_lb.config(font=ft2)
    dx_lb.place(x=490, y=240)

    dx_up_bt = Button(bp, text=" + ", width=3, height=1, fg="white", bg="#f26d83", border=0, command=incdx)
    dx_up_bt.config(font=ft1)
    dx_up_bt.place(x=550,y=205)

    dx_dn_bt = Button(bp, text=" - ", width=3, height=1, fg="white", bg="#f26d83", border=0, command=decdx)
    dx_dn_bt.config(font=ft1)
    dx_dn_bt.place(x=550,y=275)

    scan_bt = Button(bp, text="SCAN", width=7, height=1, fg="white", bg="#f26d83", border=0, command=sendScan)
    scan_bt.config(font=ft1)
    scan_bt.place(x=640,y=135)

    confirm_bt = Button(bp, text="CONFIRM", width=7, height=1, fg="white", bg="#f26d83", border=0, command=moveBoard)
    confirm_bt.config(font=ft1)
    confirm_bt.place(x=640,y=205)

    reset_bt = Button(bp, text="ZERO", width=7, height=1, fg="white", bg="#f26d83", border=0, command=sendZero)
    reset_bt.config(font=ft1)
    reset_bt.place(x=640,y=275)

    home_bt = Button(bp, text="H O M E", width=10, height=2, fg="white", bg="#5b9aa0", border=0, command = homeBP)
    home_bt.config(font=ft1)
    home_bt.place(x=640,y=330)
   
    help_bt = Button(bp, text="?", width=2, height=1, fg="white", bg="#5b9aa0", border=0, command=boardInstructions)
    help_bt.config(font = ft1)
    help_bt.place(x=710,y=60)

    emc_bt = Button(bp, text="S T O P", width=8, height=2, fg="white", bg="red", border=0, command=sendStop)
    emc_bt.config(font = ft1)
    emc_bt.place(x=560,y=60)

    bp.after(0, update, bp)
    bp.mainloop()


# # Control Panel

# In[8]:


def home():
    
    def closeCP():
        closeWindow(cp)
    
    def logout():
        closeWindow(cp)
        login()

    # navigating from the control panel (home page)
    def cpLights():
        closeWindow(cp)
        lights()

    def cpSensors():
        closeWindow(cp)
        sensors()

    def cpBoards():
        closeWindow(cp)
        boards()

    def cpVision():
        closeWindow(cp)
        vision()

    def cpPumps():
        closeWindow(cp)
        pumps()
    
    cp=Tk()
    cp.geometry("800x450")
    cp.title("Control Panel")
    cp.resizable(0,0)
    
    # place background: 
    im = Image.open("bg_gradient1.png")
    bg = ImageTk.PhotoImage(im) 
    canvas = Canvas(cp, width=800, height=450)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor='nw', image=bg)
    
    Frame(cp, width=700, height=350, bg='white').place(x=50, y=50)

    header = Label(cp, text = "Control Panel", bg='white', font = ft2)
    header.place(x=300, y=60)

    sd_bt = Button(cp, width=20, height=2, fg="white", bg="#e96df2", border=0, text="S E N S O R  D A T A", command = cpSensors)
    sd_bt.place(x=100, y=100)

    vision_bt = Button(cp, width=20, height=2, fg="white", bg="#546ff7", border=0, text="V - H I V E  V I S I O N", command = cpVision)
    vision_bt.place(x=100, y=160)

    light_bt = Button(cp, width=20, height=2, fg="white", bg="#f2a46d", border=0, text="L I G H T S", command = cpLights)
    light_bt.place(x=100, y=220)

    pump_bt = Button(cp,width=20, height=2, fg="white", bg="#7dd0b6", border=0, text="P U M P S", command = cpPumps)
    pump_bt.place(x=100, y=280)

    board_bt = Button(cp, width=20, height=2, fg="white", bg="#f26d83", border=0, text="B O A R D S", command = cpBoards)
    board_bt.place(x=100, y=340)

    logout_bt = Button(cp,width=10,height=2, fg="white", bg="#5b9aa0", border=0, font=ft1, text="LOGOUT", command=logout)
    logout_bt.place(x=640,y=280)
    
    quit_bt = Button(cp, width=10, height=2, fg="white", bg="#5b9aa0", border=0, text="Q U I T", command = closeCP)
    quit_bt.place(x=660, y=350)
   
    cp.after(0, update, cp)
    cp.mainloop()
    


# Login:

#In[10]:


def login():
    window = Tk()
    window.geometry("350x450")
    window.title("Green Box Login")
    window.resizable(0,0)

    def cmd():
        if e1.get() == '21017' and e2.get() == 'admin':
            messagebox.showinfo("  Welcome   ", " Login Successful")
            # convert the next two lines to their own function, developing into
            # the rest of the program.
            window.destroy()
            initcnc()
        else:
            messagebox.showinfo("Login failed", "    Please try again or contact administrator   ")
    
    # draw the background and frame:
    im = Image.open("bg_gradient1.png")
    bg = ImageTk.PhotoImage(im) 
    canvas = Canvas(window, width=800, height=450)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor='nw', image=bg)
    Frame(window,width=250,height=320,bg='white').place(x=50,y=50)

    l0=Label(window,text="V-Hive Green Box", bg='white')
    l0.config(font=ft2)
    l0.place(x=70,y=65)
    
    # place UA logo:
    im1 = Image.open("ua_logo.png")
    ua_logo = ImageTk.PhotoImage(im1) 
    canvas = Canvas(window, width=90, height=80, bg="white", highlightthickness=0, relief='ridge')
    canvas.place(x=130, y=110)
    canvas.create_image(47, 42, anchor="center", image=ua_logo)
    
    # label 1 and entry 1 (username):
    l1=Label(window,text="Username:", bg='white')
    l1.config(font=ft1)
    l1.place(x=80,y=200)

    e1=Entry(window,width=20, border=0)
    e1.config(font=ft1)
    e1.place(x=80,y=230)

    # label 2 and entry 2, (password):
    l2=Label(window,text="Password:", bg='white')
    l2.config(font=ft1)
    l2.place(x=80,y=280)

    e2=Entry(window,width=20, border=0)
    e2.config(font=ft1,show="*")
    e2.place(x=80,y=310)

    Frame(window, width=180, height=2, bg="#141414").place(x=80,y=250)
    Frame(window, width=180, height=2, bg="#141414").place(x=80,y=330)

    Button(window,width=20,height=2,fg="white", bg="#5b9aa0", border=0, command=cmd, text="L O G I N").place(x=100,y=390)

    #window.after(0, update, window)
    window.mainloop()
    
def initialize():
    arduinoComms.flush()
    arduinoComms.send("i")
    while (arduinoComms.readLine() != "Limits Found"):
        pass
    arduinoComms.send("f5")
    arduinoComms.readLines(2)
    arduinoComms.send("r0")
    arduinoComms.readLines(2)
    arduinoComms.send("h")
    
def initcnc():
    window = Tk()
    window.geometry("350x450")
    window.title("Green Box Login")
    window.resizable(0,0)
    
    def callinit():
        initialize()
        window.destroy()
        home()

    # draw the background and frame:
    im = Image.open("bg_gradient1.png")
    bg = ImageTk.PhotoImage(im) 
    canvas = Canvas(window, width=800, height=450)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor='nw', image=bg)
    Frame(window,width=250,height=320,bg='white').place(x=50,y=50)

    l0=Label(window,text="V-Hive Green Box\nplease wait during initialization", bg='white')
    l0.config(font=ft2)
    l0.place(x=70,y=65)
    
    # place UA logo:
    im1 = Image.open("ua_logo.png")
    ua_logo = ImageTk.PhotoImage(im1) 
    canvas = Canvas(window, width=90, height=80, bg="white", highlightthickness=0, relief='ridge')
    canvas.place(x=130, y=110)
    canvas.create_image(47, 42, anchor="center", image=ua_logo)
    

    Frame(window, width=180, height=2, bg="#141414").place(x=80,y=250)
    Frame(window, width=180, height=2, bg="#141414").place(x=80,y=330)

    window.after(100, callinit)
    window.mainloop()

login()


# In[ ]:





# In[ ]:

           