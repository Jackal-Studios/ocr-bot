#!/usr/bin/env python3
import os
from PIL import Image
import pytesseract
import cv2
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from time import time
import pickle
import os.path

API_TOKEN = open('./secrets/api.txt','r+').readline()
ids=[[451248878,'eng']]
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# ids=[[451248878,'eng']]
if(os.path.isfile('./db/my_ids.pickle')):
    with open('./db/my_ids.pickle', 'rb') as data:
        ids = pickle.load(data)
        data.close()

else:
    with open('./db/my_ids.pickle','wb') as output:
        pickle.dump(ids,output)
        output.close()
# with open('test.pickle','wb') as output:
#          pickle.dump(ids,output)
#          output.close()

vote_cb = CallbackData('vote', 'action')
start_time=time()
temporary_folder_path="./ramdisk/"
filecount=0
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program files\Tesseract-OCR\tesseract.exe'        #for windows users
forward_mode=False
async def cvprocess():
    return cv2.imread(temporary_folder_path+"img.jpg",0)
async def pytesseractprocess(img,lang):
    return pytesseract.image_to_string(img, lang=lang)
async def removetempfile():
    return os.remove(temporary_folder_path + 'img.jpg')
async def ocr(language):
    try:
        global filecount
        filecount+=1
    	#image = cv2.imread(temporary_folder_path+"img.jpg")
    	#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    	#cv2.imwrite(temporary_folder_path+"1.png", gray)
        if(os.path.getsize(temporary_folder_path+'img.jpg')<1000):
            return "Error downloading file"
        try:
            img = await cvprocess()
        except:
            return "There was an error while processing your file"
        #text = pytesseract.image_to_string(Image.open(temporary_folder_path+"1.png"), lang=language)
        text = await pytesseractprocess(img,language)
	    #os.remove(temporary_folder_path+'1.png')
        await removetempfile()
        if(text==""):
            text="ERROR: No text found"
        return text
    except:
        return "There was an error processing Your file"

def get_keyboard():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton('English \U0001F1EC\U0001F1E7', callback_data=vote_cb.new(action='eng'))).row(
        types.InlineKeyboardButton('Українська \U0001F1FA\U0001F1E6', callback_data=vote_cb.new(action='ukr')),
        types.InlineKeyboardButton('Deutsch \U0001F1E9\U0001F1EA', callback_data=vote_cb.new(action='deu')),
        types.InlineKeyboardButton('中文语言 \U0001F1E8\U0001F1F3', callback_data=vote_cb.new(action='chi_sim'))).row(
        types.InlineKeyboardButton('हिंदुस्तानी \U0001F1EE\U0001F1F3', callback_data=vote_cb.new(action='hin')),
        types.InlineKeyboardButton('Español \U0001F1EA\U0001F1F8', callback_data=vote_cb.new(action='spa')),
        types.InlineKeyboardButton('عربى' + '\U0001F1E6\U0001F1EA', callback_data=vote_cb.new(action='ara'))).row(
        types.InlineKeyboardButton('Русский \U0001F1F7\U0001F1FA', callback_data=vote_cb.new(action='rus')),
        types.InlineKeyboardButton('Portugues \U0001F1F5\U0001F1F9', callback_data=vote_cb.new(action='por')),
        types.InlineKeyboardButton('Française 🇫🇷', callback_data=vote_cb.new(action='fra')),)

