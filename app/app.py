from flask import Flask, render_template, request, redirect, url_for, json, jsonify,session
from gtts import gTTS
import speech_recognition as sr
from html_table_extractor.extractor import Extractor
import os
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import requests, webbrowser
app = Flask(__name__)
app.secret_key=os.urandom(23564)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        error = request.args['error']
    except:
        error = '0'
    if error == '0' and request.method!='POST':
        sample = 'Welcome to Google for Blind...! Press Enter to search google'
        myobj = gTTS(text=sample, lang='en', slow=False)
        myobj.save("text.mp3")
        os.system("mpg321 text.mp3")
        error = 1
    print(error)
    if request.method == 'POST':

        if request.form['btn']=='search audio':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("What do you want to search")
                r.adjust_for_ambient_noise(source, duration = 1)
                audio = r.listen(source)
                try :
                    text = r.recognize_google(audio)
                    print(text)
                    sample = 'Press enter if you want to search '+text +', else press 1 key to navigate to home'
                    myobj = gTTS(text=sample, lang='en', slow=False)
                    myobj.save("text.mp3")
                    os.system("mpg321 text.mp3")
                
                    return redirect(url_for('check' ,text=text))
                except :
                    sample = 'Unable to recognize you! , press enter and speak again'
                    myobj = gTTS(text=sample, lang='en', slow=False)
                    myobj.save("text.mp3")
                    os.system("mpg321 text.mp3")
                    return redirect(url_for('index', error = 1))

    return render_template("index.html" ) 

@app.route('/check' ,methods=['GET','POST'])
def check():
    text = request.args['text']
    if request.method == 'POST' and request.form['btn'] == 'search?':
        req = requests.get('https://www.google.com/search?q='+text, headers={'User-Agent': 'Mozilla/5.0'})
        req.raise_for_status()
        soup_doc = BeautifulSoup(req.text, 'html.parser')
        linkelements = soup_doc.select('.r a')
       
        sample = 'link elements of the search page are as follows'
        number = 1
        for x in soup_doc.select(".r a"):
            if number <= 9:
                sample = sample +', '+str(number)+". "+ x.text
            number += 1
        myobj = gTTS(text=sample, lang='en', slow=False) 
        myobj.save("links.mp3") 
        os.system("mpg321 links.mp3")
        return redirect(url_for('link_number', text = text, error=0))

    if request.method == 'POST' and request.form['btn'] == 'speak again?':
        return redirect(url_for('index', error = 1))

        
    return render_template('fm.html')

@app.route('/link_number',methods=['GET','POST'])
def link_number():
    text = str(request.args['text'])
    error = request.args['error']
    req = requests.get('https://www.google.com/search?q='+text, headers={'User-Agent': 'Mozilla/5.0'})
    url = 'https://www.google.com/search?q='+text
    req.raise_for_status()
    soup_doc = BeautifulSoup(req.text, 'html.parser')
    linkelements = soup_doc.select('.r a')
    if error == '0' and request.method!='POST':
        sample = 'Press corresponding key to navigate to the respective page, or press 0 to hear again, else press enter to navigate to home page'
        myobj = gTTS(text=sample, lang='en', slow=False)
        myobj.save("text.mp3")
        os.system("mpg321 text.mp3")
        error = '1'
    
    if request.method == 'POST':
        if request.form['btn'] == 'hear again':
            os.system("mpg321 links.mp3")

        if request.form['btn'] == 'Home':
            return redirect(url_for('index', error = 1))
        number_input = int(request.form['btn'])
        return redirect(url_for('destination', text=text, number_input=number_input, error = 0))
    
    return render_template('page_number.html', url=url)   

