from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://mgszgjtfvffrgz:06ddfdd12980f5848f3d0d30ea0a20a52d773371412cd10ab9a1c235e209ac36@ec2-54-217-225-16.eu-west-1.compute.amazonaws.com:5432/dfhb33b1aiskat"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    post_text = db.Column(db.String(1000))

def retriveQuery(searchquery):
    posts = Post.query.filter(Post.post_text.ilike('%' + searchquery + '%')).all()
    return render_template('search.html', posts=posts)

@app.route("/")
def home():
    searchquery = request.args.get('searchquery')
    if searchquery:
        return retriveQuery(searchquery)
    else:
        posts = Post.query.all()
        return render_template('home.html', posts=posts)

@app.route("/newpost")
def newpost():
    searchquery = request.args.get('searchquery')
    if searchquery:
        return retriveQuery(searchquery)
    else:
        return render_template('newpost.html')

@app.route('/newpost', methods=['POST'])
def newpostSubmit():
    name = request.form.get('name')
    post = request.form.get('post')

    new_post = Post(name=name, post_text=post)
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(url_for('home'))
