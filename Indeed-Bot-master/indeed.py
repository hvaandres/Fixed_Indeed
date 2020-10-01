#system libraries
import os
import random
import time

# Selenium Libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

# Recaptcha Libraries 
import time
import pickle
import info
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub

class IndeedBot:
    def __init__(self):

        # Create headless chrome
        options = Options()
        options.add_argument("--headless")
        options.add_argument("user-data-dir=selenium")

        # create a new Chrome session
        self.driver = webdriver.Chrome('/Users/hvaandres/Downloads/Indeed-Bot-master/chromedriver')


        # open indeed
        self.driver.get('https://secure.indeed.com/account/login')
        
        '''
        self.driver.get('https://secure.indeed.com/account/login')
        pickle.dump( self.driver.get_cookies() , open("cookies.pkl","wb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        '''

        # SetUP some sleep

        time.sleep(5)

        # Get email field
        emailElem = self.driver.find_element_by_id('login-email-input')
        emailElem.send_keys(info.email)

        # Get password field
        passElem = self.driver.find_element_by_id('login-password-input')
        passElem.send_keys(info.password)
        passElem.submit()
        
        #switch to recaptcha frame
        frames=self.driver.find_elements_by_tag_name("iframe")
        self.driver.switch_to.frame(frames[0]);
        time.sleep(5)

        #click on checkbox to activate recaptcha
        self.driver.find_element_by_class_name("recaptcha-checkbox-border").click()

        #switch to recaptcha audio control frame
        self.driver.switch_to.default_content()
        frames=self.driver.find_elements_by_css_selector("#recaptcha-audio-button")#.find_elements_by_tag_name("iframe")
        self.driver.switch_to.frame(frames[0])
        time.sleep(5)

        #click on audio challenge
        self.driver.find_element_by_id("recaptcha-audio-button").click()

        #switch to recaptcha audio challenge frame
        self.driver.switch_to.default_content()
        frames= self.driver.find_elements_by_tag_name("iframe")
        self.driver.switch_to.frame(frames[-1])
        time.sleep(5)

        #click on the play button
        self.driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
        #get the mp3 audio file
        src = self.driver.find_element_by_id("audio-source").get_attribute("src")
        print("[INFO] Audio src: %s"%src)
        #download the mp3 audio file from the source
        urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
        sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
        sound.export(os.getcwd()+"\\sample.wav", format="wav")
        sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
        r= sr.Recognizer()

        with sample_audio as source:
            audio = r.record(source)

        #translate audio to text with google voice recognition
        key=r.recognize_google(audio)
        print("[INFO] Recaptcha Passcode: %s"%key)



        

        print('Logging in...')
        self.driver.implicitly_wait(10)

        # Redirect to main page
        self.driver.find_element_by_class_name('gnav-PageLink-text').click()

        # Close privacy policy
        

        # get what field
        whatElem = self.driver.find_element_by_xpath('//*[@id="text-input-what"]')
        #whatElem.clear()
        whatElem.send_keys(info.title)

        # get where field
        whereElem = self.driver.find_element_by_id('text-input-where')
        whereElem.send_keys(Keys.CONTROL, 'a')
        whereElem.send_keys(info.zipCode)
        whereElem.submit()
 
        # get list of jobs with apply by indeed only
        jobList = self.driver.find_elements_by_class_name('iaP')

        # initialize main page
        main = self.driver.window_handles[0]

        # Go through the jobList and open in new tab
        for job in jobList:
            job.click()

            # get new tab and switch to it
            jobWin = self.driver.window_handles[1]
            self.driver.switch_to.window(jobWin)
            title = self.driver.title
            print('Applying job ' + title)

            # Click on Apply Now
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'jobsearch-IndeedApplyButton-contentWrapper'))).click()

            # Locate the parent iframe and switch to it
            parentIframe = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,"//iframe[contains(@id,'modal-iframe')]")))    
            self.driver.switch_to.frame(parentIframe)

            # Locate the parent iframe and switch to it
            childIframe =  WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,"//iframe[contains(@src,'resumeapply')]")))
            self.driver.switch_to.frame(childIframe)   
            conButton = self.driver.find_element_by_xpath('//*[@id="form-action-continue"]')
            # Click on continue button if there any             
            if conButton.is_enabled():
                self.driver.implicitly_wait(30)
                conButton.click()
                if conButton.is_enabled():
                    self.driver.close()
                    self.driver.switch_to.window(main) 
                else:
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="form-action-submit"]'))).click()
                    self.driver.close()
                    self.driver.switch_to.window(main) 
            

            #If no button close the window and switch to main window
            #WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form-action-submit"]'))).click()
            #if self.driver.find_element_by_xpath('//*[@id="ia-container"]/div/div[2]/a'):
            else: 
                self.driver.close()
                self.driver.switch_to.window(main)
 



IndeedBot()
