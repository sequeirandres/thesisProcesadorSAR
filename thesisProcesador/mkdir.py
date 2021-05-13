import os

directory = 'mediciones'

try:
    os.makedirs(directory)
except OSError as e:
    if os.path.exists(directory):
        print('Directory ["'+ directory +'"] already exits')
