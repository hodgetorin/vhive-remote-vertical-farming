from tkinter import *
from tkinter import messagebox

w = Tk()
w.geometry("350x500")
w.title("Green Box Login")
w.resizable(0,0)

# declare the font type:
ft1 = ('consolas', 13)

def cmd():
    if e1.get() == '21017' and e2.get() == 'admin':
        messagebox.showinfo("                   ","                                                                      ")
        # convert the next two lines to their own function, developing into
        # the rest of the program. 
        q=Tk()
        q.mainloop()
    else:
        messagebox.showinfo("LOGIN FAILED", "    please try again or contact administrator   ")

# paint the background:
bg = PhotoImage(file = "bg_gradient1.png")
l_bg = Label(w, image = bg)
l_bg.place(x=0,y=0) 

Frame(w,width=250,height=400,bg='white').place(x=50,y=50)

# label 1 and entry 1 (username):
l1=Label(w,text="Username:", bg='white')
l1.config(font=ft1)
l1.place(x=80,y=200)

e1=Entry(w,width=20, border=0)
e1.config(font=ft1)
e1.place(x=80,y=230)

# label 2 and entry 2, (password):
l2=Label(w,text="Password:", bg='white')
l2.config(font=ft1)
l2.place(x=80,y=280)

e2=Entry(w,width=20, border=0)
e2.config(font=ft1,show="*")
e2.place(x=80,y=310)

Frame(w, width=180, height=2, bg="#141414").place(x=80,y=250)
Frame(w, width=180, height=2, bg="#141414").place(x=80,y=330)

Button(w,width=20,height=2,fg="white", bg="#5b9aa0", border=0, command=cmd, text="L O G I N").place(x=100,y=375)

w.mainloop()