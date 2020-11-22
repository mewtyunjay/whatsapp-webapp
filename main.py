from flask import Flask, render_template, url_for, request
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, sys

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/Send', methods = ["GET", "POST"])
def Send():
    delay = 30
    name = request.form['user_name']
    msg = str(request.form['user_msg'])

    def new_chat(user_name):
        # click on search bar
        new_chat = chrome_browser.find_element_by_xpath('//div[@class="_22PcK"]')
        new_chat.click()

        # type the new user name
        new_user = chrome_browser.find_element_by_xpath('//div[@class="_1awRl copyable-text selectable-text"]')
        new_user.send_keys(user_name)
        # time.sleep(1)

        try:
            # click on the said user
            # user = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
            user = WebDriverWait(chrome_browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, f'{user_name}')))
            user.click()
            time.sleep(2)

        # if user not found
        except NoSuchElementException:
            print("User doesn't exist in database")
        except Exception as e:
            chrome_browser.close()
            print(e)
            sys.exit()


    # for reading cache to avoid rescan of QR
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=/Users/mrityunjay/Library/Application Support/Google/Chrome/Default')
    options.add_argument('--profile-directory=Default')

    # link the chromedriver
    chrome_browser = webdriver.Chrome(executable_path='/Users/mrityunjay/Downloads/chromedriver', options=options)
    chrome_browser.get('https://web.whatsapp.com/')
    time.sleep(15)

    username_list = [name]

    for user_name in username_list:

        try:
            # look for chat in recent chats and click on it
            # user = WebDriverWait(chrome_browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, f'{user_name}')))
            user = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
            user.click()

            # if not found in recent chat, look for it in new chat
        except NoSuchElementException as se:
            new_chat(user_name)


         # click on textbox and type message
        message_box = chrome_browser.find_element_by_xpath('//div[@class="DuUXI"]')
        # message_box.click()
        message_box.send_keys(msg)

        # click on msg send button
        # button = chrome_browser.find_element_by_xpath('//button[@class="_2Ujuu"]')
        # button.click()
    return render_template('index.html', prediction_text=f"{msg}")


if __name__ == '__main__':
    app.run(debug=True)