from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk
import process_photo


class BillScanner:
    def __init__(self, parent):
        self.myParent = parent  # remember my parent, the root
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()

        self.button1 = Button(self.myContainer1)
        self.button1.configure(text="Load new bill")
        self.button1.pack()
        self.button1.bind("<Button-1>", self.button1Click) ### (1)        

        self.button1 = Button(self.myContainer1)
        self.button1.configure(text="See database")
        self.button1.pack()
        self.button1.bind("<Button-1>", self.button1Click) ### (1)

        self.button3 = Button(self.myContainer1)
        self.button3.configure(text="Exit")
        self.button3.pack()
        self.button3.bind("<Button-1>", self.button3Click) ### (2)

    def button1Click(self, event):    ### (3)
        self.myParent.withdraw()
        filename = tkFileDialog.askopenfilename()
        print filename
        pr = process_photo.ProcessPhoto(filename)
        if pr.ended == True:
            photo = ImageTk.PhotoImage(file=pr.outfile)
            label = Label(self.myContainer1, image=photo)
            label.photo = photo
            label.pack()
            self.myParent.deiconify()

    def button3Click(self, event):
        self.myParent.destroy()


root = Tk()
myapp = BillScanner(root)
root.mainloop()