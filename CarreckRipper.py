import os
import argparse
import requests
import urllib.request
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import multiprocessing
from threading import Thread

OUTPUT_DIR = 'output/'

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
headers = { 'User-Agent' : user_agent }

def crawlURL(url):
    print('Crawling: ', url)

    try:
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')

        for i,article in enumerate(articles):
            try:
                new_url = article.find_all('h1', {'class': 'entry-title'})[0].find_all('a')[0].get('href')
                response = requests.get(new_url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')


                article = soup.find_all('div', {'class': 'entry-content'})[0]
                links = [link.get('href') for link in article.find_all('a')]
                for link in links:
                    thread = Thread(target = downloadImage, args = (link,))
                    thread.start()

            except Exception as e:
                pass
    except Exception as e:
        pass

def downloadImage(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        tmp_images = soup.find_all('img')

        if 'imagebam' in url:
            image = tmp_images[0]["src"]
        elif 'imgbox' in url:
            image = tmp_images[-1]["src"]
        elif 'imagevenue' in url:
            image = 'http://img167.imagevenue.com/'+tmp_images[0]["src"]
        elif 'imgur' in url:
            image = url+'.jpg'
        else:
            print('Unhandled URL:',url)

        img_name = image.strip().split('/')[-1]
        filename = OUTPUT_DIR+img_name

        urllib.request.urlretrieve(image,filename)

    except Exception as e:
        pass

def main(args):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    BASE_URL = args.base_url
    PAGES = args.pages

    print('-------------\nBase URL:', BASE_URL)
    print('Pages:', PAGES,'\n-------------\n\n')

    Parallel(n_jobs=multiprocessing.cpu_count()-2)(delayed(crawlURL)(BASE_URL + 'page/' + str(i)) for i in range(1,PAGES+1))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Crawls carreck.com and downloads all images of a celebrity.')
  parser.add_argument( "base_url", type=str, help='URL of first page.')
  parser.add_argument( "pages" , type=int, help='Number of Pages to crawl.')
  parser.add_argument('-c', '--cpuCount',
                            default=6,
                            dest='cpu_count',
                            help='Number of threads to run the process on.')
  main( parser.parse_args() )
