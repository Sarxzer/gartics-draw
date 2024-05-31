from PIL import Image
import pyautogui as pg
import keyboard as kb
import tkinter as tk
from tkinter import filedialog as fd

colorsHex = ['#000000', '#666666', '#0050cd', '#ffffff', '#aaaaaa', '#26c9ff', '#017420', '#990000', '#964112', '#11b03c', '#ff0013', '#ff7829', '#b0701c', '#99004e', '#cb5a57', '#ffc126', '#ff008f', '#feafa8']
colorsRGB = [(0, 0, 0), (102, 102, 102), (0, 80, 205), (255, 255, 255), (170, 170, 170), (38, 201, 255), (1, 116, 32), (153, 0, 0), (150, 65, 18), (17, 176, 60), (255, 0, 19), (255, 120, 41), (176, 112, 28), (153, 0, 78), (203, 90, 87), (255, 193, 38), (255, 0, 143), (254, 175, 168)]
colors = ['Black', 'Gray', 'Blue', 'White', 'Light Gray', 'Light Blue', 'Green', 'Dark Red', 'Brown', 'Light Green', 'Red', 'Orange', 'Dark Orange', 'Purple', 'Dark Beige', 'Yellow', 'Pink', 'Light Beige']

def remove_background(image: Image):
    img = image.convert("RGB")

    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] in range(215, 256) and item[1] in range(215, 256) and item[2] in range(215, 256):
            new_data.append((255, 255, 255))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img

