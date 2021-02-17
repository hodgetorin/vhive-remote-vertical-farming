from tkinter import *

pp=Tk()
pp.geometry("650x500")
pp.title("Pump Controls")
pp.resizable(0,0)

ft1 = ('consolas', 13)
ft2 = ('consolas', 18)

bg = PhotoImage(file = "bg_gradient1.png")
l_bg = Label(pp, image = bg)
l_bg.place(x=0,y=0) 

Frame(pp,width=550,height=400,bg='white').place(x=50,y=50)

header = Label(pp,text = "Pump Controls",bg='white',font = ft2).place(x=250, y=60)

# air_state will change on click of nute_pwr_button
air_state = "ON"
air_pwr_lb1 = Label(pp,text = "Air Pump",bg='white',font = ft2).place(x=100, y=130)
air_pwr_lb2 = Label(pp,text = "Current state:          "+air_state,bg='white',font = ft1).place(x=100, y=170)
air_pwr_bt = Button(pp,width=15,height=2,fg="white", bg="#5b9aa0", border=0,  font = ft1, text="Toggle Power").place(x=400,y=130)
# command = open dialog box, toggle power to pumps, rewrite air_pwr_lb2

# nute_state will change on click of nute_pwr_button
nute_state = "ON"
nute_pwr_lb1 = Label(pp,text = "Nutrient Pump",bg='white',font = ft2).place(x=100, y=250)
nute_pwr_lb2 = Label(pp,text = "Current state:          "+nute_state,bg='white',font = ft1).place(x=100, y=290)
nute_pwr_bt = Button(pp,width=15,height=2,fg="white", bg="#5b9aa0", border=0,  font = ft1, text="Toggle Power").place(x=400,y=250)
# command = toggle power to pumps, rewrite nute_pwr_lb2

home_bt = Button(pp,width=10,height=2,fg="white", bg="#5b9aa0", border=0, font = ft1,text="H O M E").place(x=400,y=380)
# command = return to main_page

quit_bt = Button(pp,width=10,height=2,fg="white", bg="#5b9aa0", border=0, font = ft1, text="Q U I T").place(x=500,y=380)
# command = end program

pp.mainloop()
