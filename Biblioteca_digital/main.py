# main.py
import tkinter as tk
from interfaz_inicio import InterfazInicio

def main():
    root = tk.Tk()
    app = InterfazInicio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
