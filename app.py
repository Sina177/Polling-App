import os.path

import pandas as pd
from flask import Flask, render_template, redirect, request, url_for, make_response

app = Flask(__name__, template_folder="templates")

if not os.path.exists("polls.csv"):
    structure = {
        "id": [],
        "poll": [],
        "option1": [],
        "option2": [],
        "option3": [],
        "votes1": [],
        "votes2": [],
        "votes3": []
    }

    pd.DataFrame(structure).set_index("id").to_csv("polls.csv")

polls_df = pd.read_csv("polls.csv").set_index("id")


@app.route("/")
def index():
    print(polls_df)
    return render_template("index.html", polls=polls_df)


@app.route("/polls/<id>")
def polls(id):
    poll = polls_df.loc[int(id)]
    return render_template("show_poll.html", poll=poll)


@app.route("/polls", methods=["GET", "POST"])
def create_poll():
    if request.method == "GET":
        return render_template("new_poll.html")
    elif request.method == "POST":
        poll = request.form['poll']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']

        if polls_df.empty:
            new_id = 1  # Start ID from 1
        else:
            new_id = max(polls_df.index.values) + 1  # Increment the max index

        polls_df.loc[new_id] = [poll, option1, option2, option3, 0, 0, 0]
        polls_df.to_csv("polls.csv")
        return redirect(url_for("index"))


@app.route("/vote/<id>/<option>")
def vote(id, option):
    if request.cookies.get(f"vote_{id}_cookie") is None:

        polls_df.at[int(id), "votes"+str(option)] += 1
        polls_df.to_csv("polls.csv")

        response = make_response(redirect(url_for("polls", id=id)))
        response.set_cookie((f"vote_{id}_cookie"), str(option))

        return response
    else:
        return render_template("error.html")




if __name__ == "__main__":
    app.run(host = "localhost", debug=True)