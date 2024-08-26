import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Frame, Button, Label, messagebox
import subprocess
import sys
import os
import random
import pygame
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model


# Initialize pygame for playing sounds
pygame.mixer.init()

# Function to play sound
def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

# Tkinter window setup
windows = tk.Tk()
windows.title('Training Page')
windows.configure(bg='#f0f0f0')

cap = cv2.VideoCapture(0)

# Function for fullscreen
def set_fullscreen():
    windows.attributes('-fullscreen', True)
    windows.resizable(False, False)
set_fullscreen()

# Load background image
bg_image = Image.open("./image/20.jpg")
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

# Load Keras model
model = load_model('select-mode/mode1/model/Num15.h5')

# Global variables
vocabulary_words = ["1", "2", "3", "4", "5"]
sound_file = ["select-mode/mode1/Cheer1.mp3", "select-mode/mode1/Cheer2.mp3", "select-mode/mode1/Cheer3.mp3"]
used_words = []
word_count = 0
scoreN = 0
random_word = None
countdown_id = None

def check_answer(predicted_character):
    global scoreN
    global word_count
    global countdown_id

    #ตรวจสอบว่าเกมจบหรือยัง
    if is_game_over:
        return  # หากเกมจบแล้ว ไม่ทำอะไรในฟังก์ชันนี้

    if word_count <= 5:
        if predicted_character == random_word:
            scoreN += 1
            play_sound(random.choice(sound_file))
            update_vocabulary()
            windows.after_cancel(countdown_id)
            countdown(9)
    else:
        show_final_score() 


# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)
# Labels for model predictions
labels_dict = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5'}

label_img = tk.Label(windows)
label_img.pack(side="left", fill='both', expand=True)

is_game_over = False

def update_frame():
    global countdown_id

    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    if ret:
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,  # image to draw
                    hand_landmarks,  # model output
                    mp_hands.HAND_CONNECTIONS,  # hand connections
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            # Prediction
            data_aux = np.expand_dims(np.array(data_aux), axis=0)  # Add batch dimension
            prediction = model.predict(data_aux)
            predicted_class = np.argmax(prediction, axis=1)[0]  # Get the highest prediction

            predicted_character = labels_dict.get(predicted_class, 'Unknown')

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame_rgb, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)

            check_answer(predicted_character)
            
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        label_img.imgtk = imgtk
        label_img.configure(image=imgtk)
    else:
        img = Image.new('RGB', (768, 576), color='black')
        imgtk = ImageTk.PhotoImage(image=img)
        label_img.imgtk = imgtk
        label_img.configure(image=imgtk)

    label_img.pack(anchor="center",padx=(100,100))
    label_img.after(10, update_frame)


update_frame()

# UI elements
bg_image_leftbot = Image.open("./image/26.jpg")
bg_image_tk_leftbot = ImageTk.PhotoImage(bg_image_leftbot)

button_frame = Frame(windows)
button_frame.pack(side='right', fill='both', expand=True)

label_leftbot = Label(button_frame, image=bg_image_tk_leftbot, bd=10, relief='groove')
label_leftbot.pack(fill='both',anchor="center")

word_count_label = Label(label_leftbot, text="1/5", fg="white", bg="black", font=("Helvetica", 36), bd=10, relief='groove', padx=110)
word_count_label.place(relx=0.5, rely=0.2, anchor="center")

word_label = Label(label_leftbot, text="Word: ", fg="white", bg="black", font=("Helvetica", 36), bd=10, relief='groove', padx=90)
word_label.place(relx=0.5, rely=0.4, anchor="center")

timer_label = Label(label_leftbot, text="Timer: 30s", fg="white", bg="black", font=("Helvetica", 36), bd=10, relief='groove', padx=90)
timer_label.place(relx=0.5, rely=0.6, anchor="center")

