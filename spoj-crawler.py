from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from BeautifulSoup import BeautifulStoneSoup
import HTMLParser
from selenium.common.exceptions import TimeoutException
import getpass

username = raw_input("Please enter your spoj username: ")
pwd = getpass.getpass('Please enter your spoj password: ')
# pwd = raw_input("")
driver = webdriver.Firefox()
# You can install install PhantomJS webdriver to avoid seeing the simulation


def main():		
	
	driver.get("http://spoj.com/login/")
	username_box = driver.find_element_by_xpath('//*[@id="inputUsername"]')
	username_box.clear()
	username_box.send_keys(username)
	pwd_box = driver.find_element_by_xpath('//*[@id="inputPassword"]')
	pwd_box.send_keys(pwd)
	btn = driver.find_element_by_xpath('//*[@id="content"]/div/div/form/div[4]/button')
	btn.click()	
	timeout = 10 # seconds
	try:
		element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH,"//*[@id='menu']/div/nav/ul/li[7]/a"))
    	)  	
	except TimeoutException:
		print "Loading took too much time!"

	driver.get("http://www.spoj.com/myaccount/")
	table = driver.find_elements_by_xpath('//*[@id="user-profile-tables"]/div/table[1]/tbody/tr/td')
	count = 0
	arr = []
	for i in table:
		link = i.get_attribute('innerHTML')
		start_index = link.find('"')
		end_index = link.find('"',10)
		link = "www.spoj.com"+link[start_index+1:end_index]		
		if (link.find("/",21)-link.find("/",14)-1)>(1+len(username)):
			arr.append("http://"+link)
			count = count + 1
	for link in arr:
		print ("Remaining : "+ str(count))
		count = count -1
		driver.get(link)

		try:
			element = WebDriverWait(driver, timeout).until(
        	EC.presence_of_element_located((By.XPATH,'//*[@id="content"]/div[8]/div[1]/form/table[1]/tbody/tr[1]/td[1]/a'))
    		)	  	
		except TimeoutException:
			print "Loading took too much time!"
			continue
		try :
			driver.find_element_by_xpath('//*[@id="content"]/div[8]/div[1]/form/table[1]/tbody/tr[1]/td[1]/a').click()
		except:
			print("exception occured for "+ link)
			continue

		# time.sleep(5)
		#xpath for edit option
		# //*[@id="statusres_18542966"]/span/a[1]

		try:
			element = WebDriverWait(driver, timeout).until(
        	EC.presence_of_element_located((By.XPATH,'//*[@id="op_window_plaintext_link"]'))
    		)	  	
		except TimeoutException:
			print "Loading took too much time!"
		time.sleep(2)
		try : 
			temp = driver.find_element_by_xpath('//*[@id="op_window_plaintext_link"]')
			temp.click()
		except:
			print("exception occured for "+ link)
			continue

		# time.sleep(5)		
		try:
			element = WebDriverWait(driver, timeout).until(
        	EC.presence_of_element_located((By.XPATH,'//*[@id="op_window2"]/div[2]/div/div[2]'))
    		)	  	
		except TimeoutException:
			print "Loading took too much time!"

		
		uni = "loading..."
		while (uni == "loading..."):
			try:
				elem = driver.find_element_by_xpath('//*[@id="op_window2"]/div[2]/div/div[2]')
			except:
				# print("exception occured for "+ link)
				break

			# print(elem)
			# print(elem.tag_name)
			pars = HTMLParser.HTMLParser()

			html_element = elem.get_attribute('innerHTML')
			
			uni = pars.unescape(html_element)

			# print(uni)
		
		file = open(link[27:].replace("/",""), "w")
		file.write(uni)
		
		file.close()			
	# driver.get("http://www.google.com")
	# print("quitting")
	driver.quit()

	
	

if __name__ == '__main__':
 	main()