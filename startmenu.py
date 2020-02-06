class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

starttext = open("s.txt", 'r')
quittext = open('q.txt', 'r')
title = open('title.txt', 'r')
print(bcolors.WARNING + title.read())
print(bcolors.OKGREEN + starttext.read())
print(bcolors.FAIL + quittext.read())

