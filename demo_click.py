import ctypes
import numpy as np
from PIL import ImageGrab
import cv2
import time
import pytesseract
import requests
from bs4 import BeautifulSoup
from math import pi, cos, sin

# ctypes.windll.user32.SetCursorPos(970, 682)
# ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
# ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up

# WINDOW = (810, 660, 1161, 1015) # for 4 letters
WINDOW = (810, 610, 1161, 965)
CENTER = (175, 175)
NUM_LETTERS = 5
RADIUS = 110
WINDOW_SIZE = 50


def getIndex(c, letters):
    c = c.lower()
    index = -1
    for i, l in letters:
        if c == l.lower():
            index = i
            letters.remove((i, l))
            break

    return index


def screenshot():
    screen = ImageGrab.grab(bbox=WINDOW)
    screen_np = np.array(screen)
    # cv2.imshow('window', screen_np)
    # cv2.waitKey(0)

    cv2.circle(screen_np, CENTER, 5, 0)

    letters = []
    centers = []

    starting_angle = pi/2

    for i in range(NUM_LETTERS):
        current_angle = i * (2 * pi) / NUM_LETTERS + starting_angle
        center = (int(CENTER[0] - RADIUS * cos(current_angle)),
                  int(CENTER[1] - RADIUS * sin(current_angle)))
        centers.append(center)
        cv2.rectangle(screen_np, (center[0] - WINDOW_SIZE, center[1] -
                                  WINDOW_SIZE, WINDOW_SIZE * 2, WINDOW_SIZE * 2), 5, 0)

        letter = screen.crop((center[0] - WINDOW_SIZE, center[1] -
                              WINDOW_SIZE, center[0] + WINDOW_SIZE, center[1] + WINDOW_SIZE))
        cv2.imwrite(f'letter{i}.png', np.array(letter))

        # letter tuning
        tesseract = pytesseract.image_to_string(letter, config='--psm 10')
        if tesseract[0] == '|' or tesseract[0] == ']' or tesseract[0] == '[' or tesseract[0] == '1':
            letter = 'I'
        else:
            letter = tesseract[0]

        letters.append(letter)

    cv2.imwrite('window.png', screen_np)
    letters = [(i, l) for i, l in enumerate(letters)]
    print(letters)
    return letters, centers


def solve(letters):
    req = requests.get(
        f'http://www.allscrabblewords.com/word-description/{letters}')
    soup = BeautifulSoup(req.content, 'html.parser')
    links = soup.findAll('a')

    words = []

    for link in links:
        if '/word-description/' in link['href'] and len(link.text) <= len(letters):
            words.append(link.text)

    return words


def pass_input(words, centers):
    for word in words:
        print(f"inputting {word}")
        counter = 0
        temp_letters = letters.copy()
        for char in word:
            i = getIndex(char, temp_letters)
            center = centers[i]

            ctypes.windll.user32.SetCursorPos(
                center[0] + WINDOW[0], center[1] + WINDOW[1])
            if counter == 0:
                ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
            counter += 1
            time.sleep(0.05)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
        time.sleep(0.05)


if __name__ == '__main__':
    # start the game
    time.sleep(1)
    print('activating')
    letters, centers = screenshot()
    words = solve(letters)
    pass_input(words, centers)
