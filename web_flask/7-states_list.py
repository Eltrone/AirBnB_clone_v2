#!/usr/bin/python3
"""Starts a Flask web application with listing of states."""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states_list', methods=['GET'], strict_slashes=False)
def states_list():
    states = storage.all("State")
    if states:
        sorted_states = sorted(states.values(), key=lambda state: state.name)
    else:
        sorted_states = []
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown_db(exception):
    """Ferme la session de base de données."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
