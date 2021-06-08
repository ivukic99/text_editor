from tkinter.colorchooser import askcolor
from tkinter.simpledialog import *

class FontDialog(Dialog):
    def body(self, parent):
        self.title("Font")
        self.root = parent
        #self.root.iconbitmap(r'C:\Users\Korisnik\Desktop\Zavrsni_rad\icon.ico')
        self.config(height=800)
        Label(self.root, text="Font").grid(row=0, column=0)
        Label(self.root, text="Stil").grid(row=0, column=1)
        Label(self.root, text="Velicina").grid(row=0, column=2)

        #lista popisa fontova
        self.F = Listbox(self.root, exportselection=0)
        f = ["Arial", "Calibri", "Comic Sans MS", "Courier New", "Times New Roman", "Verdana"]
        for t in f:
            self.F.insert(END, t)
        self.F.grid(row=1, column=0)
        self.F.select_set(1)
        self.F.bind("<<ListboxSelect>>", self.Click)

        #lista sa popisom stilova
        self.S = Listbox(self.root, exportselection=0)
        s = ["Regular", "Italic", "Bold", "Bold Italic"]
        for t in s:
            self.S.insert(END, t)
        self.S.grid(row=1, column=1)
        self.S.select_set(0)
        self.S.bind("<<ListboxSelect>>", self.Click)

        #lista sa popisom veličina
        v = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
        self.V = Listbox(self.root)
        for t in v:
            self.V.insert(END, t)
        self.V.grid(row=1, column=2)
        self.V.select_set(4)
        self.V.bind("<<ListboxSelect>>", self.Click)

        #gumb za odabir boja
        self.C = Button(self.root, bg="black", width=10, command=self.Boja)
        self.C.grid(row=2, column=0, padx=3, pady=3)

        #naljepnica na kojoj se nalazi tekst oblikovan odabranim fontom
        self.P = Label(self.root, text="Primjer teksta", bg="yellow")
        self.P.grid(row=3, column=0, columnspan=3)
        self.Click()
        self.Font = None
        return self.F

    def Click(self, e = None):
        font = self.F.get(self.F.curselection()[0])
        stil = self.S.get(self.S.curselection()[0]).lower()
        velicina = int(self.V.get(self.V.curselection()[0]))
        if stil == "regular":
            stil = "normal"
        self.P.config(font = (font, velicina, stil))
        return

    def Boja(self):
        c = askcolor()
        if c:
            self.C.config(bg = c[1])
            self.P.config(fg = c[1])
        return

    def apply(self):
        self.Font = (self.P["font"], self.P["fg"])
        return

