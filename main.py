from flask import Flask, render_template, request, send_file, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import zipfile
import time
import os
import shutil

PATH = "C:\Program Files (x86)\chromedriver.exe"

downloading_path = r"C:\proj\\"


app =  Flask(__name__)

@app.route('/') # url endpoint
def main():
    return render_template(
        'app.html',
        )

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/', methods=['POST'])
def upload_file():
    global downloading_path
    uploaded_file = request.files['file']
    group = request.form['group']
    profile = int(request.form['profile'])
    download_path = request.form['download']
    if download_path:
        downloading_path = download_path + "\\"
    print(downloading_path)
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        run_bot(uploaded_file, group, profile)
    return redirect(url_for('main'))

@app.route('/')
def appfunc():
    return render_template('app.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')


def bot(file_text, group, profile_index, rep=True):
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")
    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": 
                        downloading_path,#IMPORTANT - ENDING SLASH V IMPORTANT # add custom path
             "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(PATH, options=options)
    driver.get("https://hl7v2.gvt.nist.gov/gvt/#/cf")


    time.sleep(2) # render full webpage
    content = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")



    driver.find_element_by_xpath('//button[@class="btn btn-sm dropdown-toggle"]').click() # open dropdown

    link = driver.find_element_by_link_text(group)
    link.click()

    time.sleep(2) # render full webpage

    

    

   
    driver.find_element_by_xpath(f'//*[@id="subNavBar"]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/table/tbody/tr[{profile_index}]/td/a').click()

    
    time.sleep(3)



    p = driver.find_element_by_xpath('//*[@id="messagePanel"]/div[2]/div/div/div[6]/div[1]/div/div/div/div[5]/div/pre/span')
    


    action = ActionChains(driver)
    driver.implicitly_wait(10)
    action.click(on_element = p)
    action.send_keys(file_text).perform()

    driver.find_element_by_xpath('//*[@id="executionPanel"]/div/div[2]/div/ul/li[2]/a').click()


    driver.find_element_by_xpath('//button[@class="btn btn-info btn-sm dropdown-toggle"]').click()

    driver.find_element_by_xpath('//*[@id="executionPanel"]/div/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div/ul/li[1]/a').click()

    time.sleep(3)
    

    if rep:
        driver.find_element_by_xpath('//button[@class="btn btn-sm dropdown-toggle"]').click() # open dropdown

        link = driver.find_element_by_link_text("NIST Home")
        link.click()


    


def run_bot(zipf, group, profile_index): # change to zip later
    rep = True
   
    
    z_file = zipfile.ZipFile(zipf, "r")
    with z_file as zip:
        onlyfiles = zip.namelist()
        length = len(onlyfiles)

        if length > 1:
            rep = True
        else:
            rep = False

        for name in zip.namelist():
            with zip.open(name) as file:
                file_text = file.read().decode('utf-8')
                bot(file_text, group, profile_index)
        
    