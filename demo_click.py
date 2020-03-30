import ctypes
import numpy as np
from PIL import ImageGrab
import cv2
import time
import pytesseract
import requests
from bs4 import BeautifulSoup
from math import pi, cos, sin

# start the game
time.sleep(1)

# ctypes.windll.user32.SetCursorPos(970, 682)
# ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
# ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up

SCREEN_AREA = (830, 640, 1125, 940)
# SCREEN_AREA = (830, 605, 1120, 900)
CENTER = (148, 148)
NUM_LETTERS = 5

screen = ImageGrab.grab(bbox=SCREEN_AREA)
screen_np = np.array(screen)
# cv2.imshow('window', screen)
# cv2.waitKey(0)

# centers = [(150, 54), (70, 190), (227, 192)]
centers = []
starting_angle = pi / 2

while len(centers) < NUM_LETTERS:
    centers.append((int(CENTER[0] - 95 * cos(starting_angle)),
                    int(CENTER[1] - 95 * sin(starting_angle))))
    starting_angle += 2 * pi / NUM_LETTERS

for center in centers:
    cv2.circle(screen_np, (int(center[0]), int(center[1])), 5, 0)
cv2.imwrite('test.png', screen_np)

letters = []

counter = 0
for center in centers:
    letter = screen.crop(
        (center[0] - 30, center[1] - 30, center[0] + 30, center[1] + 30))
    letter = letter.convert('L')

    # tuning
    for x in range(letter.width):
        for y in range(letter.height):
            # for the given pixel at w,h, lets check its value against the threshold
            # note that the first parameter is actually a tuple object
            if letter.getpixel((x, y)) < 100:
                # lets set this to zero
                letter.putpixel((x, y), 0)
            else:
                # otherwise lets set this to 255
                letter.putpixel((x, y), 255)

    cv2.imwrite(f'image{counter}.jpg', np.array(letter))
    tesseract = pytesseract.image_to_string(letter, config='--psm 10')
    if tesseract[0] == '|' or tesseract[0] == ']' or tesseract[0] == '[' or tesseract[0] == '1':
        letters.append('I')
    else:
        letters.append(tesseract[0])
    counter += 1

letters = [(i, l) for i, l in enumerate(letters)]
temp_letters = letters.copy()
print(letters)

req = requests.get(
    f'http://www.allscrabblewords.com/word-description/{letters}')
soup = BeautifulSoup(req.content, 'html.parser')
links = soup.findAll('a')

words = []

for link in links:
    if '/word-description/' in link['href'] and len(link.text) <= len(letters):
        words.append(link.text)

def getIndex(c):
    c = c.lower()
    index = -1
    for i, l in temp_letters:
        if c == l.lower():
            index = i
            temp_letters.remove((i, l))
            break

    return index

# print(getIndex('a'))
# print(getIndex('a'))
# print(getIndex('t'))

# version #1 what lol
# for word in words:
#     print(f"inputting {word}")
#     counter = 0
#     for char in word:
#         i = getIndex(char)
#         center = centers[i]

#         ctypes.windll.user32.SetCursorPos(center[0] + 824, center[1] + 645)
#         if counter == 0:
#             ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
#         time.sleep(0.1)
#     ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up


# version #2: first word working
# for word in words:
#     print(f"inputting {word}")
#     counter = 0
#     for char in word:
#         i = getIndex(char)
#         center = centers[i]

#         ctypes.windll.user32.SetCursorPos(center[0] + 824, center[1] + 645)
#         if counter == 0:
#             ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
#         counter += 1
#         time.sleep(0.1)
#     ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up

# version #3: oh it was working off the empty letters array, need to make temp
for word in words:
    print(f"inputting {word}")
    counter = 0
    temp_letters = letters.copy()
    for char in word:
        i = getIndex(char)
        print(i)
        center = centers[i]

        ctypes.windll.user32.SetCursorPos(
            center[0] + SCREEN_AREA[0], center[1] + SCREEN_AREA[1])
        if counter == 0:
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
        counter += 1
        time.sleep(0.05)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
    time.sleep(0.05)
