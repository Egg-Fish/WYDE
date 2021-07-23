def add_flashcard(deck_id, question, answer):
    f = open("db\cards.csv","r")
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split(',')
    f.close()

    f = open("db\cards.csv", "a+")
    flashcard_id = str(int(lines[-1][0]) + 1)           #taking reference from the last line's id, + 1
    f.write("\n")
    f.write("{},{},{},{},{}".format(flashcard_id, deck_id, str(question), str(answer), 0))

    f.close()

def add_quizquestion(deck_id, question, answer, points):
    f = open("db\cards.csv","r")
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split(',')
    f.close()

    f = open("db\cards.csv", "a+")
    flashcard_id = str(int(lines[-1][0]) + 1)           #taking reference from the last line's id, + 1
    f.write("\n")
    f.write("{},{},{},{},{}".format(flashcard_id, deck_id, str(question), str(answer), points))


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
    #add_flashcard(1,"Are you yonglin?","Yes I am ONG")
    #add_quizquestion(1,"1 + 1 = ?", "2", 500)
    pass