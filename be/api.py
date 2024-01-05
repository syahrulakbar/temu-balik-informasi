import main
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import ekstensi CORS

app = Flask(__name__)
CORS(app)
# query = input("Masukkan query: ")

# main.jurnal(query)

tasks = [
    {
        'id': 1,
        'title': 'Belajar Python',
        'done': False
    },
    {
        'id': 2,
        'title': 'Membuat REST API',
        'done': False
    }
]

# Endpoint untuk mendapatkan semua tugas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/search', methods=['GET'])
def search_jurnal():
    query = request.args.get('query', '')
    results = main.jurnal(query)
    return jsonify({'results': results})


if __name__ == "__main__":
    app.run(debug=True)