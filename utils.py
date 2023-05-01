import time
import os
import pandas as pd
from bs4 import BeautifulSoup

scroll_time = 5


def scroll_to_page_bottom(driver):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
        time.sleep(scroll_time)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def extract_data_from_comments(soup):
    global thumbnail_url
    comment_sections = soup.find_all('ytd-comment-thread-renderer')
    all_comment = []

    for comment in comment_sections:
        user_info = comment.find('ytd-comment-renderer').find('a', {'id': 'author-text'})
        user_name = user_info.text.strip()
        comment_text = comment.find('yt-formatted-string', {'id': 'content-text'}).text.strip()
        comment_likes = comment.find('span', {'id': 'vote-count-middle'}).text.strip()
        comment_time = comment.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text.strip()
        thumbnail_url_tag = comment.find('yt-img-shadow', {"class": "style-scope ytd-comment-renderer no-transition"})
        if thumbnail_url_tag is not None:
            thumbnail_url = thumbnail_url_tag.find('img').get('src')

        all_comment.append([user_name, comment_text, comment_time, comment_likes, thumbnail_url, ])

    return all_comment


def get_channel_directory_path(url):
    channel_name = url.split("/")[-2].replace('@', '')
    channel_dir = os.path.join(os.getcwd(), channel_name)
    if not os.path.exists(channel_dir):
        os.mkdir(channel_dir)
    return channel_dir


def get_video_urls_from_page(soup):
    video_urls = []
    for video in soup.find_all('ytd-rich-grid-media'):
        video_url = 'https://www.youtube.com' + video.find('a', {'id': 'video-title-link'}).get('href')
        video_urls.append(video_url)
    return video_urls


def process_comments_for_video(video_url, channel_dir, driver):
    driver.get(video_url)

    time.sleep(scroll_time)

    scroll_to_page_bottom(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    comment_data = extract_data_from_comments(soup)

    video_name = soup.title.string.split(" - YouTube")[0]
    video_title = video_name.replace('/', '-')

    file_name = video_title + '.csv'
    file_path = os.path.join(channel_dir, file_name)
    df = pd.DataFrame(comment_data, columns=['User Name', 'Thumbnail URL', 'Comment Time', 'Likes', 'Comment Text'])
    df.to_csv(file_path, index=False)
    print(f"Comments for video {video_title} saved to CSV file {file_name}")


def extract_chanel_all_video_comments_details(channel_url, driver):
    channel_url += "/videos"
    driver.get(channel_url)

    time.sleep(scroll_time)

    scroll_to_page_bottom(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    channel_dir = get_channel_directory_path(channel_url)
    video_urls = get_video_urls_from_page(soup)

    for video_url in video_urls:
        process_comments_for_video(video_url, channel_dir, driver)

    print('Comment details saved to the CSV file')
