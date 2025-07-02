from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'hangman_secret'

HANGMAN_EMOJIS = ['😶', '😐', '😟', '😣', '😫', '😵', '💀']

# ✅ Word list with hints
WORDS = {
    'easy': {
        'cat': 'A small domestic animal',
        'sun': 'Bright object in the sky',
        'pen': 'Used for writing',
    },
    'medium': {
        'python': 'Popular programming language',
        'flask': 'Python web framework',
        'resume': 'A document for job applications',
    },
    'hard': {
        'algorithm': 'Set of rules for solving a problem',
        'university': 'Place for higher studies',
        'development': 'Process of creating software',
    }
}

# ✅ Initialize game session
def initialize_game(difficulty):
    word, hint = random.choice(list(WORDS[difficulty].items()))
    session['word'] = word
    session['hint'] = hint
    session['difficulty'] = difficulty

    # Adjust guesses and tries based on difficulty level
    if difficulty == 'easy':
        session['guesses'] = random.sample(list(set(word)), 1)  # Reveal 1 letter
        session['tries_left'] = 8
    elif difficulty == 'medium':
        session['guesses'] = random.sample(list(set(word)), 2)  # Reveal 2 letters
        session['tries_left'] = 6
    elif difficulty == 'hard':
        session['guesses'] = []  # No pre-filled letter
        session['tries_left'] = 5


# ✅ Home Route with difficulty selection
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def set_difficulty():
    difficulty = request.form.get('difficulty', 'medium')
    initialize_game(difficulty)
    return redirect(url_for('game'))

# ✅ Game Route
@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'word' not in session:
        return redirect(url_for('home'))

    word = session['word']
    guesses = session['guesses']
    tries_left = session['tries_left']

    if request.method == 'POST':
        guess = request.form['guess'].lower()
        if guess and guess not in guesses:
            guesses.append(guess)
            if guess not in word:
                tries_left -= 1
            session['guesses'] = guesses
            session['tries_left'] = tries_left

    display_word = ' '.join([letter if letter in guesses else '_' for letter in word])
    emoji = HANGMAN_EMOJIS[6 - tries_left]

    if '_' not in display_word:
        return redirect(url_for('result', outcome='win'))
    elif tries_left <= 0:
        return redirect(url_for('result', outcome='lose'))

    return render_template(
        'game.html',
        display_word=display_word,
        tries_left=tries_left,
        guesses=guesses,
        emoji=emoji,
        hint=session['hint'],
        difficulty=session['difficulty']
    )

# ✅ Result screen
@app.route('/result/<outcome>')
def result(outcome):
    word = session.get('word', '')
    return render_template('result.html', outcome=outcome, word=word)

#✅ Run App
if __name__ == '__main__':
    app.run(debug=True)
