from tkinter import Tk
from FilterImageDll import FilterImageDll

def main():
    root = Tk()
    root.geometry("1000x600+300+300")
    app = FilterImageDll(root)
    app.mainloop()

if __name__ == '__main__':
    main()
