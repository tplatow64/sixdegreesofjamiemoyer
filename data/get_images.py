import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib.request
import time
import random
import csv
import os

def player_image_exists(player_image_dir: str, playerId : str) -> bool:
    # if os.path.exists(f'{player_image_dir}{playerId}.jpg'):
    #     return True
    # else:
    #     return False
    return False

def write_header(row: list, output_csv):
    header_row = []
    for key,value in row.items():
        header_row.append(key)
    header_row.append('image_url')
    output_csv.writerow(header_row) #print the headers     

def write_row(row: list, image_url, output_csv):
    data_row = []
    for key,value in row.items():
        data_row.append(value)
    data_row.append(image_url)
    output_csv.writerow(data_row) #print the data

def scrape_and_download_image(url, folder, playerId):
    # Send a GET request to the URL
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # response = requests.get(url, headers=headers)
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    try:
        # Attempt to open the URL
        response = urlopen(req)
    except Exception as e:
        print(f"Error opening URL {url}: {e}")
        return ''
    
    # Check if the request was successful (status code 200)
    if response != '':
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response, 'html.parser')

        # Find the player's image tag
        div_tags = soup.find_all(class_='media-item multiple')  # Multiple Images tag with class 'poptip'
        if len(div_tags) == 0:
            div_tags = soup.find_all(class_='media-item') # Image tag with class 'poptip'
        for div_tag in div_tags:
            # Find all the image tags inside the current div tag
            image_tags = div_tag.find_all('img')
            
            # Loop through all the image tags
            for image_tag in image_tags:
                # Process each image tag here
                # For example, you can extract attributes like 'src', 'alt', etc.
                # if not(player_image_exists(folder, playerId)):
                #     sleep_time = random.uniform(19, 28)
                #     print(f'sleeping {sleep_time} seconds')
                #     time.sleep(sleep_time)
                #     urllib.request.urlretrieve(image_tag['src'], f'{folder}{playerId}.jpg')
                #     print("Image source:", image_tag['src'])
                #     print("downloaded")   
                # else:
                #     sleep_time = random.uniform(12, 23)
                #     print(f'sleeping {sleep_time} seconds')
                #     time.sleep(sleep_time)
                #     print("no download needed")
                print("Image source:", image_tag['src'])
                return image_tag['src']
            print("FAILED download")
            return ''
    else:
        print("Failed to retrieve page:", response.status_code)
        return ''
    
if __name__ == "__main__":
    image_folder = 'C:\\coding\\6_degrees_jamie_api\\static\\images\\player_images\\'
    data_folder = 'C:\\coding\\6_degrees_jamie\\'
    data_file = 'player_urls.csv'
    output_file = 'player_urls_w_images.csv'
    count = 0

    with open(f'{data_folder}{data_file}', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        with open(f'{data_folder}{output_file}', mode='a', newline='', encoding='utf-8') as output_csv:
            output_csv = csv.writer(output_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                count+=1
                # if count == 1:
                #     write_header(row, output_csv)
                playerId = row.get('playerID', '')
                player_url = row.get('player_url', '')
                name = row.get('name', '')
                if player_url != '':
                    print(f'#{count} - {name} - {playerId}')
                    image_url = scrape_and_download_image(player_url, image_folder, playerId)
                    print('waiting')
                    sleep_time = random.uniform(12,19)
                    write_row(row, image_url, output_csv)
                else:
                    write_row(row, '', output_csv)
    print('done')