"""
This is for the personal practice of Tkinter
Under no circumstance is this file to be used for real purposes

Author: Shin Do Hyun

"""


from Tkinter import *
from PIL import Image, ImageTk
from urllib2 import urlopen
import io
import requests
from bs4 import BeautifulSoup 


ROOT_URL = 'http://tabshoura.com/wordpress/wp-content/uploads/2016/06/'

def trade_spider(max_pages):  # max_pages makes sure we dont crawl too much
    page = 1  # changes every time we loop through a page
    while page < max_pages:
        url = ROOT_URL
        source_code = requests.get(url)  # connect to webpage and store results in source_code
        plain_text = source_code.text  # just get the good meat of the website
        soup = BeautifulSoup(plain_text)  # all source code from website and soup is what we can sort through


        for link in soup.findAll('a', {'class': 'item-name'}):  # 'a' is links in HTML language, pick out links with item-name
            href = ROOT_URL + link.get('href')  # only take text inside href attribute, will get full url
            title = link.string  # get only the text inside it(title of something)
            get_single_item_data(href)  # for each item individual page and do def
            print(href)
            print(title)
        page += 1

    changeImage(item_name.jpg)

def get_single_item_data(item_url):
    source_code = requests.get(item_url)  # connect to webpage and store results in source_code
    plain_Image = source_code.text  # just get the good meat of the website
    soup = BeautifulSoup(plain_Image)
    for item_name in soup.findAll('img', {'class': 'i-name'}):  # need HTML element, attribute, and value
        return (item_name.jpg)
    for link in soup.findAll('a'):  # find all links on page
        href = ROOT_URL + link.get('href')
        print(href)  # test

def changeImage(image):
    my_photo = image
    #make image_opener = Image.open(photo_encoded).resize((100,100))



URL="http://tabshoura.com/wordpress/wp-content/uploads/2016/06/news.jpg"
my_photo=urlopen(URL).read()
photo_encoded=io.BytesIO(my_photo)
image_opener=Image.open(photo_encoded).resize((100,100))


root = Tk()

root.title("Shin's News Feed")

topTitle = Label(root, text = "Shin's News Feed", font = "Helvetica 44 bold")
topTitle.pack()

lbl = Label(root, text = "All of the contents are extracted from")
lbl.pack()

lbl1 = Label(root, text = "www.forif.co.kr")
lbl1.pack()


urlImage = ImageTk.PhotoImage(image_opener)

imglbl = Label(root, image = urlImage)
imglbl.pack()




lbl2 = Label(root, text = "Select the news from these buttons", font = 10)
lbl2.pack()

buttonFrame = Frame(root)
buttonFrame.pack()

btn1 = Button(root, text = "Top news", padx = 50) #add function
btn1.pack(side = LEFT)

btn2 = Button(root, text = "Entertainment news", padx = 50)
btn2.pack(side = LEFT)

btn3 = Button(root, text = "World news", padx = 50)
btn3.pack(side = LEFT)

btn4 = Button(root, text = "Business", padx = 50)
btn4.pack(side = LEFT)


root.mainloop()
