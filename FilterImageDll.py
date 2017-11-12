from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk
from ctypes import CDLL, c_int, POINTER, c_double, cast
import re


class FilterImageDll(Frame):

    def __init__(self, parent: object) -> object:
        Frame.__init__(self, parent)
        self.parent = parent
        self.loadAndSetDll()
        self.initUI()

    # laduje funkcje z biblioteki dll z pliku i ustawia jej argumenty i typ zwracany
    def loadAndSetDll(self):
        print('loadAndSetDll')
        self.lib = CDLL('filterlib')
        self.lib.test.argtypes = (c_int,  # szerokosc obrazu
                             c_int,  # wysokosc obrazu
                             POINTER(c_double),  # wskaznik na tablice pikseli obrazu
                             POINTER(c_double),  # wskaznik na tablice nowych pikseli obrazu
                             POINTER(c_double) # wskaznik na maske
                             )

        self.lib.test.restype = POINTER(c_double)

    # wywolanie funkcji z biblioteki dll, ktora wykonuje filtrowanie na obrazie za pomoca podanej przez uzytkownika maski
    def filterImg(self):
        print('filterImg')

        entriesStrings = [e.get() for e in self.entries]

        for es in entriesStrings:
            if re.match("^-?\d+?\.?/?\d*?$", es) is None:
                messagebox.showwarning(
                        "Wprowadź maskę",
                        "Nieprawidłowa wartość maski:\n(%s)" % es
                    )
                return

        try:
            mask = [eval(es) for es in entriesStrings]
        except ZeroDivisionError:
            messagebox.showwarning(
                "Wprowadź maskę",
                "Nie można dzielić przez 0"
            )
            return

        c_mask = cast((c_double * 9)(), POINTER(c_double))
        for i in range(9):
            c_mask[i] = mask[i]

        self.imgLst = list(self.img.getdata())  # zamiana obrazu na liste
        c_imgLst = cast((c_double * self.imgTk.width()*self.imgTk.height())(), POINTER(c_double))
        for i in range(len(self.imgLst)):
            c_imgLst[i] = self.imgLst[i]

        c_imgLstNew = cast((c_double * self.imgTk.width()*self.imgTk.height())(), POINTER(c_double))
        for i in range(len(self.imgLst)):
            c_imgLstNew[i] = 0.0

        self.lib.test(c_int(self.imgTk.width()), c_int(self.imgTk.height()), c_imgLst, c_imgLstNew, c_mask)

        for i in range(len(self.imgLst)):
            self.imgLst[i] = c_imgLstNew[i]

        imgNew = Image.new(self.img.mode, self.img.size)
        imgNew.putdata(self.imgLst)
        self.img = imgNew
        self.imgTk = ImageTk.PhotoImage(self.img)
        self.labelImg.configure(image=self.imgTk)
        self.labelImg.image = self.imgTk

    # wyobor obrazu z pliku
    def loadImg(self):
        print('loadImg')
        try:
            self.fileName = filedialog.askopenfilename(filetypes=(("jpg image files", "*.jpg"), ("gif image files", "*.gif"), ("tiff image files", "*.tiff")))
            print('fileName: ', self.fileName)
            if self.fileName == '':
                return
            self.img = Image.open(self.fileName).convert("L")  # zamiana obrazu na odcienie szarosci
            self.imgTk = ImageTk.PhotoImage(self.img)
            self.labelImg.configure(image=self.imgTk)
            self.labelImg.image = self.imgTk
        except IOError:
            messagebox.showerror(
                "Błąd otwarcia pliku",
                "Nie można otworzyć pliku:\n(%s)" % self.fileName
            )


    def initUI(self):
        self.parent.title("Filtrowanie obrazu")
        self.pack(fill=BOTH, expand=1)
        Style().configure("TFrame", background="#333")  # ustawienie stylu z ciemnym tlem

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.columnconfigure(0, pad=3)
        frame.columnconfigure(1, pad=3)
        frame.columnconfigure(2, pad=3)
        frame.columnconfigure(3, pad=3)
        frame.rowconfigure(0, pad=3)
        frame.rowconfigure(1, pad=3)
        frame.rowconfigure(2, pad=3)
        frame.rowconfigure(3, pad=3)

        # pola do wprowadzenia maski
        maskLabel = Label(frame, text="Wprowadź maskę: ")
        maskLabel.grid(row=0, columnspan=3, sticky=W + E)
        self.entry1 = Entry(frame)
        self.entry1.grid(row=1, column=0)
        self.entry2 = Entry(frame)
        self.entry2.grid(row=1, column=1)
        self.entry3 = Entry(frame)
        self.entry3.grid(row=1, column=2)
        self.entry4 = Entry(frame)
        self.entry4.grid(row=2, column=0)
        self.entry5 = Entry(frame)
        self.entry5.grid(row=2, column=1)
        self.entry6 = Entry(frame)
        self.entry6.grid(row=2, column=2)
        self.entry7 = Entry(frame)
        self.entry7.grid(row=3, column=0)
        self.entry8 = Entry(frame)
        self.entry8.grid(row=3, column=1)
        self.entry9 = Entry(frame)
        self.entry9.grid(row=3, column=2)

        self.entries = [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6, self.entry7, self.entry8, self.entry9]
        for e in self.entries: # ustawienie poczatkowej wartosci elementow maski na 1.0
            e.insert(0,0.0)

        frame.pack(side=LEFT, padx=25, pady=25)

        frame2 = Frame(self, relief=RAISED, borderwidth=0)
        frame2.pack(side=BOTTOM)

        self.img = Image.open('lenaGrey.jpg').convert("L") # zamiana obrazu na odcienie szarosci
        self.imgTk = ImageTk.PhotoImage(self.img)

        self.labelImg = Label(self, image=self.imgTk)
        self.labelImg.image = self.imgTk
        self.labelImg.pack(side=RIGHT, padx=20, pady=20)

        filterButton = Button(frame2, text="Filtruj", command=self.filterImg)
        filterButton.pack(side=LEFT, padx=5, pady=5)

        loadImgButton = Button(frame2, text="Wczytaj obraz", command=self.loadImg)
        loadImgButton.pack(side=LEFT, padx=5, pady=5)

        self.pack()

