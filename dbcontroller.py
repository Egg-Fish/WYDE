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
    rf = open("db\cards.csv","r")
    cardslist = []
    for i in rf:
        cardslist.append(i.strip("\n").split(","))
    rf.close()
    for i in cardslist:
        if i[0] == str(id):
            i[2] = question
            i[3] = answer
    wf = open("db\cards.csv","w+")
    for i in range(len(cardslist)):
        wf.write("{},{},{},{},{}".format(cardslist[i][0], cardslist[i][1], cardslist[i][2], cardslist[i][3], cardslist[i][4]))
        wf.write("\n")
    wf.close()

def modify_quizquestion(id, question, answer, points):
    rf = open("db\cards.csv","r")
    cardslist = []
    for i in rf:
        cardslist.append(i.strip("\n").split(","))
    rf.close()
    for i in cardslist:
        if i[0] == str(id):
            i[2] = question
            i[3] = answer
            i[4] = points
    wf = open("db\cards.csv","w+")
    for i in range(len(cardslist)):
        wf.write("{},{},{},{},{}".format(cardslist[i][0], cardslist[i][1], cardslist[i][2], cardslist[i][3], cardslist[i][4]))
        wf.write("\n")
    wf.close()

def get_flashcard(id) -> list:
    f = open("db\cards.csv","r")
    cardslist = []
    for i in f:
        cardslist.append(i.strip("\n").split(","))
    for i in cardslist:
        if i[0] == str(id):
            return i

if __name__ == '__main__':
    # Place tests here
    #add_flashcard(1,"Are you yonglin?","Yes I am ONG")
    #add_quizquestion(1,"1 + 1 = ?", "2", 500)
    #modify_quizquestion(6,"pumpkin","hi",999)
    #print(get_flashcard(5))
    pass