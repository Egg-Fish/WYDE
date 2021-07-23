def add_flashcard(question, answer):
    path = "\db\"
    f = open("cards.csv","a+")
    lines = f.readlines()
    f.close()
    del lines[1]

    f = open("cards.csv", "w+")

    for line in lines:
        f.write(line)
    
    f.close()

def add_quizquestion(question, answer):
    pass

def remove_flashcard(id):
    pass

def remove_quizquestion(id):
    pass

def modify_flashcard(id, question, answer):
    pass

def modify_quizquestion(id, question, answer):
    pass

def get_flashcard(id) -> list:
    pass

def get_quizquestion(id) -> list:
    pass


if __name__ == '__main__':
    # Place tests here
    pass