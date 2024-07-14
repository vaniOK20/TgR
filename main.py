import requests
from bs4 import BeautifulSoup
import random as ran
import telebot

USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

headers={'User-Agent':USER_AGENT}

def pr(url):
  response=requests.get(url, headers=headers)
  response.raise_for_status()
  return response.text
  
def MaxPage(tag):
  html=BeautifulSoup(pr(f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}'), 'html.parser')
  page=html.find('a', alt="last page")
  if page:
    e=str(page)[str(page).find('pid')+4:]
    maxp=int(e[:e.find('"')-1])
  else:
    maxp=1
  if maxp>=200000: maxp=200000
  return maxp

def GetRandomPost(tag):
  mp=MaxPage(tag)
  html=BeautifulSoup(pr(f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}&pid={ran.randint(-1, mp)}'), 'html.parser')
  if not html.find('div', class_='image-list'):
    return None
  spans=html.find('div', class_="image-list").find_all('span')
  span=ran.choice(spans)
  return 'https://rule34.xxx'+span.find('a').get('href'), span.find('img').get('alt')

def GetImage(url):
  html=BeautifulSoup(pr(url), 'html.parser')
  images=html.find_all('img')
  image=None
  for img in images:
    if str(img).find('id="image"')!=-1:
      image=img
      break
  if not image:
    v=str(html.find('video'))
    v=v[v.find('src="')+5:]
    return v[:v.find('"')-1], True
  else:
    return image.get('src'), False

def GetAllPage(tag):
  count=ran.randint(0, MaxPage(tag))
  html=BeautifulSoup(pr(f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}&pid={count}'), 'html.parser')
  if not html.find('div', class_='image-list'):
    return None
  spans=html.find('div', class_="image-list").find_all('span')
  scr=[]
  for span in spans:
    scr.append('https://rule34.xxx'+span.find('a').get('href'))
  return scr

bot=telebot.TeleBot('6721623038:AAHjszLNE_FYuiUcpa-mqILtM_s27K_JIRI')

@bot.message_handler(content_types=['text'])
def handle_text(message):
  if message.text.startswith('знайти'):
    ab=GetRandomPost(message.text[6:])
    if ab:
      text=ab[1]
      if len(ab[1])>1022: text=ab[1][:1021]
      img=GetImage(ab[0])
      if img[1]:
        bot.send_video(message.chat.id, img[0], caption=text)
      else:
        bot.send_photo(message.chat.id, photo=img[0], caption=text)
    else:
      bot.send_message(message.chat.id, "Error")
  elif message.text.startswith('всі'):
    tag=message.text[3:]
    urls=GetAllPage(tag)
    for url in urls:
      im=GetImage(url)
      if im[1]:
        bot.send_video(message.chat.id, im[0])
      else:
       bot.send_photo(message.chat.id, photo=im[0])
bot.polling(none_stop=True, timeout=20, long_polling_timeout=20)