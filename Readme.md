Documnent Browser for blind (Software Eng project)
				
By:
Ankit Bagde -17CS30009

Under supervision of :
* Prof. Debasis Samanta
* Sumana Maiti

Demo video link ----  https://drive.google.com/file/d/1F8JsJ1HYw81mM-Kkn66hsAMv6adi2Q0A/view?usp=sharing

About the project:
* The project is webapp which will help a visually impaired individual to search Google with minimum use of keys of keyboard.
* For complete opreation only number keys and enter key is used, which can easily accessible by blind user


Language used - Flask(Python), HTML, CSS, Javascript, jQuery

Prerequisites - Python3

----Run the following commands first---
```
pip3 install Flask
pip3 install gTTS
pip3 install SpeechRecognition
pip3 install beautifulsoup4
pip3 install html-table-extractor
```
(in app folder)
```
pip3 install python-pyaudio python3-pyaudio
pip3 install pyaudio
```
Run the webapp by : python3 app.py

How will the webapp work?

Firstly, it will ask the blind user to speak of keyword he/she want to search.
After confirming the keyword, it will search the google and will read the results of the google search page in the following manner:

Eg- if keyword = document :

System - linkelements of the document are :
1. document-wikipedia
2. google docs
....

It will now ask the user to input the number of link he wishes to navigate. \
Back option is also provided. \
For input, number keys are used. \

After navigating to a particular page, webscraping is used to extract data from the webpage.
Now user has three options :
1. Navigate to home page
2. Navigate to back page i.e. links input page
3. Search for a HTML attribute of the navigated page.

Any kind of error is tackled by the software resulting in redirecting user to back page and asking him to repeat again.
