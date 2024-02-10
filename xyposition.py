import pyautogui

#좌표 구하기
# 
px, py = pyautogui.position()
print(pyautogui.position())

#스크린샷 찍는방법 (파일이름, 시작점, width,height)
pyautogui.screenshot('fountain.png', region=(2119,103, 30, 30))
#pyautogui.screenshot('7.png', region=(137,783, 80, 80))
#loc=pyautogui.locateCenterOnScreen(r'resource/7.png')
#pyautogui.moveTo(loc)