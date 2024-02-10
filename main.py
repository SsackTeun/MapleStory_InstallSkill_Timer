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

        self.run_button = tk.Button(master, text="실행", command=self.toggle_script)
        self.run_button.pack(pady=10)

        self.confidence_label = tk.Label(master, text="신뢰도:")
        self.confidence_label.pack()

        self.confidence_scale = tk.Scale(master, from_=0.0, to=1.0, orient="horizontal", length=200, resolution=0.01)
        self.confidence_scale.set(0.92)  # 기본 신뢰도 설정
        self.confidence_scale.pack(pady=5)

        self.delay_label = tk.Label(master, text="딜레이 (초):")
        self.delay_label.pack()

        self.delay_var = tk.DoubleVar()
        self.delay_scale = ttk.Scale(master, from_=1, to=7, orient="horizontal", length=200, variable=self.delay_var)
        self.delay_scale.set(1.0)  # 기본 딜레이 설정
        self.delay_scale.pack(pady=5)

        self.delay_display = tk.Label(master, text="현재 딜레이: 1.0 초")
        self.delay_display.pack()

        self.image_var = tk.StringVar(value='sol.png')
        self.sol_radio = tk.Radiobutton(master, text="솔 에르다", variable=self.image_var, value='sol.png')
        self.sol_radio.pack()

        self.fountain_radio = tk.Radiobutton(master, text="에르다 파운틴", variable=self.image_var, value='fountain.png')
        self.fountain_radio.pack()

        self.is_running = False

        # 창 닫기 이벤트 처리
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

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
            confidence = self.confidence_scale.get()
            delay = self.delay_scale.get()
            selected_image = self.image_var.get()
            self.script_thread = Thread(target=self.main_loop, args=(confidence, delay, selected_image))
            self.script_thread.start()

    def stop_script(self):
        if self.is_running:
            self.is_running = False
            self.run_button.config(text="실행")
            # 스크립트 스레드가 완료될 때까지 대기
            if self.script_thread.is_alive():
                self.script_thread.join()

    def main_loop(self, confidence, delay, selected_image):
        while self.is_running:
            try:
                pyautogui.locateCenterOnScreen(os.path.join(BASE_DIR, f'resource\\{selected_image}'), confidence=confidence)
                
                sleep(delay)  # 딜레이 추가
                pygame.mixer.music.play()
                print('감지됨')
            except pyautogui.ImageNotFoundException:
                print('실행 중')
                sleep(0.1)

    def update_delay_display(self, *_):
        current_delay = self.delay_scale.get()
        self.delay_display.config(text=f"현재 딜레이: {current_delay:.1f} 초")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.delay_scale.config(command=app.update_delay_display)  # 연결된 함수 추가
    root.mainloop()