@app.route('/destination', methods=['GET','POST'])
def destination():
    error = request.args['error']
    text = request.args['text']
    number_input = request.args['number_input']
    req = requests.get('https://www.google.com/search?q='+text, headers={'User-Agent': 'Mozilla/5.0'})
    req.raise_for_status()
    soup_doc = BeautifulSoup(req.text, 'html.parser')
    linkelements = soup_doc.select('.r a')
    page = Request(("https://google.com" + linkelements[int(number_input)-1].get('href')), headers={'User-Agent': 'Mozilla/5.0'})
    page_response = urlopen(page)
    url = "https://google.com" + linkelements[int(number_input)-1].get('href')
    html_read = page_response.read()
    soup = BeautifulSoup(html_read, 'html.parser')

    if error == '0' and request.method != 'POST':
        sample = 'Press enter to search for HTML attributes. 1 to navigate back, 2 to navigate to home page'
        myobj = gTTS(text=sample, lang='en', slow=False)
        myobj.save("text.mp3")
        os.system("mpg321 text.mp3")
   
    if request.method == 'POST':

        if request.form['btn'] == 'Home':
            return redirect(url_for('index', error = 1))

        if request.form['btn'] == 'Back':
            return redirect(url_for('link_number', text=text, error=1))

        if request.form['btn'] == 'search audio':
            if error == '0':    
                sample = 'Speak html attributes like title, paragraph, bold, links, tables, etcetra.'
                myobj = gTTS(text=sample, lang='en', slow=False)
                myobj.save("text1.mp3")
                os.system("mpg321 text1.mp3")
                error = 1

            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something or else say 'exit' to exit!")
                r.adjust_for_ambient_noise(source, duration = 1)
                audio = r.listen(source)
            try :
                text1 = r.recognize_google(audio)
                print(text1)

                if text1 == 'title':
                    sample = 'Title of the given page is '+soup.title.string
                    myobj = gTTS(text=sample, lang='en', slow=False)
                    myobj.save("text.mp3")
                    os.system("mpg321 text.mp3")
                elif text1 == 'bold' :
                    sample = 'Bold attributes of the given page are'
                    for x in soup.find_all('b'):
                        sample = sample +", "+ x.string
                    myobj = gTTS(text=sample, lang='en', slow=False) 
                    myobj.save("welcome.mp3") 
                    os.system("mpg321 welcome.mp3")
                elif text1 == 'links' :
                    sample = 'links to other pages are'
                    for x in soup.find_all('a'):
                        sample = sample +", "+ x.string
                    myobj = gTTS(text=sample, lang='en', slow=False) 
                    myobj.save("welcome.mp3") 
                    os.system("mpg321 welcome.mp3")
                elif text1 == 'para' :
                    sample = 'pragraphs of the given page is'
                    for x in soup.find_all('p'):
                        sample = sample +", "+ x.string
                    myobj = gTTS(text=sample, lang='en', slow=False) 
                    myobj.save("welcome.mp3") 
                    os.system("mpg321 welcome.mp3")
                elif text1 == 'tables' or text == 'table' :
                    sample = 'Tables of the given page are : '
                    extractor = Extractor(soup)
                    extractor.parse()
                    table_list = extractor.return_list()
                    print(len(table_list))
                    for rows in range(len(table_list)):
                        if rows >0 :
                            if len(table_list[rows]) != len(table_list[0]):
       
                                break
                            for columns in range(len(table_list[rows])):
                                sample += table_list[0][columns]+" is "+table_list[rows][columns]+", "
                    myobj = gTTS(text=sample, lang='en', slow=False) 
                    myobj.save("welcome.mp3") 
                    os.system("mpg321 welcome.mp3")  

                else:
                    sample = 'Unable to recognize HTML attribute, press enter and speak again'
                    myobj = gTTS(text=sample, lang='en', slow=False)
                    myobj.save("text.mp3")
                    os.system("mpg321 text.mp3")
                    return redirect(url_for('destination', text=text, number_input=number_input, error=1))


            except :
                sample = 'Unable to recognize you! , press enter and speak again'
                myobj = gTTS(text=sample, lang='en', slow=False)
                myobj.save("text.mp3")
                os.system("mpg321 text.mp3")
                return redirect(url_for('destination', text=text, number_input=number_input, error=1))
    return render_template('destination.html', url=url)    

if __name__ == "__main__":
    app.run(debug=True)


