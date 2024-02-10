import tkinter as tk
from tkinter import ttk
from threading import Thread
import pyautogui
import pygame
from time import sleep
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(BASE_DIR, 'resource\\sound.wav'))

class App:
    def __init__(self, master):
        self.master = master
        master.geometry("300x250")
        master.resizable(width=False, height=False)
        master.title("메이플스토리 야누스 알리미")

        # Run button
        self.run_button = tk.Button(master, text="실행", command=self.toggle_script)
        self.run_button.pack(pady=10)

        # Confidence scale
        self.confidence_label, self.confidence_var, self.confidence_scale = self.create_scale("신뢰도:", 0.0, 1.0, 0.92, self.update_confidence)

        # Delay scale
        self.delay_label, self.delay_var, self.delay_scale = self.create_scale("딜레이 (초):", 1, 7, 1.0, self.update_delay_display)

        # Image selection using radio buttons
        self.image_var = tk.StringVar(value='sol.png')
        self.create_radio_button("솔 에르다", 'sol.png')
        self.create_radio_button("에르다 파운틴", 'fountain.png')

        self.is_running = False
        self.script_thread = None

        # Close window event handling
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_scale(self, label_text, scale_from, scale_to, default_value, command):
        label = tk.Label(self.master, text=label_text)
        label.pack()

        scale_var = tk.DoubleVar()
        scale = ttk.Scale(self.master, from_=scale_from, to=scale_to, orient="horizontal", length=200, variable=scale_var,
                          command=command)
        scale.set(default_value)
        scale.pack(pady=5)

        return label, scale_var, scale

    def create_radio_button(self, text, value):
        radio_button = tk.Radiobutton(self.master, text=text, variable=self.image_var, value=value)
        radio_button.pack()

    def on_closing(self):
        self.stop_script()
        self.master.destroy()

    def toggle_script(self):
        if self.is_running:
            self.stop_script()
        else:
            self.run_script()

    def run_script(self):
        if not self.is_running:
            self.is_running = True
            self.run_button.config(text="중지")
            confidence = self.confidence_var.get()
            delay = self.delay_var.get()
            selected_image = self.image_var.get()
            self.script_thread = Thread(target=self.main_loop, args=(confidence, delay, selected_image))
            self.script_thread.start()

    def stop_script(self):
        if self.is_running:
            self.is_running = False
            self.run_button.config(text="실행")
            # Wait for the script thread to complete
            if self.script_thread and self.script_thread.is_alive():
                self.script_thread.join()

    def main_loop(self, confidence, delay, selected_image):
        while self.is_running:
            try:
                pyautogui.locateCenterOnScreen(os.path.join(BASE_DIR, f'resource\\{selected_image}'), confidence=confidence)

                sleep(delay)  # Add delay before playing the sound
                pygame.mixer.music.play()
                print('감지됨')
            except pyautogui.ImageNotFoundException:
                print('실행 중')
                sleep(0.1)

    def update_confidence(self, *_):
        # Update confidence scale
        current_confidence = self.confidence_var.get()
        self.confidence_label.config(text=f"현재 신뢰도: {current_confidence:.2f}")

    def update_delay_display(self, *_):
        # Update delay scale
        current_delay = self.delay_var.get()
        self.delay_label.config(text=f"현재 딜레이: {current_delay:.1f} 초")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
