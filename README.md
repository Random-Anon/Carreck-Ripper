# Carreck-Ripper
Crawls http://www.carreck.com/pictures and downloads all images of a celebrity.

### Installation

```
git clone https://github.com/Random-Anon/Carreck-Ripper.git
```
or download the zip file

Install the dependencies

```
pip install -r requirements.txt
```

### Running

```
python CarreckRipper.py [CARRECK_CELEB_URL] [LAST_PAGE_YOU_WANT_TO_CRAWL]
```

Example
```
python CarreckRipper.py http://www.carreck.com/pictures/category/jessica-alba/ 78
```
This will crawl all 78 pages of Jessica Alba and it will try to download every gallery and save the images in a folder called output.
