from flask import Flask, render_template, request
from typing import List
import api

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Starting a new game
        if 'genre' in request.form and 'decade' in request.form and 'secret_movie' not in request.form:
            genre = request.form['genre']
            decade = request.form['decade']
            secret_movie = api.pick_movie(genre, decade)
            first_hint = api.guess_movie(secret_movie, [], [])
            return render_template('index.html', secret_movie=secret_movie, hint_history=[first_hint], guess_history=[])

        # Submitting a guess
        elif 'secret_movie' in request.form and 'current_guess' in request.form:
            secret_movie = request.form['secret_movie']
            hint_history = request.form.getlist('hint_history[]')
            guess_history = request.form.getlist('guess_history[]')
            current_guess = request.form['current_guess']
            guess_history.append(current_guess)
            response = api.guess_movie(secret_movie, guess_history, hint_history)

            if 'CORRECT' in response:
                return render_template('index.html', win=True, secret_movie=secret_movie)

            hint_history.append(response)
            return render_template('index.html', secret_movie=secret_movie, hint_history=hint_history, guess_history=guess_history)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
