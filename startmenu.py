class choices:
    # Choices must be lowercase
    START = "s"
    QUIT = "q"

    @staticmethod
    def is_valid_choice(choice):
        choice = choice.lower()
        return choice == choices.START or choice == choices.QUIT

def print_title_screen():
    class bcolors:
        PURPLE = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDCOLOR = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    starttext = open("s.txt", 'r')
    quittext = open('q.txt', 'r')
    title = open('title.txt', 'r')

    print(bcolors.YELLOW + title.read())
    print(bcolors.GREEN + starttext.read())
    print(bcolors.RED + quittext.read())
    print(bcolors.ENDCOLOR)

print_title_screen()

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
