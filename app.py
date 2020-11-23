from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from flask_mysqldb import MySQL
import time
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import csv
import yaml
from datetime import datetime

app = Flask(__name__)

# mysql confg
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app) #instantiation of mysql obj

@app.route('/', methods=['GET','POST'])
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

        for number in numbers:
            try:
                url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
                chrome_browser.get(url)
                wait = WebDriverWait(chrome_browser, 30)
                button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='_2Ujuu']")))
                button.click()
                time.sleep(3) #important
                cur = mysql.connection.cursor()
                now = datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                cur.execute("REPLACE INTO users(msisdn, message, sent_time) VALUES(%s, %s, %s)",(number, message, formatted_date))
                mysql.connection.commit()
                # cur.close()

            except Exception:
                return render_template('index.html', prediction_text="Could not be sent")
            # cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM users ")
            if result > 0:
                userDetails = cur.fetchall()
                cur.close()
        chrome_browser.close()

    return render_template('index.html', prediction_text=f"Messages Sent to {len(numbers)} contacts!", userDetails=userDetails)

@app.route('/status', methods=['GET','POST'])
def status():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users ")
    if result > 0:
        userDetails = cur.fetchall()
        return render_template("status.html", userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)
