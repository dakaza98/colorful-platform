class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class choices:
    # Choices must be lowercase
    START = "s"
    QUIT = "q"

    @staticmethod
    def is_valid_choice(choice):
        choice = choice.lower()
        return choice == choices.START or choice == choices.QUIT

starttext = open("s.txt", 'r')
quittext = open('q.txt', 'r')
title = open('title.txt', 'r')
print(bcolors.WARNING + title.read())
print(bcolors.OKGREEN + starttext.read())
print(bcolors.FAIL + quittext.read())
print(bcolors.ENDC)

while True:
    choice = input("Press S to start or Q to quit\n")

    if choices.is_valid_choice(choice):
        if choice == choices.START:
            # Start game here
            print("Game will now start")
            break
        elif choice == choices.QUIT:
            break
        else:
            raise Exception("Choice " + choice + " has no implementation")
