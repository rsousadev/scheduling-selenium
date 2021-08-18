import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests


class WhatsappBot:

    def __init__(self):
        self.url = 'https://web.whatsapp.com'
        option = Options()
        self.driver = webdriver.Firefox(options=option, executable_path='./geckodriver')
        self.driver.get(self.url)
        self.request_url = 'https://endpoint_api.com.br'


    def send_message(self, group_name, message):
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div/label/div/div[2]').send_keys(group_name)
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div[2]').click()
        driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div/div[2]').click()
        for part in message.split('\n'):
            driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div/div[2]').send_keys(part)
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(
                Keys.ENTER).perform()
        #driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]').send_keys(message)
        driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div/div[2]').send_keys(Keys.RETURN)
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]').clear()

    def token(self):
        url = self.request_url + '/api-token/'
        data = {'username':'username', 'password':'password'}
        response = requests.request("POST", url, json=data).json()
        return response['token']

    def project_select(self, token_auth, project_name):
        url = self.request_url + '/api/projects?name=' + str(project_name)
        header = {'Authorization': 'Token ' + str(token_auth)}
        response = requests.request("GET", url, headers=header).json()
        return response

    def group_update(self, token_auth, group_id, group_p, groups_name, group_link, group_clicks):
        url = self.request_url + '/api/groups/' + str(group_id)
        header = {'Authorization': 'Token ' + str(token_auth)}
        data = {'click': group_p, 'links': group_link, 'clicks': group_clicks, 'name': groups_name}
        response = requests.request("PUT", url, json=data, headers=header).json()
        return response
