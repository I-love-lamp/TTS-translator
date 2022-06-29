# -*- coding: utf-8 -*-
"""
Created on Tue May 24 13:37:31 2022

@author: DaireStokes
"""

from translator import Translator
from text_to_speech import TextToSpeech

# create interaction menu
# options: 1 = translation, 2 = text-to-speech, 3 = translation & TTS, 0 = quit

service = int(input("what service do you need? (1 = translate plain text, 2 = translate XLIFF file, 3 = text-to-speech, 4 = translate plain text and text-to-speech, 0 = quit.....  "))
while not service == 0:
    if service == 1 or service == 3:
        s_lang = int(input("What is the source language? (1 = English, | 2 = Arabic, | 3 = Turkish | 4 = French | 5 = Spanish | 0 = Quit.....  "))
        
        if service == 1:# map user selections to source language
            if s_lang == 1:
                source_lang = "en"
            elif s_lang == 2:
                source_lang = "ar"
            elif s_lang == 3:
                source_lang = "tr"
            elif s_lang == 4:
                source_lang = "fr"
            else:
                source_lang = "es"
        
        t_lang = int(input("What is the target language? (1 = English, | 2 = Arabic, | 3 = Turkish | 4 = French | 5 = Spanish | 0 = Quit.....  "))
        
        if service == 1 or service == 3:
            # map user selections to target language
            if t_lang == 1:
                target_lang = "en"
                voice = "Amy"            
            elif t_lang == 2:
                target_lang = "ar"
                voice = 'Zeina'
            elif t_lang == 3:
                target_lang = "tr"
                voice = 'Filiz'
            elif t_lang == 4:
                target_lang = "fr"
                voice = "Lea"
            else:
                target_lang = "es"
                voice = 'Lupe'
        
        
        # run text translation
        if not service == 0:
            service = input("Translation (press t) for Speech synthesis (press s).....")
            if service == 't':
                translator = Translator()
                file_path = input("Enter the file path.....   ")
                source_text = translator.get_file_text(file_path)
                translated_text = translator.translate_text(source_text, source_lang, target_lang)
                translator.write_translated_file(translated_text, file_path, target_lang)
            elif service == 's':
                tts = TextToSpeech(voice, 'mp3')
                tts.text_to_speech(1, input("Paste the text here....."), title = input("What course is this for? ...."))
                print('****************')
                print("Speech file has been created successfully.")
                cont = input("Translate another (y/n)")
                if cont == 'n':
                    break
    else:        
        service = int(input("what service do you need? (1 = translate plain text, 2 = translate English XLIFF file, 3 = text-to-speech, 4 = translate plain English and text-to-speech, 0 = quit.....  "))
        