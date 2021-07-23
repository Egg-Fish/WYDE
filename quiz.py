from dbcontroller import get_flashcard


def check_equal(attempt, answer):
    if type(attempt) != type(answer):
        return False
    elif type(attempt) == int and type(answer) == int:
        if attempt == answer:
            return True
        else:
            return False
    elif type(attempt) == float and type(answer) == float:
        if attempt > answer:
            if ((attempt-answer)/answer)*100 < 1:
                return True
            else:
                return False
        else:
            if (abs(attempt-answer)/answer)*100 < 1:
                return True
            else:
                return False
    elif type(attempt) == str and type(answer) == str:
        answerlist = answer.lower().split(" ")
        checklist = answerlist[:]
        attemptlist = attempt.lower().split(" ")
        count = 0
        for i in attemptlist:
            if i in checklist:
                count += 1
                checklist.pop(checklist.index(i))
        if count/len(answerlist) >= 0.7:
            return True
        else:
            return False
    pass

def attempt_quizquestion(id, attempt):
    flashcard = get_flashcard(id)
    answer = flashcard[3]
    if answer.isdigit():
        answer = int(answer)
    else:
        try:
            answer = float(answer)
        except ValueError:
            answer = str(answer)
    return check_equal(attempt,answer)
    pass

if __name__ == '__main__':
    print(attempt_quizquestion(11, 2.3))
    # Place tests here
    pass