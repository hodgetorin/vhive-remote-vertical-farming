from tkinter import *

cp=Tk()
cp.geometry("650x500")
cp.title("CONTROL PANEL")
cp.resizable(0,0)

ft1 = ('consolas', 13)
ft2 = ('consolas', 18)


bg = PhotoImage(file = "bg_gradient1.png")
l_bg = Label(cp, image = bg)
l_bg.place(x=0,y=0) 


Frame(cp, width=550, height=400, bg='white').place(x=50, y=50)

#header = Label(cp, text = "Control Panel", bg='white', font = ft2)
#header.place(x=250, y=60)

#canvas = Canvas(cp, width = 260, height = 120, highlightthickness=0, relief='ridge')
#canvas.place(x=250, y = 200)
#canvas.create_image(image = (PhotoImage(file = "cp_title.gif")))


#l_logo = Label(cp, image = logo)
#l_logo.place(x=310, y=120)

sd_bt = Button(cp, width=20, height=2, fg="white", bg="#e96df2", border=0, text="S E N S O R  D A T A")
sd_bt.place(x=100, y=120)

vision_bt = Button(cp, width=20, height=2, fg="white", bg="#546ff7", border=0, text="V - H I V E  V I S I O N")

vision_bt.place(x=100, y=180)

light_bt = Button(cp, width=20, height=2, fg="white", bg="#f2a46d", border=0, text="L I G H T S")
light_bt.place(x=100, y=240)

pump_bt = Button(cp,width=20, height=2, fg="white", bg="#7dd0b6", border=0, text="P U M P S")
pump_bt.place(x=100, y=300)

board_bt = Button(cp, width=20, height=2, fg="white", bg="#f26d83", border=0, text="B O A R D S")
board_bt.place(x=100, y=360)

quit_bt = Button(cp, width=10, height=2, fg="white", bg="#5b9aa0", border=0, text="Q U I T")
quit_bt.place(x=510, y=400)
# needs command = lamda\ endprog()

logout_bt = Button(cp, width=10, height=2, fg="white", bg="#5b9aa0", border=0, text="L O G O U T ")
logout_bt.place(x=510, y=350)
# needs command = return to login_page()


cp.mainloop()




