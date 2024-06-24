import os

if __name__ == '__main__':
    os.system('chcp 65001')
    os.system('mitmweb.exe -s myAddon.py -p 8080')