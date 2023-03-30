# -*- coding: utf-8 -*-

import logging
import openai
import telegram, os
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters
import Updater, CommandHandler



#################
import openai
	
openai.api_key = os.getenv("OPENAI_API_KEY") 

chat_language = os.getenv("INIT_LANGUAGE", default = "zh") #amend here to change your preset language
	
conversation = []

class ChatGPT:  
    

    def __init__(self):
        
        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo")



    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})
        

        response = openai.ChatCompletion.create(
	            model=self.model,
                messages = self.messages

                )

        conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        print("AI回答內容：")        
        print(response['choices'][0]['message']['content'].strip())


        
        return response['choices'][0]['message']['content'].strip()
	







#####################

telegram_bot_token = str(os.getenv("TELEGRAM_BOT_TOKEN"))



# Load data from config.ini file
#config = configparser.ConfigParser()
#config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=telegram_bot_token)



@app.route('/callback', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


def reply_handler(bot, update):
    """Reply message."""
    #text = update.message.text
    #update.message.reply_text(text)
    chatgpt = ChatGPT()        
    
                                            #update.message.text 人類的問題 the question humans asked
    ai_reply_response = chatgpt.get_response(update.message.text) #ChatGPT產生的回答 the answers that ChatGPT gave
    
    update.message.reply_text(ai_reply_response) #用AI的文字回傳 reply the text that AI made

# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='你好，欢迎调戏可爱的雌堕弱受緒山まひろ酱！')

def menu(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='能给緒山まひろ的命令！:\n/menu  让主人们康康緒山まひろ里面都有什么扒！\n/ping  和緒山まひろ打个招呼扒~！\n/gpt  没错喔~緒山まひろ酱内置了ChatGPT讷~~！\n/search [搜索内容]  緒山まひろ内置的sukebei.nyaa.si种子站搜索')

def ping(update, context):
    sticker_id = "CAACAgUAAxkBAAGuYglkJc1MJmBhBBgNyhsrIEfW7URPTAACfAkAAoThKVW8g26jtyadwi8E"
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker_id)

def search(update, context):
    query = ' '.join(context.args)
    url = f'https://sukebei.nyaa.si/?f=0&c=0_0&q={query}'
    response = requests.get(url)
    results = response.json()

    if results:
        context.bot.send_message(chat_id=update.message.chat_id, text=results[0]['title'])
        context.bot.send_message(chat_id=update.message.chat_id, text=results[0]['url'])
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='緒山まひろ酱哭唧唧的告诉主人...没有找到相关结果呐~~~')

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

def main():
    updater = Updater(token='TELEGRAM_BOT_TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(MessageHandler(Filters.regex('^/ping$'), ping))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, gpt))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
