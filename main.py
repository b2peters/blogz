from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

#intitialize the Blog class
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(999))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body=body
        self.owner=owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(90))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username=username
        self.password=password

#a list of all Blog objects
def all_blogs():
    blogs = Blog.query.all()
    return blogs


@app.route('/blog', methods=['GET', 'POST'])
def newpost():
        #validating conditionals
    body_error=''
    title_error=''


    if request.method == 'POST':
        blog_name = request.form['blog_title']
        blog_body = request.form['blog_body']

        #does it have a title
        if blog_name.strip() == "":
            title_error = "Please enter a new title"

        #does body have stuff    
        if blog_body.strip() == "":
            body_error = "Please enter some text"
        
        #return error messages
        if title_error or body_error:
            return render_template("newpost.html", title_error=title_error ,body_error=body_error, blog_title=blog_name, blog_body=blog_body) 
        
        #commit new blog to db
        else:
            new_blog = Blog(blog_name, blog_body)
            db.session.add(new_blog)
            db.session.commit() 
            id = str(new_blog.id)
            return redirect('/blog?id='+id)
    #render a template for a new blog post
    
    else:
        id = request.args.get('id')
        if id : 
            blog=Blog.query.get(id)
            # blogs=blog
            return render_template('blog.html', blogs=[blog])
        else:
            return render_template('blog.html', blogs=all_blogs())

@app.route('/login', methods=['GET', 'POST'])    
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(username=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        elif not user:
            flash('User does not exist')
        else:
            flash('User password incorrect')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=email).first()
        if not existing_user:
            new_user = User(email,password)
            db.session.add(new_user)
            db.session.commit()
            session['email']=email
            return redirect('/newpost')
        else:
            flash('Duplicate user')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    # del session['email']
    session['email']=''
    return redirect('/blog')




@app.route('/newpost', methods=['POST', 'GET'])
def create_new():
    # blogs=blogs
    return render_template('newpost.html', blogs=all_blogs())
    
@app.route('/')
def index():
    users=User.query.all()
    return render_template('index.html', users=users)
    
if __name__ == '__main__':

    app.run()

