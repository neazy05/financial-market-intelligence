"""Legacy graduation-project Telegram bot.

This is a curated, secret-scrubbed copy of the original prototype. It has not
been fully runtime-tested; see README.md before attempting to run it.
"""
import os
# -*- coding: utf-8 -*-



from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from telegram import *
from telegram.ext import * 
from requests import *
import emoji
import yfinance as yf
from prophet import Prophet
import datetime
from datetime import date
from transformers import PegasusTokenizer, PegasusForConditionalGeneration


import csv
# 3. Setup Pipeline
monitored_tickers=[]

model_se = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis",num_labels=3)
tokenizer_se = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")
model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer_sum = PegasusTokenizer.from_pretrained(model_name)
model_sum = PegasusForConditionalGeneration.from_pretrained(model_name)

print("app is ready")

def search_for_stock_news_links(ticker):
    search_url = 'https://www.google.com/search?q=yahoo+finance+{}&tbm=nws'.format(ticker)
    r = requests.get(search_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    atags = soup.find_all('a')
    hrefs = [link['href'] for link in atags]
    return hrefs


def strip_unwanted_urls(urls, exclude_list):
    val = []
    for url in urls:
        if 'https://finance.yahoo.com/news/' in url and not any(exc in url for exc in exclude_list):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            val.append(res)
    return list(set(val))
def scrape_and_process(URLs):
    ARTICLES = []
    for url in tqdm(URLs):
        #print("1",url)
        r = requests.get(url)
       # print("2")
        soup = BeautifulSoup(r.text, 'html.parser')
       # print("3")
        results = soup.find_all('p')
        #print("4")
        text = [res.text for res in results]
        #print("5")
        words = ' '.join(text).split(' ')[:200]
       # print("6")
        ARTICLE = ' '.join(words)
       # print("7")
        ARTICLES.append(ARTICLE)
       # print("8")
    return ARTICLES
def summarize(articles):
    summaries = []
    for article in tqdm(articles):
        #print(article)
        input_ids = tokenizer_sum.encode(article, return_tensors="pt")
        #3input_ids = {k: v.cuda() for k, v in input_ids.items()}
        output = model_sum.generate(input_ids, max_length=55, num_beams=5, early_stopping=True)
        summary = tokenizer_sum.decode(output[0], skip_special_tokens=True)
        summaries.append(summary)
    return summaries
def create_output_array(summaries, scores, urls,monitored_tickers):
    output = []
    for ticker in monitored_tickers:
        for counter in range(len(summaries[ticker])):
            output_this = [
                            ticker, 
                            summaries[ticker][counter], 
                            scores[ticker][counter]['label'], 
                            scores[ticker][counter]['score'], 
                            urls[ticker][counter]
                          ]
            output.append(output_this)
    return output


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
NextDay_Date=  NextDay_Date .strftime("%Y-%m-%d")    

    


#FINAL
if not os.getenv("TELEGRAM_BOT_TOKEN"):
    raise RuntimeError("Set TELEGRAM_BOT_TOKEN in your environment before starting the bot.")
updater = Updater(token=os.environ["TELEGRAM_BOT_TOKEN"])
dispatcher = updater.dispatcher

Botdescription = f"""
boot Description 
وصف للبوت
{emoji.emojize(' :pushpin:')}

"""

intro="""
intro into cryptocurrencies
مقدمة للعملات الرقمية 
"""
Start= "Start"

BTC=0
ETH=0
TICKETS={"ETH":0,"BTC":0,"TSLA":0,"AAPL":0,"GOOG":0,"GME":0,"MSFT":0}
keys=""

def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(Start)],
     [KeyboardButton(Botdescription)],
          [KeyboardButton(intro)],
]
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
    أهلا وسهلا بكم في بوت تحليل مشاعر  في المقالات المالية وتوقع الأسعار
     
     تم تطوير النظم الذكية وراء هذا البوت  والبوت من قبل الطلاب 
               عبد الرحمن النيازي -سيف عبدالوهاب
              بإشراف الدكتور المهندس  
                           فراس الزين 
    """, reply_markup=ReplyKeyboardMarkup(buttons))

def messageHandler(update: Update, context: CallbackContext):

    #print(update.message.text)
    temp1=update.message.text.split("\n")[0]
    #print(type(temp1),len(temp1),len("boot Description"))
    if "intro into cryptocurrencies"==temp1:
        context.bot.send_message(chat_id=update.effective_chat.id, text=""". العملة المشفرة   هو شكل من أشكال المال الرقمي الذي تم تصميمه ليكون آمنا، وفي كثير من الحالات، مجهولا من المرسل و المتلقي 
        (اي غير معروف من ارسل المال و الى من أُرسل). وهي عملة مرتبطة بالإنترنت المشفر (كإرسال ايميل مشفر)، عملية تحويل المعلومات المقروءة إلى شفرة غير قابلة للإختراق، و لا يمكن تتبع عمليات الشراء والتحويلات.
         ظهر علم التشفير مع الحاجة إلى الاتصال الآمن في الحرب العالمية الثانية. وقد تطورت في العصر الرقمي مع عناصر نظرية رياضية وعلوم الكمبيوتر لتصبح وسيلة لتأمين الاتصالات والمعلومات والمال على الانترنت.
        
        """)

    if "boot Description " == temp1:
        #print("true")
        context.bot.send_message(chat_id=update.effective_chat.id, text="""
        .يقوم هذا البوت بعملية تحليل للمشاعر لاسهم المالية والعملات الرقمية عن طريق جمع مقالات من مواقع مالية معروفة ثم تلخيص هذه المقالات وتحديد المشاعر بها ثم أعطاء قرار بخصوص الشراء الاحتفاظ أو الابتعاد 
        يختص النظام بالمقالات الأجنبية بسبب قلة المقالات المالية ويقوم النظام بجلب المقالات من موقع ياهو فاينسس
        تم تطوير خاصية إضافية لتوقع سعر سهم من مجموعة أسهم محددة مسبقا
        
        """)

    if Start in update.message.text:
        buttons = [
         [KeyboardButton("select a or a stock crypto to do sentiment analysis")],
          
        [KeyboardButton("predict price  \N{money bag}" )],
        [KeyboardButton("Manual")],
        [KeyboardButton("back button" )], ]
        context.bot.send_message(chat_id=update.effective_chat.id, text="""
            يمكنك البدء الآن
        """, reply_markup=ReplyKeyboardMarkup(buttons))
    #print(update.message.text,len(update.message.text),len("Manual"))
    if "Manual" in update.message.text:
         buttons_2 = [[InlineKeyboardButton("Manual", callback_data="Manual")],]
         sent_msg=context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons_2), text="""
         manual way
        """)
    if "back button" in update.message.text:
        buttons = [[KeyboardButton(Start)], [KeyboardButton(Botdescription)],[KeyboardButton(intro)]]
        context.bot.send_message(chat_id=update.effective_chat.id, text="""
        أهلا وسهلا بكم في بوت تحليل مشاعر  في المقالات المالية وتوقع الأسعار
        
        :تم تطوير النظم الذكية وراء هذا البوت  والبوت من قبل الطلاب 
        عبدالرحمن نيازي --سيف 
        بإشراف الدكتور المهندس
                فراس الزين 
        """, reply_markup=ReplyKeyboardMarkup(buttons))
    if "select a or a stock crypto to do sentiment analysis" in update.message.text:
        buttons = [[InlineKeyboardButton("BTC", callback_data="BTC")],
         [InlineKeyboardButton("ETH", callback_data="ETH")],
         [InlineKeyboardButton("GME", callback_data="GME")],
         [InlineKeyboardButton("MSFT", callback_data="MSFT")],
         [InlineKeyboardButton("AAPL", callback_data="AAPL")],
         [InlineKeyboardButton("GOOG", callback_data="GOOG")],
         [InlineKeyboardButton("TSLA", callback_data="TSLA")],
         ]
       
        sent_msg=context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="""
        قام باختيار احداى العملات الرقمية أو الأسهم أو قم بإدخال عملة أو سهم 
        """)
    if "predict price  \N{money bag}" in update.message.text:
         buttons_1 = [[KeyboardButton("ETH-USD")],
         [KeyboardButton("BTC-USD")],
          [KeyboardButton("GOOG")],
        [KeyboardButton("AAPL" )],
        [KeyboardButton("GME" )],
         [KeyboardButton("back button" )], ]
         context.bot.send_message(chat_id=update.effective_chat.id, text="""
            الرجاء القيام باختيار سهم أو عملة رقمية لإجراء عملية لتوقع سعر الإغلاق  لليوم التالي
        """, reply_markup=ReplyKeyboardMarkup(buttons_1))

    if "BTC-USD" in update.message.text or "ETH-USD" in  update.message.text or "GOOG" in  update.message.text or "AAPL" in update.message.text   or "GME" in  update.message.text :   
        if update.message.text[0] != "$":
            print(update.message.text)
            data = load_data(update.message.text)
            df_train = data[['Date','Close']]

            df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
            period=2
            m = Prophet()
            m.fit(df_train)
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)
            print(forecast.tail(1)["yhat"])
            v=list(forecast.tail(1)["yhat"])
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"""
            
                {update.message.text}السعر المتوقع لإغلاق  
                {NextDay_Date} يوم 
                {v}
                """)
        
    
    if "$" ==  update.message.text[0]:
        print(update.message.text.split("$")[1])
        
        data = load_data(update.message.text.split("$")[1])
        print(data.shape)

        if data.shape[0] != 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"""
            
           يتم البحث الآن عن السعر المتوقع
            """)
            print("stage 2 is under way")
            df_train = data[['Date','Close']]

            df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
            period=2
            m = Prophet()
            m.fit(df_train)
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)
            print(forecast.tail(1)["yhat"])
            v=list(forecast.tail(1)["yhat"])
            
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"""
            
                {update.message.text}السعر المتوقع لإغلاق  
                {NextDay_Date} يوم 
                {v}
               """)
            keys_1=[update.message.text.split("$")[1]]
            print(keys_1)
            context.bot.send_message(chat_id=update.effective_chat.id,  text=f"""
                يتم الآن جمع المقالات لتحليل المشاعر  {keys_1}
                    """)
            monitored_tickers=keys_1
            context.bot.send_message(chat_id=update.effective_chat.id,  text=f"""Searching for stock news for {monitored_tickers}
                        """)

            raw_urls = {ticker:search_for_stock_news_links(ticker) for ticker in monitored_tickers}



            context.bot.send_message(chat_id=update.effective_chat.id,text='Cleaning URLs.')
            exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support']

            cleaned_urls = {ticker:strip_unwanted_urls(raw_urls[ticker] , exclude_list) for ticker in monitored_tickers} 

            # 4.3. Search and Scrape Cleaned URLs
            context.bot.send_message(chat_id=update.effective_chat.id,text='Scraping news links.')
            

            articles = {ticker:scrape_and_process(cleaned_urls[ticker]) for ticker in monitored_tickers} 


            # 2. Setup Model

            #model.cuda()
            print('Summarizing articles.')
            context.bot.send_message(chat_id=update.effective_chat.id,text='Summarizing articles.')
            
            summaries = {ticker:summarize(articles[ticker]) for ticker in monitored_tickers}

            context.bot.send_message(chat_id=update.effective_chat.id,text='Calculating sentiment.')
            print('Calculating sentiment.')
            #sentiment = pipeline("sentiment-analysis")


            nlp = pipeline("sentiment-analysis", model=model_se, tokenizer=tokenizer_se)
            scores = {ticker:nlp(summaries[ticker]) for ticker in monitored_tickers}

            # # 6. Exporting Results
            print('Exporting results')

            final_output = create_output_array(summaries, scores, cleaned_urls,monitored_tickers)

        
            for i in keys_1:
                temp=i
            keys_1=temp
            for i in range(0,len(final_output)):
            # print(message.txt)
                context.bot.send_message(chat_id=update.effective_chat.id, text=cleaned_urls[keys_1][i])
                context.bot.send_message( chat_id=update.effective_chat.id,text="{} \n sentiment is : {}".format(final_output[i][1],final_output[i][2]))

        else:
            DATA=0
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"""
            الأسم المدخل غير موجود في قاعدة بيانات الأسهم الرجاء التأكد من كتابته
                """)


            
    #Next message will call the age_handler function

        
    #if "Start analysing" in update.message.text:
   
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    data=data.tail(3)

    return data


def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()
    global BTC, ETH,TICKETS,keys
   
    if query in ["ETH","BTC","TSLA","AAPL","GOOG","GME","MSFT"]:
        
        for k, v in TICKETS.items():
            if k == query:
                TICKETS[k]=1
            else:
                TICKETS[k]=0
            keys = [k for k, v in TICKETS.items() if v == 1]
            keys=str(keys)
    

        context.bot.send_message(chat_id=update.effective_chat.id,  text=f"""
            the selected ticket is  {keys}
                """)
        buttons_1 = [[InlineKeyboardButton("start Analysing", callback_data="startA")],
            ]
        
        sent_msg=context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons_1), text="""
            بدء التحليل؟        """)
    if query=="Manual":
        context.bot.send_message(chat_id=update.effective_chat.id, text="""
        
        
    قم بإدخال اسم سهم او عملة رقمية للقيام بتحليل المشاعر وعملية توقع السعر 
    الرجاء كتابة الرمز $ قبل الأسم كمثال
    $AAPL
        """)

    if query=="startA":

        print(TICKETS)
        temp=""
        keys = [k for k, v in TICKETS.items() if v == 1]

        print(keys)
        context.bot.send_message(chat_id=update.effective_chat.id,  text=f"""
            the selected ticket is  {keys}
                """)
        monitored_tickers=keys
        context.bot.send_message(chat_id=update.effective_chat.id,  text=f"""Searching for stock news for {monitored_tickers}
                    """)

        raw_urls = {ticker:search_for_stock_news_links(ticker) for ticker in monitored_tickers}



        context.bot.send_message(chat_id=update.effective_chat.id,text='Cleaning URLs.')
        exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support']

        cleaned_urls = {ticker:strip_unwanted_urls(raw_urls[ticker] , exclude_list) for ticker in monitored_tickers} 

        # 4.3. Search and Scrape Cleaned URLs
        context.bot.send_message(chat_id=update.effective_chat.id,text='Scraping news links.')
        

        articles = {ticker:scrape_and_process(cleaned_urls[ticker]) for ticker in monitored_tickers} 


        # 2. Setup Model

        #model.cuda()
        print('Summarizing articles.')
        context.bot.send_message(chat_id=update.effective_chat.id,text='Summarizing articles.')
        
        summaries = {ticker:summarize(articles[ticker]) for ticker in monitored_tickers}

        context.bot.send_message(chat_id=update.effective_chat.id,text='Calculating sentiment.')
        print('Calculating sentiment.')
        #sentiment = pipeline("sentiment-analysis")


        nlp = pipeline("sentiment-analysis", model=model_se, tokenizer=tokenizer_se)
        scores = {ticker:nlp(summaries[ticker]) for ticker in monitored_tickers}

        # # 6. Exporting Results
        print('Exporting results')

        final_output = create_output_array(summaries, scores, cleaned_urls,monitored_tickers)

    
        for i in keys:
            temp=i
        keys=temp
        for i in range(0,len(final_output)):
        # print(message.txt)
            context.bot.send_message(chat_id=update.effective_chat.id, text=cleaned_urls[keys][i])
            context.bot.send_message( chat_id=update.effective_chat.id,text="{} \n sentiment is : {}".format(final_output[i][1],final_output[i][2]))

      


    
dispatcher.add_handler(CallbackQueryHandler(queryHandler))
dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling()