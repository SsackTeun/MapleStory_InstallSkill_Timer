import tkinter as tk
from tkinter import filedialog
import logging
from threading import Thread
import pyautogui
import pygame
from time import sleep, time
import os
import keyboard

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pygame.mixer.init()

# Logging Conf
log = logging.getLogger()
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)


class App:
    def __init__(self, master):
        self.master = master
        self.is_running = False  # Add this line to define is_running attribute
        self.image_var = tk.StringVar(value='sol_L10_Time10.png')  # Initialize image_var
        self.sound_file_path = os.path.join(BASE_DIR, 'resource', 'sound.wav')

        self.alarm_sound_file_path = os.path.join(BASE_DIR, 'resource', '탁상시계.wav')

        row_counter = 0 #row_counter 초기화

        master.geometry("550x400")
        master.resizable(width=False, height=False)
        master.title("v1.1 메이플스토리 설치기 타이머")

        keyboard.add_hotkey('F11', lambda: self.set_timer(15))
        keyboard.add_hotkey('F12', lambda: self.set_timer(30))

        # Create a frame to hold the divided layout
        divided_frame = tk.Frame(master, bd=1, relief=tk.GROOVE)
        divided_frame.grid(row=0, column=0, padx=10, pady=10)

        # Configure the columns to have equal weight
        divided_frame.columnconfigure(0, weight=1)
        divided_frame.columnconfigure(1, weight=1)

        # Left side (Controls)
        controls_frame = tk.Frame(divided_frame, bd=0, relief=tk.GROOVE)
        controls_frame.grid(row=0, column=0)

        # 실행
        self.run_button = tk.Button(controls_frame, text="실행", command=self.toggle_script, bd=5, relief=tk.GROOVE)
        self.run_button.grid(row=0, column=0, padx=5, pady=15)

        # 사운드 파일 선택 버튼
        self.sound_button = tk.Button(controls_frame, text="사운드 파일 선택", command=self.choose_sound_file, bd=5, relief=tk.GROOVE)
        self.sound_button.grid(row=0, column=1, padx=5, pady=15)

        # 현재 선택된 파일 이름 표시 Label
        self.selected_file_label = tk.Label(controls_frame, text=f"현재 선택된 파일: {os.path.basename(self.sound_file_path)}", bd=0, relief=tk.GROOVE)
        self.selected_file_label.grid(row=0, column=2, padx=5, pady=15)

        # 신뢰도
        # 라벨
        self.confidence_label = tk.Label(controls_frame, text="유사도 :", bd=0, relief=tk.GROOVE)
        self.confidence_label.grid(row=1, column=0, pady=5)

        # 스케일 바
        self.confidence_scale = tk.Scale(controls_frame, from_=0.92, to=1.0, orient="horizontal", length=200, resolution=0.01, bd=2, relief=tk.GROOVE)
        self.confidence_scale.set(0.96)  # 기본 신뢰도 설정
        self.confidence_scale.grid(row=1, column=1, pady=5)

        # 딜레이
        # 라벨
        self.delay_label = tk.Label(controls_frame, text="감지 후 소리 \n지연 딜레이 (초) :", bd=0, relief=tk.GROOVE)
        self.delay_label.grid(row=2, column=0, pady=5)

        # 스케일 바
        self.delay_scale = tk.Scale(controls_frame, from_=0.0, to=10.0, orient="horizontal", length=200, resolution=0.1, bd=2, relief=tk.GROOVE)
        self.delay_scale.set(0.0)  # 기본 딜레이 설정
        self.delay_scale.grid(row=2, column=1, pady=5)

        # Image Options
        self.image_options = {
            '솔 야누스 1~10레벨 기준 10초 남음 기준': 'sol_L10_Time10.png',
            '솔 야누스 30레벨 기준 10초 남음 기준': 'sol_L30_Time10.png',
            '솔 야누스 1~10레벨 기준 20초 남음 기준': 'sol_L10_Time20.png',
            '에르다 파운틴': 'fountain.png',
        }

        row_counter = 4
        for text, value in self.image_options.items():
            radio_button = tk.Radiobutton(controls_frame, text=text, variable=self.image_var, value=value, bd=0,
                                          relief=tk.GROOVE, anchor="w")
            radio_button.grid(row=row_counter, column=0, columnspan=2, padx=5, pady=2, sticky="w")
            row_counter += 1

        # Right side (Image)
        image_frame = tk.Frame(divided_frame, bd=0, relief=tk.GROOVE)
        image_frame.grid(row=0, column=2, padx=10)

        self.createdBy_label = tk.Label(controls_frame, text="created by : 방금나갔어(노바)")
        self.createdBy_label.grid(row=6, column=2, pady=5)

        # Corrected image loading
        self.createdBy_img = tk.PhotoImage(file=os.path.join(BASE_DIR, f'resource\\charactor.png'))
        print(os.path.join(BASE_DIR, f'resource\\charactor.png'))
        self.createdBy_img_label = tk.Label(controls_frame, image=self.createdBy_img, bd=0, relief=tk.GROOVE)
        self.createdBy_img_label.grid(row=2, column=2, pady=5, padx=5)

        # 타이머 추가
        self.timer_end_time = 0  # 타이머 종료 시간 초기화
        self.is_timer_running = False  # 타이머 실행 상태 초기화

        # 타이머 버튼 추가 (기존 UI 구성 코드에 추가)
        # __init__ 메소드 내에서
        self.timer_label = tk.Label(controls_frame, text="남은 시간: 00:00:00", bd=5, relief=tk.GROOVE)
        self.timer_label.grid(row=8, column=0, padx=5, pady=5)
        row_counter += 1

        self.timer_30m_button = tk.Button(controls_frame, text="30분 타이머 시작", command=lambda: self.set_timer(30), bd=5,
                                          relief=tk.GROOVE)
        self.timer_30m_button.grid(row=8, column=1, padx=5, pady=5)
        row_counter += 1

        self.timer_15m_button = tk.Button(controls_frame, text="15분 타이머 시작", command=lambda: self.set_timer(15), bd=5,
                                          relief=tk.GROOVE)
        self.timer_15m_button.grid(row=8, column=2, padx=5, pady=5)
        row_counter += 1

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
                pyautogui.locateCenterOnScreen(os.path.join(BASE_DIR, f'resource\\{selected_image}'),
                                               confidence=confidence)
                sleep(delay)  # 딜레이 추가
                pygame.mixer.music.load(self.sound_file_path)
                pygame.mixer.music.play()
                log.info('감지됨')
                sleep(5)
            except pyautogui.ImageNotFoundException:
                log.info('%s', delay)
                log.info('confidence : ' + str(confidence))
                log.info('selected_image :' + selected_image)
                log.info('실행 중')
                sleep(0.3)

    def choose_sound_file(self):
        new_sound_file_path = filedialog.askopenfilename(initialdir=os.path.join(BASE_DIR, 'resource'))
        if new_sound_file_path:
            self.sound_file_path = new_sound_file_path
            self.selected_file_label.config(text=f"현재 선택된 파일: {os.path.basename(self.sound_file_path)}")

    def set_timer(self, minutes):
        self.timer_end_time = time() + minutes * 60
        self.is_timer_running = True
        self.check_timer()

    def check_timer(self):
        if self.is_timer_running:
            remaining = int(self.timer_end_time - time())
            if remaining <= 0:
                self.is_timer_running = False
                self.timer_label.config(text="남은 시간: 00:00:00")  # 타이머 완료 시 레이블 리셋
                pygame.mixer.music.load(self.alarm_sound_file_path)
                pygame.mixer.music.play()
                log.info('타이머 완료')
            else:
                mins, secs = divmod(remaining, 60)
                hours, mins = divmod(mins, 60)
                self.timer_label.config(text=f"남은 시간: {hours:02d}:{mins:02d}:{secs:02d}")
                self.master.after(1000, self.check_timer)  # 1초 후에 다시 체크


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
