from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:abcd@localhost/myDB'

app.debug = True
db = SQLAlchemy(app)

class books(db.Model):
    __tablename__ = 'books'
    booktitle = db.Column(db.String(100), primary_key=True)
    booktext = db.Column(db.String(), nullable=False)
    likes = db.Column(db.Integer(), nullable=False, default=0)

    def __init__(self, booktitle, booktext, likes):
        self.booktitle = booktitle
        self.booktext = booktext
        self.likes = likes

@app.route('/test', methods=['GET'])
def test():
    return
    {
        'test': 'test1'
    }

    
@app.route('/books', methods=['GET'])
def get_books():
    allbooks = books.query.all()
    output = []
    for book in allbooks:
        curbook = {}
        curbook['booktitle'] = book.booktitle
        curbook['booktext'] = book.booktext
        curbook['likes'] = book.likes
        output.append(curbook)
    return jsonify(output)

@app.route('/books', methods=['POST'])
def put_books():
    bookdata = request.get_json()
    book = books(booktitle=bookdata['booktitle'], booktext=bookdata['booktext'], likes=bookdata['likes'])
    db.session.add(book)
    db.session.commit()
    return jsonify(bookdata)

@app.route('/books/<string:booktitle>', methods=['PUT'])
def update_book(booktitle):
    bookdata = request.get_json()
    curbook = bookdata['booktitle']
    book = books.query.filter_by(booktitle=curbook).first()
    book.likes +=1
    #book.booktext = "updated_book_text"
    db.session.commit()
    return jsonify(bookdata)

@app.route('/books/<string:booktitle>', methods=['GET'])
def search_book(booktitle):
    allbooks = books.query.filter(books.booktitle.contains(booktitle)).order_by(books.likes)
    output = []
    for book in allbooks:
        curbook = {}
        curbook['booktitle'] = book.booktitle
        curbook['booktext'] = book.booktext
        curbook['likes'] = book.likes
        output.append(curbook)
    return jsonify(output)

@app.route('/books/<string:booktitle>', methods=['DELETE'])
def delete_book(booktitle):
    bookdata = request.get_json()
    curbook = bookdata['booktitle']
    book = books.query.filter_by(booktitle=curbook).delete()
    db.session.commit()
    return jsonify(bookdata)



if __name__ == "__main__":
    app.run(debug=True)
