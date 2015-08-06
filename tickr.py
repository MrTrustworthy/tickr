#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
__author__ = 'MrTrustworthy'

from flask import Flask, render_template, request, redirect, url_for
import ticketdb

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    # if there are changes, process them
    if request.method == "POST":

        #change state if needed
        if request.form["state"]:
            ticketdb.change_state(request.form["ticket_id"], request.form["state"])

            #add comment if needed
        if request.form["comment"]:
            ticketdb.add_comment(request.form["ticket_id"], request.form["comment"])

        if request.form["deadline"]:
            ticketdb.change_deadline(request.form["ticket_id"], request.form["deadline"])

    #get open tickets if not explicitly changed
    states = request.args.get("states") or "OPEN"

    data = ticketdb.get_all(states)

    return render_template("main.html", data=data)


@app.route("/newticket", methods=["POST"])
def newticket():
    ticketdb.add_ticket(request.form["ticketname"])

    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True)