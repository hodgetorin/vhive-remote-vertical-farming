from tkinter import *

b=Tk()
b.geometry("650x500")
b.title("Board Controls")
b.resizable(0,0)

bg = PhotoImage(file = "bg_gradient1.png")
l_bg = Label(b, image = bg)
l_bg.place(x=0,y=0) 

ft1 = ('consolas', 13)
ft2 = ('consolas', 18)

#j=0;r=100
#for i in range(1000):
 #   c=str(222222+r)
  #  Frame(b, width=10, height=500, bg='#'+c).place(x=j, y=0)
   # j=j+10
    #r=r+100

dz = 0; dx = 0

Frame(b, width=550, height=400, bg='white').place(x=50, y=50)

header = Label(b, text="Board Controls", bg='white')
header.config(font=ft2)
header.place(x=250, y=50)

coord = Label(b, text="0 ------------------------- 48", bg='white')
coord.config(font=ft1)
coord.place(x=120, y=80)

selected_pos = Label(b, text="current position: 0", bg='white')
selected_pos.config(font=ft1)
selected_pos.place(x=70, y=330)

# the boards:
g1_bt = Button(b, text=" G1 ", width=2, height=9, fg="white", bg="#3caa38", border=0)
g1_bt.config(font=ft1)
g1_bt.place(x=140,y=110)

l1_bt = Button(b, text=" L1 ", width=2, height=9, fg="white", bg="#b73c9c", border=0)
l1_bt.config(font=ft1)
l1_bt.place(x=190,y=110)

g2_bt = Button(b, text=" G2 ", width=2, height=9, fg="white", bg="#3caa38", border=0)
g2_bt.config(font=ft1)
g2_bt.place(x=240,y=110)

l2_bt = Button(b, text=" L2 ", width=2, height=9, fg="white", bg="#adabad", border=0)
l2_bt.config(font=ft1)
l2_bt.place(x=290,y=110)

g3_bt = Button(b, text=" G3 ", width=2, height=9, fg="white", bg="#adabad", border=0)
g3_bt.config(font=ft1)
g3_bt.place(x=340,y=110)


# dz and dx hold integer values of inches
dz_bt = Button(b, text="E X T E N D", width=12, height=2, fg="white", bg="#f26d83", border=0)
dz_bt.place(x=70, y=370)
# on click: change button text to "R E T R A C T"

dx_lb = Label(b,text = "dx:  " + str(dx),bg='white')
dx_lb.config(font=ft2)
dx_lb.place(x=200, y=380)

dx_up_bt = Button(b, text=" + ", width=3, height=1, fg="white", bg="#f26d83", border=0)
dx_up_bt.config(font=ft1)
dx_up_bt.place(x=260,y=345)

dx_dn_bt = Button(b, text=" - ", width=3, height=1, fg="white", bg="#f26d83", border=0)
dx_dn_bt.config(font=ft1)
dx_dn_bt.place(x=260,y=415)

confirm_bt = Button(b, text="CONFIRM", width=7, height=1, fg="white", bg="#f26d83", border=0)
confirm_bt.config(font=ft1)
confirm_bt.place(x=350,y=350)

reset_bt = Button(b, text="RESET", width=7, height=1, fg="white", bg="#f26d83", border=0)
reset_bt.config(font=ft1)
reset_bt.place(x=350,y=400)

home_bt = Button(b, text="H O M E", width=10, height=2, fg="white", bg="#5b9aa0", border=0)
home_bt.config(font=ft1)
home_bt.place(x=495,y=320)
# command = return to main_page

quit_bt = Button(b, text="Q U I T", width=10, height=2, fg="white", bg="#5b9aa0", border=0)
quit_bt.config(font=ft1)
quit_bt.place(x=495,y=380)

# command = end program
help_bt = Button(b, text="?", width=2, height=1, fg="white", bg="#5b9aa0", border=0)
help_bt.config(font = ft1)
help_bt.place(x=560,y=60)

emc_bt = Button(b, text="S T O P", width=8, height=2, fg="white", bg="red", border=0)
emc_bt.config(font = ft1)
emc_bt.place(x=510,y=250)

b.mainloop()