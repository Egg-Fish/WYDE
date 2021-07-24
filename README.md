# WYDE
A flashcard web application for teachers and students alike

## Description

WYDE is a web platform that uses the concept of spaced repetition to deliver effective learning. 

The concept is simple;
Teachers will create Decks - a set of created flashcards meant to refresh a student's mind. Some decks will have questions
in them that they can do during quiz time. 

When a student wants to revise a topic, he/she can look for the deck that is set up by the teacher and start his/her revision.
The decks are available to the students at any time, 27/4/365.

We believe WYDE is the solution for mitigating the effects of Covid-19 for a few reasons:

* The lack of face-to-face teacher interactions has left students to learn topics albeit on their own. With WYDE, the teachers
can set decks for the students to revise whenever they want to. This gives students an additional resource when it comes to 
home-based learning

* Teachers can gauge class performance better. A teacher can set a deck with content of a new chapter that he/she may want to teach in the
future. Afterwards, he/she can ask the class to start doing the deck before the official start of the lectures. This gives the teacher a
sense of how fast a class can learn a certain topic on their own, and pick up the students who need the extra face-to-face support. Before
Covid-19, teachers had to check and monitor the rate of which a class is learning at. With WYDE, it is as simple as setting a deck and 
watching the process unfold.

* Flashcards are powerful tools. They have been used by medical professionals to push through their infamously gruelling examinations.
With WYDE, this concept of spaced repetition will be reinforced to more people than before. Additionaly, teachers can create decks to
explain common pitfalls and errors to the class. This saves the teacher valuable time as he/she does not need to spend time answering
questions that could be better explained in a flashcard.

## Getting Started

### Dependencies

* Python v3.7.x and above 

### Installing

You can install this by cloning the repository

```bash
git clone https://github.com/Egg-Fish/WYDE.git
cd WYDE
```

Once you are inside the working directory, install the required packages using [pip](https://pypi.org/project/pip/)

Note: It is advisable to create a virtual environment and install the packages in that environment when dealing with 
multiple hackathon submissions.

```bash
pip install -r requirements.txt
```


### Executing program

The server can be run using
```bash
python3 main.py
```
This will listen in on port 80 of the machine


## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details
