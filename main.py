import tkinter as tk
import logging
from threading import Thread
import pyautogui
import pygame
from time import sleep
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(BASE_DIR, 'resource\\sound.wav'))


#Logging Conf
log = logging.getLogger()
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)

class App:
    def __init__(self, master):
        self.master = master
        self.image_var = tk.StringVar(value='sol.png')  # Initialize image_var
        master.geometry("300x300")
        master.resizable(width=False, height=False)
        master.title("메이플스토리 야누스 알리미")

        # 실행
        self.run_button = tk.Button(master, text="실행", command=self.toggle_script)
        self.run_button.pack(pady=5)  # Increase the vertical spacing

        # 신뢰도
        # 라벨
        self.confidence_label = tk.Label(master, text="신뢰도:")
        self.confidence_label.pack(pady=0)  # Increase the vertical spacing

        # 스케일 바
        self.confidence_scale = tk.Scale(master, from_=0.0, to=1.0, orient="horizontal", length=200, resolution=0.01)
        self.confidence_scale.set(0.92)  # 기본 신뢰도 설정
        self.confidence_scale.pack(pady=0)  # Increase the vertical spacing

        # 딜레이
        # 라벨
        self.delay_label = tk.Label(master, text="딜레이 (초):")
        self.delay_label.pack(pady=2)  # Increase the vertical spacing

        # 스케일 바
        self.delay_scale = tk.Scale(master, from_=0.0, to=8.0, orient="horizontal", length=200, resolution=0.1)
        self.delay_scale.set(0.0)  # 기본 딜레이 설정
        self.delay_scale.pack(pady=2)  # Increase the vertical spacing

        self.delay_display = tk.Label(master, text="현재 딜레이: 1.0 초")
        self.delay_display.pack(pady=2)  # Increase the vertical spacing

        self.image_options = {
            '솔 에르다 1~10레벨 기준': 'sol.png',
            '솔 에르다 30레벨 기준': 'sol_30.png',
            '에르다 파운틴': 'fountain.png',
        }

        for text, value in self.image_options.items():
            radio_button = tk.Radiobutton(master, text=text, variable=self.image_var, value=value)
            radio_button.pack(pady=2)

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
                log.info('감지됨')
            except pyautogui.ImageNotFoundException:
                log.info('%s',delay)
                log.info('confidence : ' + str(confidence))
                log.info('selected_image :' + selected_image)
                log.info('실행 중')
                sleep(0.3)

    def update_delay_display(self, *_):
        current_delay = self.delay_scale.get()
        self.delay_display.config(text=f"현재 딜레이: {current_delay:.1f} 초")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.delay_scale.config(command=app.update_delay_display)  # 연결된 함수 추가
    root.mainloop()
