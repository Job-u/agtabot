import re
import openai
import speech_recognition as sr
from gtts import gTTS
import os
import time

class bot:
    exit_commands = ("bye", "exit", "ty", "thanks","thank you", "done", "quit")

    translations = {
        
    # Greetings and Common Phrases
    "What is your name?": {"filipino": "Ano ang pangalan mo?", "casiguran_agta": "anya i ngahen moa"},
    "Goodbye": {"filipino": "Paalam.", "casiguran_agta": "naydén kako dén"},
    "Thank you.": {"filipino": "Maraming salamat.", "casiguran_agta": "me ado a salamat"},
    "I am sorry.": {"filipino": "Patawarin mo ako.", "casiguran_agta": "Patawadén nék mo"},
    "Yes.": {"filipino": "Opo.", "casiguran_agta": "on"},
    "No.": {"filipino": "Hindi po.", "casiguran_agta": "ewan be"},
    "My name is .": {"filipino": "Ako si .", "casiguran_agta": "saken ti"},
    "Good to see you": {"filipino": "Buti na lang nakita kita", "casiguran_agta": "meta"},
    "How are you": {"filipino": "Kamusta ka na?", "casiguran_agta": "kumusta kam dén"},
    "I am fine": {"filipino": "Mabuti naman.", "casiguran_agta": "ma ige be"},
    "Glad to meet you": {"filipino": "Masaya akong makilala ka.", "casiguran_agta": "mesahat ék a matenggi taka"},
    "Good afternoon": {"filipino": "Magandang hapon", "casiguran_agta": "memahal a apon"},
    "Good evening": {"filipino": "Magandang gabi", "casiguran_agta": "memahal a kélép"},
    "Good morning": {"filipino": "Magandang umaga", "casiguran_agta": "memahal a gagabi"},
    "How about you": {"filipino": "Kayo po? / Ikaw?", "casiguran_agta": "sikam"},
    
    # Daily Use Expressions
    "Excuse me": {"filipino": "Makikiraan po.", "casiguran_agta": "mékidiman kame"},
    "I'm leaving": {"filipino": "Aalis na po ako.", "casiguran_agta": "még dema kamedén"},
    "Can you help me": {"filipino": "Maaari mo ba akong tulungan?", "casiguran_agta": "pwede ék moy tulungan"},
    "What can I do for you": {"filipino": "Ano po ang magagawa ko para sa inyo?", "casiguran_agta": "anya i magimet koa para dekam"},
    "I understand": {"filipino": "Naiintindihan ko.", "casiguran_agta": "meentendian ko"},
    
    # Question Words
    "What": {"filipino": "Ano?", "casiguran_agta": "anya"},
    "When": {"filipino": "Kailan?", "casiguran_agta": "ni kesya"},
    "Where": {"filipino": "Saan?", "casiguran_agta": "tahe"},
    "Which": {"filipino": "Alin?", "casiguran_agta": "nahe"},
    "Who": {"filipino": "Sino?", "casiguran_agta": "te esya"},
    "Why": {"filipino": "Bakit?", "casiguran_agta": "ata ay"},
    "How much": {"filipino": "Magkano?", "casiguran_agta": "sanganya?"},

    # Colors
    "Blue": {"filipino": "Asul", "casiguran_agta": "asul"},
    "Red": {"filipino": "Pula", "casiguran_agta": "medingat"},
    "White": {"filipino": "Puti", "casiguran_agta": "melatak"},
    "Black": {"filipino": "Itim", "casiguran_agta": "mengitet"},
    "Green": {"filipino": "Berde", "casiguran_agta": "kumanidon"},
    "Yellow": {"filipino": "Dilaw", "casiguran_agta": "medilaw"},
    "Brown": {"filipino": "Kulay tsokolate", "casiguran_agta": "tsokolate"},
    "Gray": {"filipino": "Kulay abo", "casiguran_agta": "kulay abo"},
    "Pink": {"filipino": "Rosas", "casiguran_agta": "rosas"},
    "Orange": {"filipino": "Dalandan", "casiguran_agta": "Kuman a don"},
    "Violet": {"filipino": "Lila", "casiguran_agta": "Kuman a pensél"},

    # Family Members
    "Grandfather": {"filipino": "Lolo", "casiguran_agta": "boboy lakay"},
    "Grandmother": {"filipino": "Lola", "casiguran_agta": "boboy bakés"},
    "Father": {"filipino": "Tatay", "casiguran_agta": "améng"},
    "Mother": {"filipino": "Nanay", "casiguran_agta": "inéng"},
    "Older Brother": {"filipino": "Kuya", "casiguran_agta": "kakéng"},
    "Older Sister": {"filipino": "Ate", "casiguran_agta": "kakéng"},
    "Youngest Sibling": {"filipino": "Bunso", "casiguran_agta": "depos"},
    "Husband": {"filipino": "Asawang lalaki", "casiguran_agta": "asawa a lalaki"},
    "Wife": {"filipino": "Asawang babae", "casiguran_agta": "asawa a babe"},
    "Son": {"filipino": "Anak na lalaki", "casiguran_agta": "anak a lalake"},
    "Daughter": {"filipino": "Anak na babae", "casiguran_agta": "anak a babe"},
    
    # Buying and Selling
    "How much for two": {"filipino": "Magkano ang dalawa?", "casiguran_agta": "sangan éduwa"},
    "I will get two": {"filipino": "Kukuha ako ng dalawa.", "casiguran_agta": "mangalap pékta éduwa"},
    "Okay, you can get them": {"filipino": "Sige kunin mo na.", "casiguran_agta": "nay alapén mo dén"},
    "It is fifty pesos": {"filipino": "Limampung piso ito.", "casiguran_agta": "lima apulo ye"},
    "The two are 100 pesos": {"filipino": "Isang daang piso ang dalawa.", "casiguran_agta": "esa a daan éduwa"},

    # Giving Directions
    "Where are you going": {"filipino": "Saan ka pupunta?", "casiguran_agta": "ahe ka umange"},
    "I'm going to the garden": {"filipino": "Pupunta ako sa halamanan.", "casiguran_agta": "ange ékta sikaw"},
    "Where is the garden": {"filipino": "Nasaan ang halamanan?", "casiguran_agta": "ahe to sikaw"},
    "The garden is by the river": {"filipino": "Malapit sa ilog ang halamanan.", "casiguran_agta": "adene ta dinom ya tu sikaw"},
    "Whose garden is it": {"filipino": "Kaninong halamanan iyon?", "casiguran_agta": "kini esya a sikaw ya"},
    "It is my garden": {"filipino": "Sa akin ang halamanan.", "casiguran_agta": "ko o ko a sikaw"}
    
    }

    def __init__(self):
        print("Greetings! Would you prefer to speak using a microphone or enter text manually?")
        print("'M' to speak using Microphone or 'T' to type your message")
        self.mode = input("Mode (M/T): ").strip().upper()
        self.recognizer = sr.Recognizer()
    
    def translate(self, userinput):

        userinput = re.sub(r'[^a-zA-Z0-9]','', userinput.lower())
        # Checks if the user's input matches any of the known phrases, either in English, Filipino, or Casiguran Agta.
        for english, translations in self.translations.items():
            # Convert stored phrases to lowercase and remove punctuation for better matching
            english_clean = re.sub(r'[^a-zA-Z0-9\s]', '', english.lower())
            filipino_clean = re.sub(r'[^a-zA-Z0-9\s]', '', translations['filipino'].lower())
            agta_clean = re.sub(r'[^a-zA-Z0-9\s]', '', translations['casiguran_agta'].lower())

              # Check if ANY keyword is found inside the user input
            if english_clean in userinput or filipino_clean in userinput or agta_clean in userinput:
                return f"English: {english}\nFilipino: {translations['filipino']}\nCasiguran Agta: {translations['casiguran_agta']}"

        return "Oops! We don’t have a translation for that yet. Do you want to email us so we can add it?"
    
    def voice_input(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return ""
        except sr.RequestError:
            print("Speech service is not available right now.")
            return ""

    def chat(self):
        while True:
            if self.mode == 'T':
                userinput = input("Enter a word or phrase or type 'quit' to exit: ")
            else:
                userinput = self.voice_input()
                if not userinput:
                    continue # Skip if recognition failed, it will try again or wait
                
            
            if userinput.lower() in self.exit_commands:
                print("Goodbye! Maraming salamat!")
                break
            print(self.translate(userinput))

AgtaBot = bot()
AgtaBot.chat()