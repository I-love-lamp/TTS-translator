# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 12:54:39 2022

@author: daire
"""
from boto3 import Session
import sys

class AWSClient(object):
    
    def __init__(self):
        # Create a client using the credentials and region defined in the [adminuser]
        # section of the AWS credentials file (~/.aws/credentials).

        self.launch = Session(profile_name="default",
                          aws_access_key_id="AKIA4TGXFOTEVZACDMWD",  
                          aws_secret_access_key="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")
        
    def extract_key(self, keyfile):
        keypair=''
        try:
            # open the source file
            with open(keyfile) as keyfile:
                # retrieve text from the file
                for char in keyfile:
                    keypair+=char
        except FileNotFoundError as error:
            # request threw an error, close gracefully
            print(error)
            sys.exit(-1)
        
        return keypair
    

        