import os
import time
import pandas as pd
import csv
import shutil
from train import Encoder
cwd = os.getcwd()

"""
Takes the user id as input, folder with is user id will be deleted from the dataset folder
"""



id = input("Please enter the ID number you want to delete:" )
delFolder = cwd + "\\dataset\\LA_"+id
try:
    shutil.rmtree(delFolder, ignore_errors=True)
    Encoder.createEncoding()
except:
    pass