score_label = Label(label_leftbot, text="Score: ", fg="white", bg="black", font=("Helvetica", 36), bd=10, relief='groove', padx=110)
score_label.place(relx=0.5, rely=0.8, anchor="center")

def show_final_score():
    global is_game_over
    is_game_over = True  # ตั้งค่า is_game_over เป็น True เพื่อระบุว่าเกมจบแล้ว

    #ลบ Label และ Button ที่เกี่ยวข้องกับคำตอบออก
    word_count_label.place_forget()
    word_label.place_forget()
    timer_label.place_forget()
    score_label.place_forget()

    # แสดงคะแนนสุดท้าย
    final_score_label = Label(label_leftbot, text=f"Final Score: {scoreN}/5", fg="white", bg="black", 
                              font=("Helvetica", 36), bd=10, relief='groove', padx=110)
    final_score_label.place(relx=0.5, rely=0.4, anchor="center")

    # ปุ่มสำหรับเริ่มใหม่
    start_again_button = Button(label_leftbot, text="Start Again", font=("Helvetica", 24), command=start_again)
    start_again_button.place(relx=0.35, rely=0.6, anchor="center")

    # ปุ่มสำหรับไปยังหน้าถัดไป
    next_button = Button(label_leftbot, text="Next", font=("Helvetica", 24), command=TriannigpageStage2)
    next_button.place(relx=0.65, rely=0.6, anchor="center")

def start_again():
    global is_game_over, word_count, scoreN, used_words, random_word
    is_game_over = False
    word_count = 0
    scoreN = 0
    used_words = []
    random_word = None

    #ลบคะแนนสุดท้ายและปุ่มออก
    for widget in label_leftbot.winfo_children():
        widget.place_forget()

    #นำ UI กลับมาใหม่
    word_count_label.place(relx=0.5, rely=0.2, anchor="center")
    word_label.place(relx=0.5, rely=0.4, anchor="center")
    timer_label.place(relx=0.5, rely=0.6, anchor="center")
    score_label.place(relx=0.5, rely=0.8, anchor="center")

    update_vocabulary()
    countdown(9)

def update_vocabulary():
    global word_count
    global used_words
    global random_word
    global countdown_id

    if word_count < 5:
        while True:
            random_word = random.choice(vocabulary_words)
            if random_word not in used_words:
                used_words.append(random_word)
                break
        word_count += 1
    else:
        windows.after_cancel(countdown_id)
        countdown(99999)
        show_final_score()

def countdown(time_left):
    global word_count
    global scoreN
    global countdown_id
    
    if time_left >= 0:
        timer_label.config(text=f"Timer: {time_left}s")
        word_count_label.config(text=f"{word_count}/5")
        word_label.config(text=f"Word: {random_word}")
        score_label.config(text=f"Score: {scoreN}")
        countdown_id = windows.after(1000, countdown, time_left - 1)
    else:
        update_vocabulary()
        countdown_id = windows.after(3000, countdown, 9)

update_vocabulary()
countdown(9)

def TriannigpageStage2():
    script_path = os.path.join(os.path.dirname(__file__), 'TriannigpageStage2.py')
    if sys.platform == "win32":
        subprocess.Popen(["python", script_path], shell=True)
    else:
        subprocess.Popen(["python3", script_path])
    cap.release()
    windows.destroy()
    
def backToMain():
    script_path = os.path.join(os.path.dirname(__file__), 'main.py')
    if sys.platform == "win32":
        subprocess.Popen(["python", script_path], shell=True)
    else:
        subprocess.Popen(["python3", script_path])
    cap.release()
    windows.destroy()

back_button = Button(windows, text='Back to Main Page', font=("Helvetica", 12), width=20, command=backToMain)
back_button.place(x=20, y=20)

def quit_program(event=None):
    if messagebox.askokcancel("Program", "Do you want to exit the program?"):
        cap.release()
        windows.quit()
        
windows.bind("<q>", quit_program)

windows.mainloop()
cap.release()
cv2.destroyAllWindows()
