from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import csv

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/Send', methods = ["GET", "POST"])
def Send():
    if request.method == 'POST':
        message = str(request.form['user_msg'])

        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=/Users/mrityunjay/Library/Application Support/Google/Chrome/Default')
        options.add_argument('--profile-directory=Default')
        chrome_browser = webdriver.Chrome(executable_path='/Users/mrityunjay/Downloads/chromedriver', options=options)

        def remove(string):
            return string.replace(" ", "")

        numbers = []
        f = request.form['file']
        if not f:
            return "No file"

        with open(f) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                row[0] = remove(row[0])
                if len(row[0]) == 10:
                    row[0] = '91' + str(row[0])
                    numbers.append(row[0])
                else:
                    numbers.append(row[0])

        numbers = np.array(numbers)
        print(type(numbers))

        for number in numbers:
            try:
                url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
                chrome_browser.get(url)

                wait = WebDriverWait(chrome_browser, 30)
                button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='_2Ujuu']")))

                button.click()
                time.sleep(1)
            except Exception:
                return render_template('index.html', prediction_text="Could not be sent")

    return render_template('index.html', prediction_text=f"Messages Sent to {len(numbers)} contacts!")

if __name__ == '__main__':
    app.run(debug=True)
