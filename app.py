from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wishes.db'

#Init the SQL db
db = SQLAlchemy(app)

#Model db
class Wishes(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item = db.Column(db.String(120), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.utcnow())

#function to return when add something
    def __repr__(self):
        return '<Name %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    titleIndex = 'To Wish'
    #INSERT INTO
    if request.method == 'POST':
        wish_maked = request.form['wish-maked']
        new_wish = Wishes(item=wish_maked)
        try:
            db.session.add(new_wish)
            db.session.commit()
            return redirect('/')
        except:
            return "That's a problem with make wishes, sorry... "
    else:
        wishes = Wishes.query.order_by(Wishes.date_create)
        return render_template("index.html", title=titleIndex, wishes=wishes)

#UPDATE wishes
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    titleUpdate = 'Update wish'
    wish_update = Wishes.query.get_or_404(id)
    if request.method == 'POST':
        wish_update.item = request.form['wish-maked']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Oh, this it is a problem with update,sorry... "
        else: #bug - no render template
            return render_template("index.html", wish_update=wish_update)