@dp.errors_handler()
async def errors_handler(dispatcher, update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import Unauthorized, InvalidQueryID, TelegramAPIError, \
        CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound, BotBlocked
    if isinstance(exception, Exception):
        print("error ocured")
        return
    if isinstance(exception, BotBlocked):
        print("bot blocked")
        return
    if isinstance(exception, CantDemoteChatCreator):
        print("Can't demote chat creator")
        return

    if isinstance(exception, MessageNotModified):
        print('Message is not modified')
        return

    if isinstance(exception, MessageToDeleteNotFound):
        print('Message to delete not found')
        return

    if isinstance(exception, Unauthorized):
        print('Unauthorized: {}'.format(exception))
        return

    if isinstance(exception, InvalidQueryID):
        print('InvalidQueryID: {} \nUpdate: {}'.format(exception,update))
        return

    if isinstance(exception, TelegramAPIError):
        print('TelegramAPIError: {} \nUpdate: {}'.format(exception,update))
        return
    print('Update: {} \n{}'.format(update,exception))




@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    print("started!")
    await bot.send_message(message.chat.id, "To use this bot, you have to choose a language(/language), send an image PNG/JPG and wait for our bot to process it. The best result can be achieved with text that has a very high contrast compared to its background (Example purely black text on a white background. Also, cropping and aligning the image also helps. Thanks for using our bot!")

@dp.message_handler(commands=['language'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await bot.send_message(message.chat.id,"Choose language",reply_markup=get_keyboard() )



@dp.callback_query_handler(vote_cb.filter(action=['eng', 'ukr','deu','chi_sim','hin','spa','ara','rus','por','fra']))
async def callback_vote_action(query: types.CallbackQuery, callback_data: dict):
    logging.info('Got this callback data: %r', callback_data)  # callback_data contains all info from callback data
    await query.answer()  # don't forget to answer callback query as soon as possible
    callback_data_action = callback_data['action']
    global ids
    used=False
    # print("callback")
    # print(query.from_user.id)
    # print(query.chat_instance)
    # print(query.message.chat.id)
    for n in ids:
        if(query.message.chat.id in n):
            ids[ids.index(n)]= [query.message.chat.id,callback_data_action]
            used=True
            break
        else:
            used=False
    if(used==False):
        ids.append([query.message.chat.id,callback_data_action])
    print(ids)
    #f=open("/home/pi/OCRBOT/ids.py","w")
    #f.write("ids=[{}]".format(ids))
    #f.close()
    with open('./db/my_ids.pickle','wb') as output:
        pickle.dump(ids,output)
    # with open('test.pickle','wb') as output:
    #     pickle.dump(ids,output)
    print("written")
   # try:
   #     f=open('ids.py','w')
   #     f.write(ids)
   #     f.close()
   # except:
   #     print("error writing to file")

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    if(message.chat.id>=0):
        try:
            global ids
            global forward_mode
            if((message.chat.id==451248878 or message.chat.id==386764197) and forward_mode==True):
                for y in ids:
                    try:
                        await bot.forward_message(y[0],451248878,message["message_id"])
                    except:
                        print("Error forwarding to: {}".format(y[0]))
            used=False
            lang = "eng"
            for n in ids:
                if (message.chat.id in n):
                    lang = str(n[1])
                    await message.reply("Your Image is being processed("+str(n[1])+")")
                    used = True
                    break
                else:
                    used = False
            if (used == False):
                await message.reply("Your Image is being processed(eng)")
            try:
                await message.photo[-1].download(temporary_folder_path+'img.jpg')
            except:
                print("error downloading")
            await bot.send_message(message.chat.id, await ocr(lang))
            #await message.photo[-1].download(temporary_folder_path+str(message["message_id"])+'.jpg')
            #ocr2(message.chat.id,message["message_id"],lang)
        except:
            print("ERROE HANDLING THE PHOTO")

@dp.message_handler(content_types=['document'])
async def handle_docs_photo(message):
    if (message.document.mime_type == 'image/jpeg' or message.document.mime_type == 'image/png'):
        if (message.chat.id >= 0):
            try:
                global ids
                used = False
                lang="eng"
                for n in ids:
                    if (message.chat.id in n):
                        lang=str(n[1])
                        await message.reply("Your Image is being processed(" + str(n[1]) + ")")
                        used = True
                        break
                    else:
                        used = False
                if (used == False):
                    await message.reply("Your Image is being processed(eng)")
                await message.document.download(temporary_folder_path+'img.jpg')
                await bot.send_message(message.chat.id, await ocr(lang))
            except:
                 print("ERROR HANDLING A DOCUMENT")
           # await message.document.download(temporary_folder_path+str(message["message_id"])+'.jpg')
           # ocr2(message.chat.id,message["message_id"],lang)

@dp.message_handler(commands=['language'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await bot.send_message(message.chat.id,"Choose language",reply_markup=get_keyboard() )
@dp.message_handler(commands=['stats'])
async def send_welcome(message: types.Message):
    global ids
    if(message.chat.id==451248878 or message.chat.id==386764197):
        unix_uptime=time()-start_time
        await message.reply("Total users:"+str(len(ids))+"\nFiles OCRed:"+str(filecount)+"\nUptime: "+str(int(unix_uptime/60/60/24))+         ####################
                            " days, "+str(int(unix_uptime/60/60)%60)+" hours, "+str(int(unix_uptime/60)%60)+" minutes")



@dp.message_handler(commands=['forward'])
async def send_welcome(message: types.Message):
    global forward_mode
    print(message.chat.id)
    if(message.chat.id==451248878 or message.chat.id==386764197):
        forward_mode=True
        await message.reply("WARNING, You entered the forwarding mode, to cancel write /cancel")
@dp.message_handler(commands=['cancel'])
async def send_welcome(message: types.Message):
    global forward_mode
    if((message.chat.id==451248878 or message.chat.id==386764197)):
        forward_mode=False
        await message.reply("Exited forwarding mode")
@dp.message_handler()
async def send_welcome(message: types.Message):
    global ids
    print(message.text)
    me= await bot.get_me()
    print(me.username)
    if (message.chat.id < 0):
        if (message.text == '@'+me.username):
            if (message.reply_to_message):
                if (
                        message.reply_to_message.content_type == 'document' or message.reply_to_message.content_type == 'photo'):
                    if (message.reply_to_message.content_type == 'photo'):
                        try:
                            # global ids
                            used = False
                            lang = "eng"
                            for n in ids:
                                if (message.reply_to_message.chat.id in n):
                                    lang = str(n[1])
                                    await message.reply_to_message.reply(
                                        "Your Image is being processed(" + str(n[1]) + ")")
                                    used = True
                                    break
                                else:
                                    used = False
                            if (used == False):
                                await message.reply_to_message.reply("Your Image is being processed(eng)")
                            try:
                                await message.reply_to_message.photo[-1].download(temporary_folder_path + 'img.jpg')
                            except:
                                print("error downloading")
                            await bot.send_message(message.reply_to_message.chat.id, await ocr(lang))
                            # await message.photo[-1].download(temporary_folder_path+str(message["message_id"])+'.jpg')
                            # ocr2(message.chat.id,message["message_id"],lang)
                        except:
                            print("ERROE HANDLING THE PHOTO")

                    elif (message.document.mime_type == 'image/jpeg' or message.document.mime_type == 'image/png'):
                        try:
                            # global ids
                            used = False
                            lang = "eng"
                            for n in ids:
                                if (message.reply_to_message.chat.id in n):
                                    lang = str(n[1])
                                    await message.reply_to_message.reply(
                                        "Your Image is being processed(" + str(n[1]) + ")")
                                    used = True
                                    break
                                else:
                                    used = False
                            if (used == False):
                                await message.reply_to_message.reply("Your Image is being processed(eng)")
                            await message.reply_to_message.document.download(temporary_folder_path + 'img.jpg')
                            await bot.send_message(message.reply_to_message.chat.id, await ocr(lang))
                        except:
                            print("ERROR HANDLING A DOCUMENT")
            else:
                await message.reply("You need to reply to a photo while mentioning this bot in order to ocr it")

    try:
        global forward_mode
        if((message.chat.id==451248878 or message.chat.id==386764197) and forward_mode==True and message["text"]!="/cancel"):
            for i in ids:
                await bot.forward_message(i[0],451248878,message["message_id"])
    except:
        await bot.message.reply("there was an error")




# @dp.message_handler()
# async def message_handler(message: types.Message):
#     global ids
#     #print(message.text)
#     #print(bot.get_me().username)
#     if(message.chat.id<0):
#         if(message.text == await bot.get_me().username):
#             if(message.reply_to_message):
#                 if(message.reply_to_message.content_type=='document' or message.reply_to_message.content_type=='photo'):
#                     if(message.reply_to_message.content_type=='photo'):
#                         try:
#                             # global ids
#                             used = False
#                             lang = "eng"
#                             for n in ids:
#                                 if (message.reply_to_message.chat.id in n):
#                                     lang = str(n[1])
#                                     await message.reply_to_message.reply("Your Image is being processed(" + str(n[1]) + ")")
#                                     used = True
#                                     break
#                                 else:
#                                     used = False
#                             if (used == False):
#                                 await message.reply_to_message.reply("Your Image is being processed(eng)")
#                             try:
#                                 await message.reply_to_message.photo[-1].download(temporary_folder_path + 'img.jpg')
#                             except:
#                                 print("error downloading")
#                             await bot.send_message(message.reply_to_message.chat.id, await ocr(lang))
#                             # await message.photo[-1].download(temporary_folder_path+str(message["message_id"])+'.jpg')
#                             # ocr2(message.chat.id,message["message_id"],lang)
#                         except:
#                             print("ERROE HANDLING THE PHOTO")
#
#                     elif(message.document.mime_type == 'image/jpeg' or message.document.mime_type == 'image/png'):
#                         try:
#                             # global ids
#                             used = False
#                             lang = "eng"
#                             for n in ids:
#                                 if (message.reply_to_message.chat.id in n):
#                                     lang = str(n[1])
#                                     await message.reply_to_message.reply("Your Image is being processed(" + str(n[1]) + ")")
#                                     used = True
#                                     break
#                                 else:
#                                     used = False
#                             if (used == False):
#                                 await message.reply_to_message.reply("Your Image is being processed(eng)")
#                             await message.reply_to_message.document.download(temporary_folder_path + 'img.jpg')
#                             await bot.send_message(message.reply_to_message.chat.id, await ocr(lang))
#                         except:
#                             print("ERROR HANDLING A DOCUMENT")
#             else:
#                 await message.reply("You need to reply to a photo while mentioning this bot in order to ocr it")
#
#


##################################################################################################################





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
