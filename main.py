import base64
import telebot
import requests
import random as ran
from telebot import types
from g4f.client import Client
bot=telebot.TeleBot('6934571077:AAFtnH7b27PTtaTIzIqml04ku8s6Ltuu8Jw');

game_in_progress={}

def GPT(prompt):
	client=Client()
	response=client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[{"role": "user", "content": prompt}],
	)
	return response.choices[0].message.content

def detect_text(image_base64, api_key):
	url=f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
	headers={
		"Content-Type": "application/json",
	}
	body={
		"requests": [
			{
				"image": {
					"content": image_base64
				},
				"features": [
					{
						"type": "TEXT_DETECTION"
					}
				]
			}
		]
	}
	response=requests.post(url, json=body, headers=headers)
	response_data=response.json()
	if 'error' in response_data:
		raise Exception(response_data['error']['message'])
	return response_data['responses'][0].get('textAnnotations', [{}])[0].get('description', '').strip()

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Чаво")

@bot.message_handler(content_types=['text'])
def start(message):
	keyboard=types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button1=types.KeyboardButton('/гра')
	button2=types.KeyboardButton('/Сігма')
	button3=types.KeyboardButton('/ХУЙ')
	keyboard.add(button1, button2, button3)

	print(f'{message.from_user.username} {message.from_user.first_name}')

	if message.text=="/Сігма":
		bot.send_message(message.chat.id, "https://www.tiktok.com/@markovv_tt/video/7196927034457672965?is_from_webapp=1&sender_device=pc")
	elif message.text.startswith("/пасхалко") or message.text.startswith("/1488") or message.text.startswith("/Пасхалко"):
		bot.send_message(message.chat.id, "што?🤣🤣🤣посхолко😳😳🤪кто заминетил🤣🤣🤣включаем вінтілітори🤣🤣🤣🤪🤪💪💪")
	elif message.text.startswith("/r34"):
		print('Ruler')
	elif message.text=="/help":
		bot.send_message(message.chat.id, text='Підсказки', reply_markup=keyboard)
	elif message.text=="/гра":
		if game_in_progress.get(message.chat.id):
			bot.send_message(message.chat.id, "Гра вже йде!")
		else:
			game_in_progress[message.chat.id]=True
			keyboard=types.InlineKeyboardMarkup()
			key_1=types.InlineKeyboardButton(text='камінь', callback_data='1')
			keyboard.add(key_1)
			key_2=types.InlineKeyboardButton(text='папір', callback_data='2')
			keyboard.add(key_2)
			key_3=types.InlineKeyboardButton(text='ножиці', callback_data='3')
			keyboard.add(key_3)
			bot.send_message(message.chat.id, text='Камін, ножиці, папір', reply_markup=keyboard)
	elif message.text=="/ХУЙ":
		bot.send_message(message.chat.id, "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬛⬛⬛⬜\n⬜⬛⬜⬛⬜⬜⬜\n⬜⬛⬜⬛⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬛⬜⬛⬜\n⬜⬜⬜⬛⬜⬛⬜\n⬜⬛⬛⬛⬜⬜⬜")
	elif message.text.startswith('/гбт'):
		if len(message.text)>5:
			bot.send_message(message.chat.id, GPT(message.text[5:]))

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if not game_in_progress.get(call.message.chat.id):
		return

	s=ran.randint(1, 3)
	if call.data == "1":
		if s==1:
			bot.send_message(call.message.chat.id, '-Камінь')
			bot.send_message(call.message.chat.id, 'Нічия')
		elif s==2:
			bot.send_message(call.message.chat.id, '-Папір')
			bot.send_message(call.message.chat.id, 'Поразка')
		elif s==3:
			bot.send_message(call.message.chat.id, '-Ножиці')
			bot.send_message(call.message.chat.id, 'Перемога')
	elif call.data == "2":
		if s==1:
			bot.send_message(call.message.chat.id, '-Камінь')
			bot.send_message(call.message.chat.id, 'Перемога')
		elif s==2:
			bot.send_message(call.message.chat.id, '-Папір')
			bot.send_message(call.message.chat.id, 'Нічия')
		elif s==3:
			bot.send_message(call.message.chat.id, '-Ножиці')
			bot.send_message(call.message.chat.id, 'Поразка')
	elif call.data == "3":
		if s==1:
			bot.send_message(call.message.chat.id, '-Камінь')
			bot.send_message(call.message.chat.id, 'Поразка')
		elif s==2:
			bot.send_message(call.message.chat.id, '-Папір')
			bot.send_message(call.message.chat.id, 'Перемога')
		elif s==3:
			bot.send_message(call.message.chat.id, '-Ножиці')
			bot.send_message(call.message.chat.id, 'Нічия')

	game_in_progress[call.message.chat.id] = False

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
	if message.caption.startswith('/text'):
		file_info=bot.get_file(message.photo[-1].file_id)
		file_path=file_info.file_path
		downloaded_file =bot.download_file(file_path)
		image_base64 =base64.b64encode(downloaded_file).decode()
		try:
			text=detect_text(image_base64, 'AIzaSyB-a5XyCQ-StJ7XeSX6EiKFVfl6Pmllinw')
			bot.send_message(message.chat.id, text)
		except Exception as e:
			print(f"Error: {e}")

bot.polling(none_stop=True, interval=0)
