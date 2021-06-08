from tkinter.simpledialog import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

class ImageDialog(Dialog):
    def body(self, parent):
        self.title("Fotografija")
        self.root = parent
        #self.root.iconbitmap(r'C:\Users\Korisnik\Desktop\Zavrsni_rad\icon.ico')
        self.config(height=800)
        fname = askopenfilename(filetype=[("Fotografija datoteke", "*.jpg;" "*.jpeg;" "*.png"), ("PDF datoteke", "*.pdf")],
                                title="Odaberi fotografiju")

        img = Image.open(fname)
        img.thumbnail((350,350))
        img = ImageTk.PhotoImage(img)
        lbl = Label(self)
        lbl.configure(image=img)
        lbl.image = img
        lbl.pack()

        #Label(self.root, image=img).grid(row=0, column=0)


