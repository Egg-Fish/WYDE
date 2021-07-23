import os
import random
import hashlib

from flask import Flask, render_template, send_file, request, make_response, session, redirect
from flask_socketio import SocketIO, send, emit

import dbcontroller
import quiz

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(app)



#  ____   ___  _   _ _____ _____ ____  
# |  _ \ / _ \| | | |_   _| ____/ ___| 
# | |_) | | | | | | | | | |  _| \___ \ 
# |  _ <| |_| | |_| | | | | |___ ___) |
# |_| \_\\___/ \___/  |_| |_____|____/ 

def authenticate(username, password):
    student = dbcontroller.get_student_from_username(username)

    password_hash = hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()

    student_hash = student[3]

    return password_hash == student_hash
    

@app.route("/addstudent", methods=["POST"])
def addstudent():
    student_id = request.form["student_id"]
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    password_hash = hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()

    email = request.form["email"]
    class_id = request.form["class_id"]

    dbcontroller.add_student(student_id,name,username,password_hash,email,class_id)
    return "DONE"


@app.route("/login", methods=["GET", "POST"])
def login():
    if method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if authenticate(username, password):

            session["username"] = username
            student = dbcontroller.get_student_from_username(username)
            session["student"] = student

            return redirect("/dashboard.html")
        
        else:
            return render_template("REMOVE") # login page

    elif request.method == "GET":
        return render_template("REMOVE") # login page

@app.route("/addflashcard", methods=["GET", "POST"])
def addflashcard():
    if request.method == "POST":
        deck_id = request.form["deck_id"]
        question = request.form["question"]
        answer = request.form["answer"]

        dbcontroller.add_flashcard(int(deck_id), question, answer)

    elif request.method == "GET":
        return "REMOVE"

@app.route("/addquizquestion", methods=["GET", "POST"])
def addquizquestion():
    if request.method == "POST":
        deck_id = request.form["deck_id"]
        question = request.form["question"]
        answer = request.form["answer"]

        dbcontroller.add_quizquestion(int(deck_id), question, answer)

    elif request.method == "GET":
        return "REMOVE"

@app.route("/adddeck", methods=["GET", "POST"])
def adddeck():
    if request.method == "POST":
        deck_id = random.randint(10000000, 99999999)
        name = request.form["name"]
        description = request.form["description"]

        dbcontroller.add_deck(deck_id, name, description)

    elif request.method == "GET":
        return "REMOVE"

@app.route("/", methods=["GET"])
def index():
    if "student" not in session:
        return render_template("REMOVE") # login

    else:
        return render_template("REMOVE") # dashboard

@app.route("/startdeck/<deck_id>")
def startdeck(deck_id):
    session["inQuiz"] = False
    return render_template("REMOVE", deck_id=deck_id)

@app.route("/startquiz/<deck_id>")
def startquiz(deck_id):
    session["current_card_id"] = 0
    session["inQuiz"] = True
    return render_template("REMOVE", deck_id=deck_id)

#  ____   ___   ____ _  _______ _____ ___ ___  
# / ___| / _ \ / ___| |/ / ____|_   _|_ _/ _ \ 
# \___ \| | | | |   | ' /|  _|   | |  | | | | |
#  ___) | |_| | |___| . \| |___  | |  | | |_| |
# |____/ \___/ \____|_|\_\_____| |_| |___\___/ 


@socketio.event
def nextCard(data):
    current_card_id = int(data["id"])
    inQuiz = False

    if "inQuiz" in session:
        inQuiz = session["inQuiz"]

    current_card = dbcontroller.get_flashcard(current_card_id)
    if not current_card:
        current_card = dbcontroller.get_quizquestion(current_card_id)

    next_card = dbcontroller.get_flashcard(current_card_id+1)
    if not next_card:
        next_card = dbcontroller.get_quizquestion(current_card_id+1)

    if int(next_card[-1]) > 0 and not inQuiz:
        emit("endOfDeck")
        return

    if next_card[1] == current_card[1]:
        emit("nextCard", next_card)
        return

    else:
        emit("endOfDeck")
        return


@socketio.event
def attemptQuestion(data):
    card_id = int(data["id"])
    current_card = dbcontroller.get_flashcard(card_id)
    if not current_card:
        current_card = dbcontroller.get_quizquestion(card_id)

    if int(current_card[-1]) == 0:
        emit("attemptQuestion", {"result": True, "current_card": current_card})

    else:
        attempt = data["attempt"]
        result = quiz.attempt_quizquestion(card_id, attempt)
        emit("attemptQuestion", {"result": result, "current_card": current_card})

@socketio.event
def getDecks(data):
    student = session["student"]

    deck_ids = dbcontroller.get_decks_from_class_id(student["class_id"])

    emit("getDecks", deck_ids)

@socketio.event
def getDeckInfo(data):
    deck = dbcontroller.get_deck_from_deck_id(data["deck_id"])
    emit("getDeckInfo", deck)

@socketio.event
def getUserInfo():
    session["student"] = dbcontroller.get_student_from_username(session["student"][2])
    emit("getUserInfo", session["student"])



# TEST

@app.route("/test/<path:path>")
def test(path):
    print(path)
    return send_file("Pages/" + path)

@app.route("/render/<filename>")
def testrender(filename):
    return render_template(filename)


if __name__ == "__main__":
    app.run(
        host="localhost",
        port=80,
        debug=True
    )