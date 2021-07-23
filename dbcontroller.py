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
    id = str(id)
    f = open("db\cards.csv","r")
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split(',')
    f.close()

    for i in range(len(lines)):
        print(lines[i][0])
        if lines[i][0] == id:
            del lines[i]
            break
    f = open("db\cards.csv","w+")
    for line in lines:
        for i in line:
            if i == line[-1]:
                f.write(i)
            else:
                f.write(i +",")

    f.close()
    

def modify_flashcard(id, question, answer):
    pass

def modify_quizquestion(id, question, answer):
    pass

def get_flashcard(id) -> list:
    pass

def get_quizquestion(id) -> list:
    f = open("db\cards.csv","r")
    for i in f:
        cardslist = i.strip("\n").split(",")
    for i in cardslist:
        if i[0] == id:
            return i
    pass


if __name__ == '__main__':
    # Place tests here
    #add_flashcard(1,"Are you yonglin?","Yes I am ONG")
    #add_quizquestion(1,"1 + 1 = ?", "2", 500)
    remove_flashcard(1)
    pass