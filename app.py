from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'hangman_secret'

HANGMAN_EMOJIS = ['😶', '😐', '😟', '😣', '😫', '😵', '💀']

WORDS = {
    'easy': {
        'cat': 'A small domestic animal',
        'sun': 'Bright object in the sky',
        'pen': 'Used for writing',
        'dog': 'A loyal pet',
        'bus': 'Public transport vehicle',
        'apple': 'A red or green fruit',
        'book': 'Used for reading',
        'fish': 'Lives in water',
        'tree': 'Found in forests or gardens',
        'milk': 'White drink from cows',
        'star': 'Shines in the night sky',
        'egg': 'Oval food from chickens',
        'hat': 'Worn on the head',
        'cup': 'Used for drinking',
        'ball': 'Used in many games',
        'rain': 'Water falling from the sky',
        'shoe': 'Worn on the foot',
        'door': 'Allows entry into a room',
        'car': 'Used for transportation',
        'soap': 'Used for washing',
    },
    'medium': {
        'python': 'Popular programming language',
        'flask': 'Python web framework',
        'resume': 'A document for job applications',
        'planet': 'Earth is one of them',
        'rocket': 'Used to explore space',
        'window': 'Lets light into a room',
        'guitar': 'A musical instrument with strings',
        'bridge': 'Used to cross rivers',
        'mobile': 'Portable communication device',
        'camera': 'Used to take pictures',
        'forest': 'A large area with trees',
        'laptop': 'Portable computer',
        'bottle': 'Holds liquids',
        'pencil': 'Used to write or draw',
        'wallet': 'Holds money and cards',
        'ticket': 'Allows entry somewhere',
        'banana': 'A yellow fruit',
        'doctor': 'Treats patients',
        'museum': 'Place to see historical items',
        'market': 'Place to buy goods',
        'ocean': 'Large body of salt water',
        'glasses': 'Worn to see better',
        'charger': 'Used to power a device',
        'kitchen': 'Room where food is cooked',
        'battery': 'Provides electrical energy',
        'speaker': 'Plays sound or music',
        'notebook': 'Used for writing notes',
        'backpack': 'Used to carry school items',
        'blanket': 'Used to keep warm',
        'printer': 'Produces a hard copy of documents',
        'internet': 'Connects the world online',
        'library': 'Place with books to read or borrow',
        'traffic': 'Vehicles on the road',
        'network': 'System of connections',
        'remote': 'Used to control a device from distance',
        'keyboard': 'Used to type on a computer',
        'monitor': 'Screen for a computer',
        'airplane': 'Flies in the sky',
        'calendar': 'Tracks days and months',
        'science': 'Systematic study of the universe'
    },
    'hard': {
        'algorithm': 'Set of rules for solving a problem',
        'university': 'Place for higher studies',
        'development': 'Process of creating software',
        'cryptography': 'Science of secure communication',
        'architecture': 'Design of buildings or systems',
        'innovation': 'Creation of something new',
        'statistics': 'Study of data',
        'simulation': 'Imitating real-world process',
        'philosophy': 'Study of fundamental nature of reality',
        'neuroscience': 'Study of the brain and nervous system',
        'equilibrium': 'State of balance',
        'biodiversity': 'Variety of life on Earth',
        'infrastructure': 'Basic physical systems of a place',
        'entrepreneur': 'Person who starts a business',
        'nanotechnology': 'Science at atomic scale',
        'consciousness': 'Awareness of self',
        'sustainability': 'Ability to maintain over time',
        'computation': 'Process of calculating',
        'aerodynamics': 'Study of air and motion',
        'metamorphosis': 'Transformation process (e.g., caterpillar to butterfly)',
    }
}

def initialize_game(difficulty):
    word, hint = random.choice(list(WORDS[difficulty].items()))
    session['word'] = word
    session['hint'] = hint
    session['difficulty'] = difficulty

    if difficulty == 'easy':
        session['guesses'] = random.sample(list(set(word)), 1)
        session['tries_left'] = 8
    elif difficulty == 'medium':
        session['guesses'] = random.sample(list(set(word)), 2)
        session['tries_left'] = 6
    elif difficulty == 'hard':
        session['guesses'] = []
        session['tries_left'] = 5

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def set_difficulty():
    difficulty = request.form.get('difficulty', 'medium')
    initialize_game(difficulty)
    return redirect(url_for('game'))

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

@app.route('/result/<outcome>')
def result(outcome):
    word = session.get('word', '')
    return render_template('result.html', outcome=outcome, word=word)

if __name__ == '__main__':
    app.run(debug=True)
