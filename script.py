from PIL import Image
import pyautogui as pg
import keyboard as kb
import tkinter as tk
from tkinter import filedialog as fd

def gui():
    root = tk.Tk()
    root.title('Gartics Drawing Bot')
    root.geometry('300x200')

    def get_xy1():
        kb.wait('space')
        x1, y1 = pg.position()
        label1.config(text=f'x1: {x1}, y1: {y1}')
    
    def get_xy2():
        kb.wait('space')
        x2, y2 = pg.position()
        label2.config(text=f'x2: {x2}, y2: {y2}')
    
    def select_image():
        image_path = fd.askopenfilename()
        imageButton.config(text=image_path)

    tk.Button(root, text='Get x1, y1', command=get_xy1).pack()
    label1 = tk.Label(root, text='')
    label1.pack()
    tk.Button(root, text='Get x2, y2', command=get_xy2).pack()
    label2 = tk.Label(root, text='')
    label2.pack()

    imageButton = tk.Button(root, text='Select Image', command=select_image)
    imageButton.pack()


    root.mainloop()

if __name__ == '__main__':
    gui()