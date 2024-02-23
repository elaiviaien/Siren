from pyrogram import Client, filters
from pygame import mixer
import os
import keyboard
import asyncio

app = Client("my_account", api_id=None, api_hash=None, config_file="")
filenames = os.listdir()
mixer.init()


def get_input(prompt, error_message, condition):
    while True:
        value = input(prompt)
        if condition(value):
            return value
        print(error_message)


tel_channel = input("Введіть назву каналу для відстеження сирени (наприклад, 'sirena_dp' без '@'): ")
call_text = input("Введіть частину повідомлення каналу, коли має спрацювати сирена: ")

siren_music = get_input("Введіть назву файлу сирени (файл повинен бути у папці файлу siren_main.exe): ",
                        "Цього файлу немає в папці, перевірте правильність написання назви файлу",
                        lambda t: t in filenames)

good_play = get_input("Відтворити спеціальний звук в кінці сирени? ('+' означає ТАК, '-' означає НІ)",
                      "Введено неправильний символ. Введіть '+' або '-'",
                      lambda t: "+" in t or "-" in t)

if "+" in good_play:
    good_call_text = input("Введіть частину повідомлення каналу, коли має спрацювати музика скасування сирени: ")
    good_siren_music = get_input("Введіть назву файлу сирени (файл повинен бути у папці файлу siren_main.exe): ",
                                 "Цього файлу немає в папці, перевірте правильність написання назви файлу",
                                 lambda t: t in filenames)

print("Відстеження каналу...")


@app.on_message(filters.channel & filters.create(lambda _, __, m: m.chat.username == tel_channel))
async def call(client, message):
    m = await app.get_history(tel_channel, limit=1)
    text = m[0].text
    music_file = siren_music if call_text in text else good_siren_music if "+" in good_play and good_call_text in text else None
    if music_file is not None:
        mixer.music.load(music_file)
        await asyncio.sleep(0.1)
        while mixer.music.get_busy() or keyboard.is_pressed('enter'):
            mixer.music.play()
            print("В укриття!!!" if call_text in text else "Скасування тривоги")
            print("Натисніть Enter, щоб зупинити")
            await asyncio.sleep(0.1)
        print("Зупинено")
        mixer.music.stop()


app.run()
