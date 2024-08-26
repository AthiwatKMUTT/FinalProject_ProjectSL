import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Frame, Button, Label, messagebox
import subprocess
import sys
import os

def start_main_page():
    windows = tk.Tk()
    windows.title('Program Test 01')
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

    # Load the background image
    bg_image = Image.open("./image/4.jpg")
   
    
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    label = tk.Label(windows,
                     bg="#d0d0d0",
                     image=bg_image_tk,
                     compound='center',
                     fg="black",
                     font=("Helvetica", 48),
                     height=150,
                     bd=10,
                     relief='groove')
    label.pack(side="top", fill="x")
    label.image = bg_image_tk  # Keep a reference to avoid garbage collection

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label_img.imgtk = imgtk
            label_img.configure(image=imgtk)
        else:
            # If camera is not available, display a black screen
            img = Image.new('RGB', (768, 576), color='black')  # Adjust size as needed
            imgtk = ImageTk.PhotoImage(image=img)
            label_img.imgtk = imgtk
            label_img.configure(image=imgtk)

        label_img.after(10, update_frame)

    label_img = tk.Label(windows)
    label_img.pack(side="left", fill='both', expand=True)

    update_frame()

    # Load the background image for the left bottom section
    bg_image_leftbot = Image.open("./image/1.jpg")
    bg_image_tk_leftbot = ImageTk.PhotoImage(bg_image_leftbot)

    button_frame = Frame(windows)
    button_frame.pack(side='right', fill='both', expand=True)

    # Create a label with the background image inside the frame
    label_leftbot = Label(button_frame, image=bg_image_tk_leftbot,bd=10,relief='groove')
    label_leftbot.place(x=0, y=0, relwidth= 1,  relheight=1)
    label_leftbot.image = bg_image_tk_leftbot  # Keep a reference to avoid garbage collection

    button1 = Button(button_frame, text='เรียนรู้ภาษามือ', font=("Helvetica", 24), width=20, command=lambda: open_page('SelectTeaching.py'))
    button1.pack(pady=(int((windows.winfo_screenheight() / 4)), 10), anchor='center', padx=(150, 150))
    button2 = Button(button_frame, text='ท้าทายภาษามือ', font=("Helvetica", 24), width=20, command=lambda: open_page('SelectChallenge.py'))
    button2.pack(pady=50, anchor='center', padx=(150, 150))
    button3 = Button(button_frame, text='ออกจากโปรแกรม', font=("Helvetica", 24), width=20, command=lambda: quit_program())
    button3.pack(anchor='center', padx=(150, 150))

    def open_page(page_script):
        script_path = os.path.join(os.path.dirname(__file__), page_script)
        if sys.platform == "win32":
            subprocess.Popen(["python", script_path], shell=True)
        else:
            subprocess.Popen(["python3", script_path])
        cap.release()
        windows.destroy()

    def quit_program(event=None):
        if messagebox.askokcancel("Program", "Do you want to exit the program?"):
            cap.release()
            windows.quit()
    windows.bind("<q>", quit_program)
    
    #if not cap.isOpened():
    #    messagebox.showerror("Error", "Unable to access camera. Displaying black screen.")
    #    update_frame()  # Display black screen initially

    windows.mainloop()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_main_page()