# def blind_browser():
#     j=1
#     while j>0:
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             print("What do you want to search")
#             r.adjust_for_ambient_noise(source, duration = 1)
#             audio = r.listen(source)
#             try :
#                 text = r.recognize_google(audio)
#                 print(text)
#                 sample = 'Press 1 if you want to search '+text +', else press any key to speak again'
#                 myobj = gTTS(text=sample, lang='en', slow=False)
#                 myobj.save("text.mp3")
#                 os.system("mpg321 text.mp3")
#                 answer = input("Type your answer")
#                 if answer == '1':
#                     break
#             except sr.UnknownValueError :
#                 print("Google Speech Recognition could not understand audio") 
#             except sr.RequestError as e: 
#                 print("Could not request results from Google Speech Recognition service; {0}".format(e))
#     req = requests.get('https://www.google.com/search?q='+text, headers={'User-Agent': 'Mozilla/5.0'})
#     req.raise_for_status()
#     soup_doc = BeautifulSoup(req.text, 'html.parser')
#     linkelements = soup_doc.select('.r a')

#     sample = 'link elements of the search page are as follows'
#     number = 1
#     for x in soup_doc.select(".r a"):
#         sample = sample +', '+str(number)+". "+ x.text
#         number += 1
#     myobj = gTTS(text=sample, lang='en', slow=False) 
#     myobj.save("welcome.mp3") 
#     os.system("mpg321 welcome.mp3")

#     number_input = int(input("Type number of link you want to go : "))

#     page = Request(("https://google.com" + linkelements[number_input-1].get('href')), headers={'User-Agent': 'Mozilla/5.0'})
#     page_response = urlopen(page)
#     html_read = page_response.read()
#     soup = BeautifulSoup(html_read, 'html.parser')

#     i=1

#     while i>0 :
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             print("Say something or else say 'exit' to exit!")
#             r.adjust_for_ambient_noise(source, duration = 1)
#             audio = r.listen(source)
#         try :
#             text = r.recognize_google(audio)
#             print(text)
#             sample = 'Press 1 if you said '+text +', else press 0 to speak again'
#             myobj = gTTS(text=sample, lang='en', slow=False)
#             myobj.save("text.mp3")
#             os.system("mpg321 text.mp3")
#             answer = input("Type your answer ")

#             if answer == '0':
#                 continue
#             else : 
#                 if text == 'exit':
#                     break
#                 elif text == 'title':
#                     sample = 'Title of the given page is '+soup.title.string
#                     myobj = gTTS(text=sample, lang='en', slow=False)
#                     myobj.save("text.mp3")
#                     os.system("mpg321 text.mp3")
#                 elif text == 'bold' :
#                     sample = 'Bold attributes of the given page are'
#                     for x in soup.find_all('b'):
#                         sample = sample +", "+ x.string
#                     myobj = gTTS(text=sample, lang='en', slow=False) 
#                     myobj.save("welcome.mp3") 
#                     os.system("mpg321 welcome.mp3")
#                 elif text == 'links' :
#                     sample = 'links to other pages are'
#                     for x in soup.find_all('a'):
#                         sample = sample +", "+ x.string
#                     myobj = gTTS(text=sample, lang='en', slow=False) 
#                     myobj.save("welcome.mp3") 
#                     os.system("mpg321 welcome.mp3")
#                 elif text == 'para' :
#                     sample = 'pragraphs of the given page is'
#                     for x in soup.find_all('p'):
#                         sample = sample +", "+ x.string
#                     myobj = gTTS(text=sample, lang='en', slow=False) 
#                     myobj.save("welcome.mp3") 
#                     os.system("mpg321 welcome.mp3")
#                 elif text == 'tables' or text == 'table' :
#                     sample = 'Tables of the given page are : '
#                     extractor = Extractor(soup)
#                     extractor.parse()
#                     table_list = extractor.return_list()
#                     print(len(table_list))
#                     for rows in range(len(table_list)):
#                         if rows >0 :
#                             if len(table_list[rows]) != len(table_list[0]):
       
#                                 break
#                             for columns in range(len(table_list[rows])):
#                                 sample += table_list[0][columns]+" is "+table_list[rows][columns]+", "
#                     myobj = gTTS(text=sample, lang='en', slow=False) 
#                     myobj.save("welcome.mp3") 
#                     os.system("mpg321 welcome.mp3")      

#         except sr.UnknownValueError :
#             print("Google Speech Recognition could not understand audio") 
#         except sr.RequestError as e: 
#             print("Could not request results from Google Speech Recognition service; {0}".format(e))