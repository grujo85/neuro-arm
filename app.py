import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Flask traži index.html isključivo u folderu 'templates'
    return render_template('index.html')

if __name__ == '__main__':
    # Podešavanje porta za Render okolinu
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
