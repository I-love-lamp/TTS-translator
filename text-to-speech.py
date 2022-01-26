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
                  aws_access_key_id="AKIA4TGXFOTEX5TGCL42",  
                  aws_secret_access_key="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")

def text_to_speech(text, page, title = input("What course is this for?")):
    '''
    Function to generate 

    Returns
    -------
    None.

    '''
    polly = session.client("polly")
    
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, 
                                           OutputFormat="mp3",
                                           VoiceId="Matthew")
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


####  grab text from source ###

# parse text from XLFF files

# parse text from a file
def get_file_text(filepath=input("Enter the file path...")):
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
# test text parser
some_text = get_file_text()
print(some_text)


# test generate speech
text_to_speech(some_text, 1)

# clean text file (handle special characters)

