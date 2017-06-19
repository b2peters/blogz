from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#intitialize the Blog class
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(999))

    def __init__(self, name, body):
        self.name = name
        self.body=body

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
        if id!=None: 
            blog=Blog.query.get(id)
            blogs=blog
            return render_template('blog.html', blogs=[blogs])

    

@app.route('/newpost', methods=['POST', 'GET'])
def index():
    
    return render_template('newpost.html', blogs=all_blogs())
    
    
if __name__ == '__main__':

    app.run()

