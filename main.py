import os
import random
import hashlib

from flask import Flask, render_template, send_file, request, make_response, session, redirect
from flask_socketio import SocketIO, send, emit

import dbcontroller
import quiz

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

socketio = SocketIO(app, async_mode="eventlet")



#  ____   ___  _   _ _____ _____ ____  
# |  _ \ / _ \| | | |_   _| ____/ ___| 
# | |_) | | | | | | | | | |  _| \___ \ 
# |  _ <| |_| | |_| | | | | |___ ___) |
# |_| \_\\___/ \___/  |_| |_____|____/ 

def authenticate(username, password):
    student = dbcontroller.get_student_from_username(username)

    if student:
        password_hash = hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()

        student_hash = student[3]

        return password_hash == student_hash

    else:
        return False
    

@app.route("/addstudent", methods=["POST"])
def addstudent():
    student_id = request.form["student_id"]
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    password_hash = hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()

    dbcontroller.add_student(student_id,name,username,password_hash,f"{username}@wdye.com.sg",1)

    session["username"] = username
    session["student"] = dbcontroller.get_student_from_username(username)
    return redirect("/")

@app.route("/signup")
def signup():
    return render_template("sign-up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if authenticate(username, password):

            session["username"] = username
            student = dbcontroller.get_student_from_username(username)
            session["student"] = student

            return redirect("/")
        
        else:
            return render_template("landing-page.html") # login page

    elif request.method == "GET":
        return render_template("landing-page.html") # login page

@app.route("/loginteacher", methods=["GET", "POST"])
def loginTeacher():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        #if authenticate(username, password):
        if True:

            session["username"] = username
            student = dbcontroller.get_student_from_username(username)
            session["student"] = [
                "99999999", 
                "TEACHER", 
                "TEACHER", 
                "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", 
                "teacher@wyde.com", 
                "0000", 
                "TEACHER"]

            return redirect("/")
        
        else:
            return render_template("teacher-log.html") # login page

    elif request.method == "GET":
        return render_template("teacher-log.html") # login page


@app.route("/signout")
def signout():
    session.pop("username")
    session.pop("student")

    return redirect("/")


@app.route("/", methods=["GET"])
def index():
    if "student" not in session:
        return render_template("landing-page.html") # login

    else:
        decks = dbcontroller.get_decks()
        student = session["student"]
        return render_template("main-page.html", decks=decks, dbcontroller=dbcontroller, student=student)


@app.route("/teacher")
def teacherLogin():
    return render_template("teacher-log.html")

@app.route("/student")
def studentLogin():
    return render_template("landing-page.html")

@app.route("/startdeck/<deck_id>")
def startdeck(deck_id):
    if "student" not in session:
        return redirect("/") # login

    session["inQuiz"] = False
    deck = dbcontroller.get_deck_from_deck_id(deck_id)
    return render_template("cards.html", deck=deck, student=session["student"], dbcontroller=dbcontroller)

@app.route("/startquiz/<deck_id>")
def startquiz(deck_id):
    if "student" not in session:
        return redirect("/") # login

    session["inQuiz"] = True
    deck = dbcontroller.get_deck_from_deck_id(deck_id)
    return render_template("cards.html", deck=deck, student=session["student"], dbcontroller=dbcontroller)

@app.route("/editdeck/<deck_id>")
def editdeck(deck_id):
    card_ids = list(map(int, dbcontroller.get_cards_in_deck(deck_id)))

    cards = [dbcontroller.get_flashcard(i) for i in card_ids]

    return render_template("cards-holders.html", cards=cards, student=session["student"], dbcontroller=dbcontroller)

@app.route("/addfc", methods=["GET", "POST"])
def addfc():
    if "student" not in session:
        return redirect("/") # login

    if request.method == "GET":
        decks = dbcontroller.get_decks()
        return render_template("add-fc.html", student=session["student"], dbcontroller=dbcontroller, decks=decks, success=False)

    elif request.method == "POST":
        if request.form["points"]:
            dbcontroller.add_quizquestion(request.form["deck_id"], request.form["question"], request.form["answer"], request.form["points"])
        else:
            dbcontroller.add_flashcard(request.form["deck_id"], request.form["question"], request.form["answer"])

        decks = dbcontroller.get_decks()
        return render_template("add-fc.html", student=session["student"], dbcontroller=dbcontroller, decks=decks, success=True)

@app.route("/adddeck", methods=["GET", "POST"])
def adddeck():
    if "student" not in session:
        return redirect("/") # login

    if request.method == "GET":
        return render_template("add-deck.html", student=session["student"], dbcontroller=dbcontroller, success=False)

    elif request.method == "POST":
        deck_id = random.randint(10000000,99999999)

        dbcontroller.add_deck(deck_id, request.form["name"], request.form["description"])

        return render_template("add-deck.html", student=session["student"], dbcontroller=dbcontroller, success=True)

@app.route("/editcard/<card_id>", methods=["GET", "POST"])
def editcard(card_id):
    if "student" not in session:
        return redirect("/") # login

    if request.method == "GET":
        decks = dbcontroller.get_decks()
        card = dbcontroller.get_flashcard(card_id)
        return render_template("edit-fc.html", student=session["student"], dbcontroller=dbcontroller, card=card, success=False)

    elif request.method == "POST":
        if request.form["method"] == "EDIT":
            dbcontroller.modify_flashcard(card_id, request.form["question"], request.form["answer"])

        elif request.form["method"] == "DELETE":
            dbcontroller.remove_flashcard(card_id)

        return redirect("/")

@app.route("/quiz")
def quizzes():
    if "student" not in session:
        return render_template("landing-page.html") # login

    else:
        decks = dbcontroller.get_decks()
        student = session["student"]
        return render_template("quizzes.html", decks=decks, dbcontroller=dbcontroller, student=student)

#  ____   ___   ____ _  _______ _____ ___ ___  
# / ___| / _ \ / ___| |/ / ____|_   _|_ _/ _ \ 
# \___ \| | | | |   | ' /|  _|   | |  | | | | |
#  ___) | |_| | |___| . \| |___  | |  | | |_| |
# |____/ \___/ \____|_|\_\_____| |_| |___\___/ 


@socketio.event
def nextCard(data):
    current_card_id = int(data["id"])

    if current_card_id == -1:
        next_card_id = dbcontroller.get_cards_in_deck(data["deck_id"])[0]
        next_card = dbcontroller.get_flashcard(next_card_id)
        emit("nextCard", next_card)
        return

    inQuiz = False

    if "inQuiz" in session:
        inQuiz = session["inQuiz"]

    current_card = dbcontroller.get_flashcard(current_card_id)

    next_card = dbcontroller.get_flashcard(current_card_id+1)

    if not next_card:
        emit("endOfDeck")
        return

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
    if filename == "main-page.html":
        decks = dbcontroller.get_decks()
        return render_template("main-page.html", decks=decks, dbcontroller=dbcontroller)


    return render_template(filename)


if __name__ == "__main__":
    socketio.run(
        app=app,
        host="0.0.0.0",
        port=80,
        debug=True
    )