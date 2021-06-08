from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from Dialog_window import *
from Image_dialog import *
import cv2
import pytesseract

class Editor(Frame):
    def __init__(self, root):
        self.root = root
        self.root.title("Prozor za obradu teksta")
        self.root.iconbitmap(r'C:\Users\Korisnik\Desktop\Zavrsni_rad\icon.ico')
        super(Editor, self).__init__(self.root)
        self.KreirajSučelje()
        self.pack(fill=BOTH, expand=True)
        return

    def KreirajSučelje(self):
        #ovo je izgled editora i pokretna traka na rubovima
        self.Tn = 1
        ys = Scrollbar(self.root, orient=VERTICAL)
        ys.pack(side=RIGHT, fill=Y)
        xs = Scrollbar(self.root, orient=HORIZONTAL)
        xs.pack(side=BOTTOM, fill=X)

        self.T = Text(self, wrap = NONE, spacing1 = 5)
        self.T.pack(fill=BOTH, expand=True)
        self.T.config(xscrollcommand = xs.set, yscrollcommand = ys.set)
        self.T.focus_set()
        self.F = None

        ys.config(command=self.T.yview)
        xs.config(command=self.T.xview)

        #ovo je izbornik
        mB = Menu(self.root)
        mD = Menu(mB, tearoff = 0)
        mD.add_command(label="Učitaj fotografiju", underline=0, accelerator="Ctrl+U", command=self.Učitaj_sliku)
        self.root.bind("<Control-u>", self.Učitaj_sliku)
        mD.add_separator()
        mD.add_command(label="Nova", underline=0, accelerator="Ctrl+N", command=self.Nova)
        self.root.bind("<Control-n>", self.Nova)
        mD.add_command(label="Otvori", underline=0, accelerator="Ctrl+O", command=self.Otvori)
        self.root.bind("<Control-o>", self.Otvori)
        mD.add_command(label="Spremi", underline=0, accelerator="Ctrl+S", command=self.Spremi)
        self.root.bind("<Control-s>", self.Spremi)
        mD.add_command(label="Spremi kao...", underline=7, accelerator="Ctrl+Shift+S", command=self.SpremiKao)
        self.root.bind("<Control-Shift-s>", self.SpremiKao)
        mD.add_separator()
        mD.add_command(label="Kraj", underline=0, accelerator="Ctrl+Q", command=self.Kraj)
        self.root.bind("<Control-q>", self.Kraj)
        mB.add_cascade(menu=mD, label="Datoteka")

        uM = Menu(mD, tearoff=0)
        uM.add_command(label="Font", underline=0, accelerator="Ctrl+F", command=self.Font)
        self.root.bind("<Control-f>", self.Font)
        uM.add_separator()
        uM.add_command(label="Izreži", underline=0, accelerator="Ctrl+X", command=self.Izreži)
        #self.root.bind("<Control-x>", self.Izreži)
        uM.add_command(label="Kopiraj", underline=0, accelerator="Ctrl+C", command=self.Kopiraj)
        #self.root.bind("<Control-c>", self.Kopiraj)
        uM.add_command(label="Zalijepi", underline=0, accelerator="Ctrl+V", command=self.Zalijepi)
        #self.root.bind("<Control-v>", self.Zalijepi)
        mB.add_cascade(menu=uM, label="Uređivanje")

        self.root.config(menu = mB)
        return


    def Kraj(self, e = None):
        self.root.destroy()
        return

    def Nova(self, e = None):
        self.T.delete(1.0, END)
        self.F = None
        self.root.title("Bez imena")
        return

    def Otvori(self, e = None):
        fname = askopenfilename(filetype=[("Sve datoteke", "*.*"),("Text datoteke", "*.txt")], title="Odaberi datoteku")
        if fname:
            try:
                #sljedeca linija brise prethodno zapisani tekst, bez njega novi tekst se dodaje na prethodni
                #self.T.delete(1.0, END)
                with open(fname, "r") as fread:
                    p = fread.read()
                    self.T.insert(0.0, p)
                    self.root.title(fname)
                    self.F = fname
            except:
                showerror("Program za uređivanje teksta", "Datoteka ne postoji")
        return

    def Spremi(self, e = None):
        if self.F == None:
            self.SpremiKao()
        else:
            with open(self.F, "w") as f:
                f.write(self.T.get(0.0, END))
        return

    def SpremiKao(self, e = None):
        #fname = asksaveasfilename(filetype=[("Datoteka python", "*.py"), ("Tekstualne datoteke", "*.txt"),
        #                                  ("Sve datoteke", "*.*"), ("Png slika", "*.png"),
        #                                  ("jpg slika", "*.jpg")], defaultextension=".txt", title="Spremi kao...")

        fname = asksaveasfilename(filetype=[("Sve datoteke", "*.*"), ("Text datoteke", "*.txt")], defaultextension=".txt", title="Spremi kao...")
        if fname:
            self.F = fname
            self.Spremi()
            self.root.title(fname)
        return

    def Kopiraj(self, e = None):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.T.get(SEL_FIRST, SEL_LAST))
        except:
            showerror("Prgram za uređivanje teksta", "Niste označili tekst")
        return

    def Izreži(self, e = None):
        try:
            self.Kopiraj()
            self.T.delete(SEL_FIRST, SEL_LAST)
        except:
            return
        return

    def Zalijepi(self, e = None):
        try:
            self.T.insert(INSERT, self.root.clipboard_get())
        except:
            showerror("Prgram za uređivanje teksta", "Međuspremnik je prazan")
        return

    def Font(self, e = None):
        try:
            f = FontDialog(self.root)
            if f.Font:
                t = "t_" + str(self.Tn)
                self.T.tag_add(t, SEL_FIRST, SEL_LAST)
                self.T.tag_config(t, font= f.Font[0], foreground=f.Font[1])
                self.Tn += 1
        except:
            return
        return

    def Učitaj_sliku(self, e = None):
        #try:
        #    ImageDialog(self.root)
        #except:
        #    print("ne radi")
        #return
        fname = askopenfilename(
            filetype=[("Fotografija datoteke", "*.jpg;" "*.jpeg;" "*.png"), ("PDF datoteke", "*.pdf")],
            title="Odaberi fotografiju")

        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        img = cv2.imread(fname)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rez = pytesseract.image_to_string(img, lang="eng+cro")
        self.T.insert(0.0, rez)

        hImg, wImg, _ = img.shape  # vraca velicinu slike
        boxes = pytesseract.image_to_data(img)
        for x, b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                if len(b) == 12:
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
                    #cv2.putText(img, b[11], (x, y + 65), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Result", img)
        cv2.waitKey(0)

def main():
    e = Editor(Tk())
    mainloop()
main()