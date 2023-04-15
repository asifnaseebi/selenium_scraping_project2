from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from utils import scroll_all_pages, extract_comments_details

driver = webdriver.Chrome()
url = "https://www.youtube.com/watch?v=zghBofrKv7s&ab_channel=EhmadZubair"

driver.get(url)
scroll_all_pages(driver)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
comments_details = extract_comments_details(soup)
driver.quit()

video_name = soup.title.string
CSV_file_name = f'{video_name}.csv'
data_frame = pd.DataFrame(comments_details, columns=[
    'User Name', 'Comment Text', 'Comment Time', 'Likes', 'Thumbnail URL'])
data_frame.to_csv(CSV_file_name, index=False)

print('Comment details saved to the CSV file')

