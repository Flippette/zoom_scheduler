import sys
import pyautogui
import subprocess
import json
import time
import datetime
import calendar
import threading

UIElements = json.load(open('./config/ui_elements.json'))
rooms = json.load(open('./config/rooms.json'))
schedule = json.load(open('./config/schedule.json'))
paths = json.load(open('./config/paths.json'))

for key in UIElements.keys():
  UIElements[key] = './assets/' + UIElements[key]

def process_exists(process_name):
  call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
  # use buildin check_output right away
  output = subprocess.check_output(call).decode()
  # check in last line for process name
  last_line = output.strip().split('\r\n')[-1]
  # because Fail message could be translated
  return last_line.lower().startswith(process_name.lower())

def waitForElement(element):
  try:
    temp = UIElements[element]
  except KeyError:
    return None
  elem = None
  while elem is None:
    time.sleep(0.1)
    elem = pyautogui.locateOnScreen(UIElements[element])
  return elem

def join(room):
  subprocess.Popen(args="", executable=paths['zoom'])
  join_btn = waitForElement('join')
  
  pyautogui.click(join_btn.left + join_btn.width / 2, join_btn.top + join_btn.height / 2)
  temp = waitForElement('join-box')
  pyautogui.typewrite(rooms[room]['id'])
  pyautogui.press('enter')
  temp = waitForElement('passcode')
  pyautogui.typewrite(rooms[room]['passwd'])
  pyautogui.press('enter')

def leave():
  leave0_btn = waitForElement('leave0')
  pyautogui.click(leave0_btn.left + leave0_btn.width / 2, leave0_btn.top + leave0_btn.height / 2)

  time.sleep(0.25)

  leave_btn = waitForElement('leave')
  pyautogui.click(leave_btn.left + leave_btn.width / 2, leave_btn.top + leave_btn.height / 2)

def get_weekday():
  threading.Timer(0.5, get_weekday).start()
  return calendar.day_name[datetime.datetime.today().weekday()][0:3].lower()

def __main__():
  join('physics')
  time.sleep(10)
  leave()

__main__()