def resize_image(image_path, box_width, box_height):
    original_image = Image.open(image_path)
    image_width, image_height = original_image.size
    image_aspect = image_width / image_height
    box_aspect = box_width / box_height

    if box_aspect > image_aspect:
        # Box is wider than image, so fit to height of box
        new_height = box_height
        new_width = int(new_height * image_aspect)
    else:
        # Box is taller than image, so fit to width of box
        new_width = box_width
        new_height = int(new_width / image_aspect)

    resized_image = original_image.resize((new_width, new_height))

    # Create a new image with the size of the box and paste the resized image into it at the center
    new_image = Image.new('RGB', (box_width, box_height), (255, 255, 255))
    new_image.paste(resized_image, ((box_width - new_width) // 2, (box_height - new_height) // 2))

    return new_image


def show_toast(message, duration=2000, mainwin=None):
    toast = tk.Toplevel()
    toast.overrideredirect(1)

    tk.Label(toast, text=message, bg="white", fg="black").pack()

    # Position the toast notification relative to the main window
    toast.update()  # Needed to ensure that the toast window has been drawn before getting its size199
    toast_width = toast.winfo_reqwidth()
    toast_height = toast.winfo_reqheight()
    x = mainwin.winfo_x() + mainwin.winfo_width() // 2 - toast_width // 2
    y = mainwin.winfo_y() + mainwin.winfo_height() // 2 - toast_height // 2
    toast.geometry(f"+{x}+{y}")

    # Style the toast notification
    toast.configure(bg="black", bd=1, relief=tk.SOLID)

    # Destroy the toast notification after a certain duration
    toast.after(duration, toast.destroy)

def draw(image_path, x1, y1, x2, y2, colors_pos, quality, root):
    if not image_path:
        show_toast('No image selected', 3000, root)
        return
    if x1 == 0 and y1 == 0:
        show_toast('x1, y1 not selected', 3000, root)
        return
    if x2 == 0 and y2 == 0:
        show_toast('x2, y2 not selected', 3000, root)
        return
    if not colors_pos:
        show_toast('Colors positions not selected', 3000, root)
        return
    
    # Create a palette with the colors of the list colorsRGB
    palette = Image.new('P', (1, 1))
    palette.putpalette(sum(colorsRGB, ()))

    image = remove_background(resize_image(image_path, x2-x1, y2-y1))
    image = image.resize((round((x2-x1)/quality), round((y2-y1)/quality)))
    image = image.quantize(colors=18, palette=palette).convert('RGB')

    current_color = 0
    for i in range(round((x2-x1)/quality)):
        for j in range(round((y2-y1)/quality)):
            if kb.is_pressed('esc'):
                show_toast('Drawing stopped', 3000, root)
                return
            pixel = image.getpixel((i, j))
            if pixel == (255, 255, 255):
                continue
            if pixel != colorsRGB[current_color]:
                current_color = colorsRGB.index(pixel)
                pg.click(colors_pos[current_color])
            pg.click(x1+(i*quality), y1+(j*quality))

def get_custom_color(pixel, btn_pos, r, g, b):
    pg.click(btn_pos[0], btn_pos[1])
    pg.click(r[0], r[1])
    pg.typewrite(str(pixel[0]))
    pg.click(g[0], g[1])
    pg.typewrite(str(pixel[1]))
    pg.click(b[0], b[1])
    pg.typewrite(str(pixel[2]))


def draw_perfect(image_path, x1, y1, x2, y2, quality, btn_pos, r, g, b, root):
    if not image_path:
        show_toast('No image selected', 3000, root)
        return
    if x1 == 0 and y1 == 0:
        show_toast('x1, y1 not selected', 3000, root)
        return
    if x2 == 0 and y2 == 0:
        show_toast('x2, y2 not selected', 3000, root)
        return
    if not btn_pos or not r or not g or not b:
        show_toast('Custom colors positions not selected', 3000, root)
        return
    
    image = remove_background(resize_image(image_path, x2-x1, y2-y1))
    image = image.resize((round((x2-x1)/quality), round((y2-y1)/quality)))

    current_color = 0
    for i in range(round((x2-x1)/quality)):
        for j in range(round((y2-y1)/quality)):
            if kb.is_pressed('esc'):
                show_toast('Drawing stopped', 3000, root)
                return
            pixel = image.getpixel((i, j))
            if pixel == (255, 255, 255):
                continue
            if pixel != current_color:
                current_color = pixel
                get_custom_color(pixel, btn_pos, r, g, b)
            pg.click(x1+(i*quality), y1+(j*quality))

colors_pos, image_path, x1, y1, x2, y2, quality, btn_pos, r, g, b= [], '', 0, 0, 0, 0, 1, [], [], [], []

def gui():
    root = tk.Tk()
    root.title('Gartics Drawing Bot')
    root.geometry('400x600')

    def get_xy1():
        global x1, y1
        kb.wait('space')
        x1, y1 = pg.position()
        label1.config(text=f'x1: {x1}, y1: {y1}')

    
    def get_xy2():
        global x2, y2
        kb.wait('space')
        x2, y2 = pg.position()
        label2.config(text=f'x2: {x2}, y2: {y2}')
    
    def select_image():
        global image_path
        image_path = fd.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff')]) or 'Select Image'
        imageButton.config(text=image_path)
    
    def get_color_at(x, y):
        screenshot = pg.screenshot()
        pixel = screenshot.getpixel((x, y))
        return '#{:02x}{:02x}{:02x}'.format(*pixel)

    def get_colors():
        global colors_pos
        x, y = [], []

        for i in range(18):
            colorLabel.config(text=f'Place the cursor on {colors[i]} and press space')
            root.update()
            kb.wait('space')
            while kb.is_pressed('space'):
                pass
            x_, y_ = pg.position()
            x.append(x_)
            y.append(y_)
        colors_pos = list(zip(x, y))
        colorLabel.config(text='Colors positions selected')

        saveButton.config(state=tk.NORMAL)
    
    def custom_color_pos():
        global btn_pos, r, g, b
        btn_pos, r, g, b = [], [], [], []

        customColorsLabel.config(text='Place the cursor on the color box and press space')
        root.update()
        kb.wait('space')
        while kb.is_pressed('space'):
            pass
        x, y = pg.position()
        btn_pos.extend([x, y])
        customColorsLabel.config(text='Place the cursor on the red input and press space')
        root.update()
        kb.wait('space')
        while kb.is_pressed('space'):
            pass
        x, y = pg.position()
        r.extend([x, y])
        customColorsLabel.config(text='Place the cursor on the green input and press space')
        root.update()
        kb.wait('space')
        while kb.is_pressed('space'):
            pass
        x, y = pg.position()
        g.extend([x, y])
        customColorsLabel.config(text='Place the cursor on the blue input and press space')
        root.update()
        kb.wait('space')
        while kb.is_pressed('space'):
            pass
        x, y = pg.position()
        b.extend([x, y])
        customColorsLabel.config(text='Custom color position selected')
        print(btn_pos)
        print(r)
        print(g)
        print(b)
    
    def save_settings():
        global colors_pos
        global x1, y1, x2, y2, image_path, quality, btn_pos, r, g, b
        savePath = fd.asksaveasfilename(filetypes=[('Text Files', '*.txt')], defaultextension='.txt', initialfile='gartic_bot_settings.txt') or 'Save Settings'
        if savePath != 'Save Settings':
            with open(savePath, 'w') as f:
                f.write(f'{x1},{y1}\n{x2},{y2}\n')
                f.write(image_path+'\n')
                f.write(f'{quality}\n')
                f.write(f'{btn_pos[0]},{btn_pos[1]}\n')
                f.write(f'{r[0]},{r[1]}\n')
                f.write(f'{g[0]},{g[1]}\n')
                f.write(f'{b[0]},{b[1]}\n')
                for pos in colors_pos:
                    f.write(f'{pos[0]},{pos[1]}\n')
    
    def load_settings():
        global colors_pos
        global x1, y1, x2, y2, image_path, quality, btn_pos, r, g, b
        loadPath = fd.askopenfilename(filetypes=[('Text Files', '*.txt')]) or 'Load Settings'
        if loadPath != 'Load Settings':
            try:
                with open(loadPath, 'r') as f:
                    x1, y1 = map(int, f.readline().strip().split(','))
                    x2, y2 = map(int, f.readline().strip().split(','))
                    image_path = f.readline().strip()
                    quality = int(f.readline().strip())
                    btn_pos = list(map(int, f.readline().strip().split(',')))
                    r = list(map(int, f.readline().strip().split(','))) 
                    g = list(map(int, f.readline().strip().split(','))) 
                    b = list(map(int, f.readline().strip().split(',')))
                    colors_pos = [tuple(map(int, line.strip().split(','))) for line in f]
                label1.config(text=f'x1: {x1}, y1: {y1}')
                label2.config(text=f'x2: {x2}, y2: {y2}')
                imageButton.config(text=image_path)
                colorLabel.config(text='Colors positions selected')
                customColorsLabel.config(text='Custom color position selected')
                drawQuality.set(quality)
                saveButton.config(state=tk.NORMAL)
            except:
                show_toast('Error loading settings', 3000, root)
        
    tk.Button(root, text='Get x1, y1', command=get_xy1).pack()
    label1 = tk.Label(root, text='')
    label1.pack()
    tk.Button(root, text='Get x2, y2', command=get_xy2).pack()
    label2 = tk.Label(root, text='')
    label2.pack()
    
    tk.Button(root, text='Select Colors Positions', command=get_colors).pack()
    colorLabel = tk.Label(root, text='')
    colorLabel.pack()

    saveButton = tk.Button(root, text='Save Settings', command=save_settings, state=tk.DISABLED)
    saveButton.pack()
    tk.Button(root, text='Load Settings', command=load_settings).pack()


    imageButton = tk.Button(root, text='Select Image', command=select_image)
    imageButton.pack()

    drawQuality = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, label='Draw Quality')
    drawQuality.pack()
    tk.Label(root, text='1: Slowest but best quality\n5: Fastest but worst quality').pack()

    tk.Label(root, text='Perfect Colors: The bot will use the exact colors of the image\nThis option is extremely slow').pack()

    customColorsPosition = tk.Button(root, text='Custom Colors Position', command=custom_color_pos)
    customColorsPosition.pack()
    customColorsLabel = tk.Label(root, text='')
    customColorsLabel.pack()

    tk.Button(root, text='Start Drawing', command=lambda: draw(image_path, x1, y1, x2, y2, colors_pos, drawQuality.get(), root)).pack()
    tk.Button(root, text='Start Drawing Perfect', command=lambda: draw_perfect(image_path, x1, y1, x2, y2, drawQuality.get(), btn_pos, r, g, b, root)).pack()


    root.mainloop()

if __name__ == '__main__':
    gui()