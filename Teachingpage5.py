import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Frame, Button, Label, messagebox
import subprocess
import sys
import os

windows = tk.Tk()
windows.title('Teaching Page')
windows.configure(bg='white')  # Change the overall background color

cap = cv2.VideoCapture(0)

def set_fullscreen():
    windows.attributes('-fullscreen', True)
    windows.resizable(False, False)
set_fullscreen()

bg_image = Image.open("./image/17.jpg")
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
label.grid(row=0, column=0, columnspan=2, sticky="ew")  # Place label at the top

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        label_img.imgtk = imgtk
        label_img.configure(image=imgtk)
    else:
        img = Image.new('RGB', (768, 576), color='black')
        imgtk = ImageTk.PhotoImage(image=img)
        label_img.imgtk = imgtk
        label_img.configure(image=imgtk)
        
    label_img.after(10, update_frame)

# Change the background color of the camera feed label
label_img = tk.Label(windows, bg="white")  # Set background to white
label_img.grid(row=1, column=0, padx=50, pady=(0, 10), sticky="nsew")  # Center camera feed

update_frame()

def open_video_window(video_path):
    global video_cap
    global video_window
    global video_names
    global current_index

    # Close the existing video window if one is open
    if video_window is not None:
        video_window.destroy()

    video_window = tk.Toplevel()
    video_window.title("Video Player")
    
    # Create a VideoCapture object
    video_cap = cv2.VideoCapture(video_path)
    
    # Get the original video resolution
    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Calculate the position to center the video window
    screen_width = windows.winfo_screenwidth()
    screen_height = windows.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set the window size and position
    video_window.geometry(f"{width}x{height}+{x}+{y}")

    # Create a canvas with the video resolution
    video_canvas = tk.Canvas(video_window, width=width, height=height)
    video_canvas.pack(fill='both', expand=True)

    fps = video_cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30  # Fallback to default if FPS cannot be determined

    def update_video_frame():
        ret, frame = video_cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            video_canvas.create_image(0, 0, anchor='nw', image=img_tk)
            video_canvas.imgtk = img_tk
            video_canvas.update_idletasks()
            video_canvas.after(int(1000 / fps), update_video_frame)  # Use video FPS for timing
        else:
            video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            update_video_frame()

    update_video_frame()

def next_video(event=None):
    global current_index
    if video_window is not None:
        video_window.destroy()
    current_index = (current_index + 1) % len(video_names)
    open_video_window(video_names[current_index])

def previous_video(event=None):
    global current_index
    if video_window is not None:
        video_window.destroy()
    current_index = (current_index - 1) % len(video_names)
    open_video_window(video_names[current_index])

def quit_program(event=None):
    if messagebox.askokcancel("Program", "Do you want to exit the program?"):
        cap.release()
        windows.quit()

windows.bind("<q>", quit_program)

windows.bind("<d>", next_video)
windows.bind("<a>", previous_video)

def back_to_main_page():
    script_path = os.path.join(os.path.dirname(__file__), 'main.py')
    if sys.platform == "win32":
        subprocess.Popen(["python", script_path], shell=True)
    else:
        subprocess.Popen(["python3", script_path])
    cap.release()
    windows.destroy()

back_button = Button(windows, text='Back to Main Page', font=("Helvetica", 12), width=20, command=back_to_main_page)
back_button.place(x=20, y=20)

button_frame = Frame(windows, bg='black')  # Change button frame background color
button_frame.grid(row=1, column=1, padx=50, pady=(0, 20), sticky="nsew")  # Center buttons

# Set background image for button_frame
bg_image_button_frame = Image.open("./image/29.jpg")
bg_image_button_frame_tk = ImageTk.PhotoImage(bg_image_button_frame)
bg_label = Label(button_frame, image=bg_image_button_frame_tk)
bg_label.place(relwidth=1, relheight=1)

# Centering the content in the grid
windows.grid_rowconfigure(1, weight=1)  # Camera feed row
windows.grid_rowconfigure(2, weight=0)  # Add this for the instructions row
windows.grid_columnconfigure(0, weight=1)  # Center column
windows.grid_columnconfigure(1, weight=1)  # Center column

# Centering the buttons inside the button_frame
button_frame.grid_rowconfigure(0, weight=1)
button_frame.grid_rowconfigure(6, weight=1)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

# List of video names
video_names = ["./videomode5/01.mp4", "./videomode5/02.mp4", "./videomode5/03.mp4", "./videomode5/04.mp4", "./videomode5/05.mp4",
               "./videomode5/06.mp4", "./videomode5/07.mp4", "./videomode5/08.mp4", "./videomode5/09.mp4", "./videomode5/10.mp4"]

current_index = 0
video_window = None
video_cap = None

# Creating buttons in 2x5 grid (5 rows per column)
button_labels = ["24H", "Allnight", "Afternoon", "Evening", "Midday", "Midnight", "Morning", "Night time", "Time", "Twilight"]

for i, label in enumerate(button_labels):
    # Calculate the row and column positions
    row = i % 5
    column = i // 5

    # Create a button for each label
    button = Button(button_frame, text=label, font=("Helvetica", 18),
                    command=lambda vn=video_names[i]: open_video_window(vn),
                    width=15, height=2)
    
    # Place the button in the grid
    button.grid(row=row, column=column, padx=20, pady=10)

# Adjust the grid configuration for the button_frame
button_frame.grid_rowconfigure(0, weight=1)
button_frame.grid_rowconfigure(1, weight=1)
button_frame.grid_rowconfigure(2, weight=1)
button_frame.grid_rowconfigure(3, weight=1)
button_frame.grid_rowconfigure(4, weight=1)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)


# Instructions label
instructions = (
    "วิธีการใช้งาน\n"
    "สมารถกดเลือกดูวิดีโอสอน ตามคำศัพท์ที่ต้องการ\n"
    "- กด D เพื่อดูวิดีโอถัดไป\n"
    "- กด A เพื่อย้อนกลับ"
)
instructions_label = Label(windows, text=instructions, font=("Helvetica", 18), bg="white", justify='center')
instructions_label.grid(row=2, column=0, columnspan=2, pady=(20, 100), sticky="ew")  # Increase top padding

windows.mainloop()
cap.release()
cv2.destroyAllWindows()
