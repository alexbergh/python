import openai  
import telebot  
  
  
openai.api_key = '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'  
bot = telebot.TeleBot('API TOKEN BOT')  
  
@bot.message_handler(func=lambda _: True)  
def handle_message(message):  
    response = openai.Completion.create(  
        model='text-davinci-003',  
        prompt=message.text,  
        temperature=0.5,  
        max_tokens=1000,  
        top_p=1.0,  
        frequency_penalty=0.5,  
        presence_penalty=0.0,  
  
    )  
  
    bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])  
    # print(message.text)  
  
bot.polling()  
  
#