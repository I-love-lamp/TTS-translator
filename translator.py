# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 12:51:17 2022

@author: daire
"""

import boto3
import sys


class Translator():
    def __init__(self):
        region = 'eu-west-1'
        self.client = boto3.client(service_name='translate', region_name=region, use_ssl=True)
    
    def translate_text(self, text, source_lang, target_lang):
        result = self.client.translate_text(Text=text, SourceLanguageCode=source_lang, 
                                       TargetLanguageCode=target_lang)
        return result
    
    ####  grab text from source ###
    
    # parse text from XLFF files
    # TODO
    
    # parse text from a file
    def get_file_text(self, filepath):
        text = ''
        if len(sys.argv) <1:
            print("Incorrect arguments provided. Enter the filepath and filename")
        else:
            try:
                # open the source file
                with open(filepath) as file:
                    # retrieve text from the file
                    for char in file:
                        text+=char
            except FileNotFoundError as error:
                # request threw an error, close gracefully
                print(error)
                sys.exit(-1)
            
        return text   