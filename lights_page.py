from tkinter import *

lp=Tk()
lp.geometry("650x500")
lp.title("Light Controls")
lp.resizable(0,0)

ft1 = ('consolas', 13)
ft2 = ('consolas', 18)

bg = PhotoImage(file = "bg_gradient1.png")
l_bg = Label(lp, image = bg)
l_bg.place(x=0,y=0) 

dz = 0; dx = 0

Frame(lp, width=550, height=400, bg='white').place(x=50, y=50)

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
cur.place(x=80, y=340)

cur = Label(lp, text="Calculated DLI: 14", bg='white')
cur.config(font=ft1)
cur.place(x=80, y=390)

timeon = "8:00"; timeoff = "22:00"

cur_time = Label(lp, text="on: " + timeon + " off: " + timeoff, bg='white')
cur_time.config(font=ft1)
cur_time.place(x=80, y=360)

set_time = Label(lp, text="Set time range ", bg='white')
set_time.config(font=ft1)
set_time.place(x=390, y=160)

set_ex = Label(lp, text="Example: 6:00 - 22:00 ", bg='white')
set_ex.config(font=ft1)
set_ex.place(x=390, y=190)

start_time = Label(lp, text="ON:  ", bg='white')
start_time.config(font=ft1)
start_time.place(x=390, y=220)

start_e=Entry(lp,width=8, border=1)
start_e.config(font=ft1)
start_e.place(x=430,y=220)

off_time = Label(lp, text="OFF:  ", bg='white')
off_time.config(font=ft1)
off_time.place(x=390, y=250)

off_e=Entry(lp,width=8, border=1)
off_e.config(font=ft1)
off_e.place(x=430,y=250)

#lhs = Radiobutton(lp, text="L", bg = "white")
#lhs.place(x=390,y=120)

#rhs = Radiobutton(lp, text="R", bg = "white")
#rhs.place(x=420,y=120)

#both = Radiobutton(lp, text="Both", bg = "white")
#both.place(x=450,y=100)

# dz and dx hold integer values of inches
#dz_lpt = Button(lp, text="R E T R A C T", width=12, height=2, fg="white", bg="#5b9aa0", border=0)
#dz_lpt.place(x=70, y=370)

#dx_llp = Label(lp,text = "dx:  " + str(dx),bg='white')
#dx_llp.config(font=ft2)
#dx_llp.place(x=200, y=380)

#dx_up_lpt = Button(lp, text=" + ", width=3, height=1, fg="white", bg="#5b9aa0", border=0)
#dx_up_lpt.config(font=ft1)
#dx_up_lpt.place(x=260,y=345)

#dx_dn_lpt = Button(lp, text=" - ", width=3, height=1, fg="white", bg="#5b9aa0", border=0)
#dx_dn_lpt.config(font=ft1)
#dx_dn_lpt.place(x=260,y=415)

confirm_lpt = Button(lp, text="CONFIRM", width=7, height=1, fg="white", bg="green", border=0)
confirm_lpt.config(font=ft1)
confirm_lpt.place(x=350,y=350)

reset_lpt = Button(lp, text="RESET", width=7, height=1, fg="white", bg="red", border=0)
reset_lpt.config(font=ft1)
reset_lpt.place(x=350,y=400)

home_lpt = Button(lp, text="H O M E", width=10, height=2, fg="white", bg="#5b9aa0", border=0)
home_lpt.config(font=ft1)
home_lpt.place(x=495,y=320)
# command = return to main_page

quit_lpt = Button(lp, text="Q U I T", width=10, height=2, fg="white", bg="#5b9aa0", border=0)
quit_lpt.config(font=ft1)
quit_lpt.place(x=495,y=380)

# command = end program
help_lpt = Button(lp, text="?", width=2, height=1, fg="white", bg="#5b9aa0", border=0)
help_lpt.config(font = ft1)
help_lpt.place(x=560,y=60)

#emc_lpt = Button(lp, text="S T O P", width=8, height=2, fg="white", bg="red", border=0)
#emc_lpt.config(font = ft1)
#emc_lpt.place(x=510,y=250)

lp.mainloop()