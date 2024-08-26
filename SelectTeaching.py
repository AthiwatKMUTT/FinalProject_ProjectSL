import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Frame, Button, Label, messagebox
import subprocess
import sys
import os

windows = tk.Tk()
windows.title('Select Teaching Page')
windows.configure(bg='gray')

cap = cv2.VideoCapture(0)

#def set_windowed_fullscreen():
#    windows.update_idletasks()
#    window_width = windows.winfo_screenwidth()
#    window_height = windows.winfo_screenheight()
#    windows.geometry(f"{window_width}x{window_height}")
#    windows.state('zoomed')
#set_windowed_fullscreen()
def set_fullscreen():
    windows.attributes('-fullscreen', True)
    windows.resizable(False, False)
set_fullscreen()

bg_image = Image.open("./image/18.jpg")
bg_image_tk = ImageTk.PhotoImage(bg_image)

label = tk.Label(windows,
                 bg="#d0d0d0",
                 image=bg_image_tk,
                 compound='center',
                 fg="black",
                 font=("Helvetica", 24),
                 height=150,
                 bd=10,
                 relief='groove')
label.pack(side="top", fill="x")
label.pack(side="top", fill="x")

# Load the background image for the left bottom section
bg_image_leftbot = Image.open("./image/29.jpg")
bg_image_tk_leftbot = ImageTk.PhotoImage(bg_image_leftbot)

button_frame = Frame(windows)
button_frame.pack(side='left', fill='both', expand=True)

# Create a label with the background image inside the frame
label_leftbot = Label(button_frame, image=bg_image_tk_leftbot,bd=10,relief='groove')
label_leftbot.place(x=0, y=0, relwidth= 1,  relheight=1)
label_leftbot.image = bg_image_tk_leftbot  # Keep a reference to avoid garbage collection

# Load the background image into the canvas

button1 = Button(button_frame, text='Teach 1', font=("Helvetica", 24), width=20,bd=10,relief='groove', command=lambda: open_page('Teachingpage1.py'))
button1.pack(pady=(175,25), anchor='center', padx=(150, 150))
button2 = Button(button_frame, text='Teach 2', font=("Helvetica", 24), width=20,bd=10,relief='groove', command=lambda: open_page('Teachingpage2.py'))
button2.pack(pady=25, anchor='center', padx=(150, 150))
button3 = Button(button_frame, text='Teach 3', font=("Helvetica", 24), width=20,bd=10,relief='groove', command=lambda: open_page('Teachingpage3.py'))
button3.pack(pady=25, anchor='center', padx=(150, 150))
button4 = Button(button_frame, text='Teach 4', font=("Helvetica", 24), width=20,bd=10,relief='groove', command=lambda: open_page('Teachingpage4.py'))
button4.pack(pady=25, anchor='center', padx=(150, 150))
button5 = Button(button_frame, text='Teach 5', font=("Helvetica", 24), width=20,bd=10,relief='groove', command=lambda: open_page('Teachingpage5.py'))
button5.pack(pady=25, anchor='center', padx=(150, 150))

def open_page(page_script):
    script_path = os.path.join(os.path.dirname(__file__), page_script)
    if sys.platform == "win32":
        subprocess.Popen(["python", script_path], shell=True)
    else:
        subprocess.Popen(["python3", script_path])
    cap.release()
    windows.destroy()


# เพิ่มปุ่มย้อนกลับไปยังหน้าต่างหลัก
def back_to_main_page():
    script_path = os.path.join(os.path.dirname(__file__), 'main.py')
    if sys.platform == "win32":
        subprocess.Popen(["python", script_path], shell=True)
    else:
        subprocess.Popen(["python3", script_path])
    cap.release()
    windows.destroy()

back_button = Button(windows, text='Back to Main Page', font=("Helvetica", 12), width=20, command=back_to_main_page)
back_button.place(x=20, y=20)  # Place the button at the top left corner

def quit_program(event=None):
    if messagebox.askokcancel("Program", "Do you want to exit the program?"):
        cap.release()
        windows.quit()
windows.bind("<q>", quit_program)

windows.mainloop()
cap.release()
cv2.destroyAllWindows()
