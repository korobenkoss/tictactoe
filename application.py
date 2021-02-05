from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], 
                            [None, None, None], 
                            [None, None, None]]
        session["turn"] = "X"

    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    # record user's move
    session["board"][row][col] = session["turn"]

    # check for row win
    for r in range(3):
        win = True
        for c in range(3):
            if session["board"][r][c] != session["turn"]:
                win = False
                continue
        if win:
            return redirect(url_for("result"))

    #check for col win
    for r in range(3):
        win = True
        for c in range(3):
            if session["board"][c][r] != session["turn"]:
                win = False
                continue
        if win:
            return redirect(url_for("result"))

    #check for diag win
    win = True
    for r in range(3):
        if session["board"][r][r] != session["turn"]:
                win = False
    if win:
            return redirect(url_for("result"))

    win = True
    for r in range(3):
        if session["board"][r][len(session["board"]) - 1 - r] != session["turn"]:
                win = False
    if win:
            return redirect(url_for("result"))

    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
    
    return redirect(url_for("index"))

@app.route("/result")
def result():
    return render_template("result.html", turn=session["turn"])

@app.route("/reset")
def reset():
    session.pop("board")

    return  redirect(url_for("index"))