#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 08:25:37 2022

@author: Daire Stokes
"""

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
import sys

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default",
                  aws_access_key_id="xxxx",  
                  aws_secret_access_key="xxxx")

class TextToSpeech():
    
    def __init__(self, voice, out_format):
        self.region = 'eu-west-1'
        self.client = session.client("polly")
        self.voice = voice
        self.output_format = out_format
    
    def text_to_speech(self, page, text, title):
        '''
        Function to generate 
    
        Returns
        -------
        None.
    
        '''
        polly = session.client("polly")
        
        # TODO: if text is > 300 chars, split into N files and recombine
        
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(Text=text, 
                                               OutputFormat=self.output_format,
                                               VoiceId=self.voice)
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)
        
        # Access the audio stream from the response
        if "AudioStream" in response:
            body = response['AudioStream'].read()
        
            file_name =f'{page}-{title}.mp3'
        
            with open(file_name, 'wb') as file:
                file.write(body)
        
        else:
            sys.exit(-1)
    
    