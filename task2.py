from selenium import webdriver
from utils import extract_chanel_all_video_comments_details

channel_url = input("Please enter the URL of the YouTube channel you want to extract video links from: ")
driver = webdriver.Chrome()
extract_chanel_all_video_comments_details(channel_url, driver)
driver.quit()
