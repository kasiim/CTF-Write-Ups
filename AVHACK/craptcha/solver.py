import requests # Module for making get/post requests
from bs4 import BeautifulSoup # HTML parser to find elements
import os # Listing files
import cv2 # Open ComputerVision lib
import shutil # Copying data to file
import numpy as np # Numpy for filtering np arrays

# Create session, since progress is tracked by session cookies
s = requests.session()

# Letter template files
letter_files = os.listdir('./letters/')

# Load templates into memory to make it faster
letters = [cv2.imread('./letters/' + letter_file) for letter_file in letter_files]

# URL to get the captcha from
url = "http://ctfp.ee:9999/captcha.php"
# URL to post answer to
post_url = "http://ctfp.ee:9999/"

# Magic detection function
def get_captcha_text(image):
    detected_letters = []

    # Iterate over each template character and see if it is in picture
    for template, letter in zip(letters, letter_files):
        # This returns us the template matching results
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # Filter out only matches where match % >= 95
        loc = np.where(result >= 0.95)
        # If matches were found for letter
        if loc[1].size:
            # Add letter to detected letters for later on with x
            # coordinate where the letter was found
            detected_letters.append((letter, loc[1]))

    answer = {}


    # Go over detected letters
    for letter in detected_letters:
        # Can be multiple of same letter 
        # (letter is a tuple of file name and x index of match found)
        for index in letter[1]:
            # Use x coord as dictionary key to sort them later on
            answer[index] = letter[0].split('.jpeg')[0]


    answer = dict(sorted(answer.items()))

    text = ""

    # Make our sorted dict into string of detected captcha text
    for key in answer.keys():
        text += answer[key]

    return text

# Get 10000 captchas and solve them!
for i in range(10000):
    # Request captcha from captcha url
    r = s.get(url, stream=True)

    filename = f'captcha.jpeg'

    # Save captcha as file (could be done without saving to file too)
    with open(filename, 'wb') as picture:
        shutil.copyfileobj(r.raw, picture)

    # Open image for comparision
    image = cv2.imread(filename)

    # Feed it to the magic function!
    captcha_message = get_captcha_text(image)


    payload = {
        'captcha' : captcha_message
    }

    # Post the found captcha to site!
    r = s.post(post_url, data=payload)

    # Parse out response text and display progress
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        h3 = soup.find("h3")
        print(h3.text)
    except AttributeError:
        # If there is no h3 tag then flag exists on page.
        flag = soup.find_all("div", {'class' : 'p-5'})
        # Profit we found the flag!
        print(flag[1].text.strip().split('\n')[0].strip())
