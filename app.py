from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import hashlib
import uuid
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///kanbanapp.db'
app.config['SECRET_KEY'] = 'theconnectiontomydb'
db=SQLAlchemy(app)

# This is the registration class form.
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

#Create the articles table
class myarticles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=False)
    author = db.Column(db.String(255), unique=False)
    body = db.Column(db.String(400), unique=False)
    CreateDate = db.Column(db.DateTime(timezone=True), default=db.func.now(), unique=False)
    category = db.Column(db.String(255), unique=False)
#Create the Users table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False)
    author = db.Column(db.String(255), unique=False)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=False)
    CreateDate = db.Column(db.DateTime(timezone=True), default=db.func.now(), unique=False)


#The articles class.
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    category = StringField('TODO/DOING/DONE', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

#A class to check if one is logged in. Will be used in decorators all throgh.
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def dictize(raw):
    list=[]
    for all in raw:
        list.append(all.__dict__)
    print(list)
    return tuple(list)
#I want to eliminate this function by fetching the data needed with individual queries from the DB.
@is_logged_in
def fetchUserInfo():
    """"
    raw=dictize(raw)
    articles,todo, doing, done =[],[],[],[]
    for article in raw:
        if article['category'] == "TODO" and article['author'] == session['username']:
            todo.append(article)
            articles.append(article)
        elif article['category'] == "DOING" and article['author'] == session['username']:
            doing.append(article)
            articles.append(article)
        elif article['category'] == "DONE" and article['author'] == session['username']:
            done.append(article)
            articles.append(article)
    return tuple(articles), tuple(todo), tuple(doing), tuple(done)
    """
    articles, todo, doing, done = [], [], [], []
    results={}
    print("Let us see the whole result set as is retrieved.")
    #print(myarticles.query.filter_by(author=session['username']))
    myArticles = dictize(myarticles.query.filter_by(author=session['username']))
    for article in myArticles:
        if article["category"] == "TODO":
            todo.append(article)
        elif article["category"]=="DOING":
            doing.append(article)
        else:
            done.append(article)
        articles.append(article)
    return tuple(articles), tuple(todo), tuple(doing), tuple(done)

# Index
# Check if user logged in
@app.route('/')
@is_logged_in
#This is the home Kanban board, my board.
def index():
    # Get articles

    Articles, todo, doing, done = fetchUserInfo()
    if len(Articles) > 0:
        return render_template('home.html', articles=Articles, todo=todo, doing=doing, done=done)
    else:
        msg = 'No Articles Found'
        return render_template('home.html', msg=msg)
#Validates the JSON is correctly formatted.
def validator(json):
    try:
        eval(json)
    except:
        return False
    if type(eval(json)).__name__ != "dict":
        return False
    for entries in list(eval(json).values()):

        try:
            entries['title']
            entries['body']
            entries['category']
        except:
            return False
    return True
#Process individual entiries in the JSON file
def jsonProcessor(json):
    djson=dict(eval(json))
    return djson['title'],djson['body'],djson['category']

# Handles the JSON uploads.
@app.route('/about', methods=['GET', 'POST'])
@is_logged_in
def about():
    form = ArticleForm(request.form)
    if request.method == 'POST':
        json = form.body.data
        if not validator(json):
            msg = 'Kindly check that your JSON is correctly formated'
            flash(msg,'danger')
            return render_template('about.html', form=form)
        count = 0
        processedJson=list(dict(eval(str(json))).values())
        for entries in processedJson:
            title, body, category = jsonProcessor(str(entries))
            # Execute
            new_article = myarticles(title=title, body=body, author=session['username'], category=category)
            # Commit to DB
            db.session.add(new_article)
            db.session.commit()
            count += 1
        flash('All {} entries made.'.format(count), 'success')
        return redirect(url_for('dashboard'))

    return render_template('about.html', form=form)


# This lists all the tasks
@app.route('/articles')
@is_logged_in
def articles():
    # Create cursor
    # Get articles
    articles,todo,doing,done = fetchUserInfo()
    if len(articles) > 0:

        return render_template('articles.html', articles=done)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)

#This fetches a single task
@app.route('/article/<string:id>/')
@is_logged_in
def article(id):
    raw = myarticles.query.all()

    #articles, todo, doing, done = db.session.query(User, article, todo, doing, done).filter_by(username = username)
    articles, todo, doing, done =fetchUserInfo(raw)
    return render_template('article.html', article=articles)


# The registration process of a user
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = hash_password(str(form.password.data))

        new_user=User(name= name, email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# The log in process of a yser
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        # Create cursor
        #cur = mysql.connection.cursor()

        # Get user by username
        #result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        raw = db.session.query(User).filter_by(username = username).all()
        results=dictize(raw)
        if len(results) > 0:
            # Get stored hash
            password = results[0]['password']
            # Compare Passwords
            if check_password(password, password_candidate):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# The dashboard that lists all your tasks and shows all you data in JSON.
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    # Get articles
    myArticles={}
    articles, todo, doing, done = fetchUserInfo()
    count=1
    for tasks in articles:
        task={'title':tasks['title'], 'body':tasks['body'], 'category':tasks['category'], 'author':tasks['author']}
        myArticles[str(count)]=task
        count+=1
    jsonData = str(myArticles)
    if len(articles) > 0:
        return render_template('dashboard.html', articles = articles, jsonData=jsonData )
    else:
        msg= "Hey there {}. Unfortunately, you have no task history with us, why dont you click the button below to get started :-)!".format(session['username'])
        return render_template('dashboard.html', msg=msg, jsonData=jsonData)
    # Close connection
    cur.close()



# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        category=form.category.data

        # Execute
        new_article=myarticles(title=title,body=body,author=session['username'], category=category)
        # Commit to DB
        db.session.add(new_article)
        db.session.commit()
        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Get article by id
    raw = myarticles.query.filter_by(id=id)
    article=dictize(raw)[0]
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.category.data = article['category']
    form.body.data = article['body']


    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        category = request.form['category']
        app.logger.info(title)
        # Execute
        #cur.execute ("UPDATE articles SET title=%s, body=%s, category=%s WHERE id=%s",(title, body,category, id))
        # Commit to DB
        #mysql.connection.commit()
        article = myarticles.query.filter_by(id = id)
        article.title=title
        article.body=body
        article.category=category
        db.session.commit()
        flash('Article Updated', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Task
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    deleted = myarticles.query.filter_by(id=id).one()
    db.session.delete(deleted)
    db.session.commit()
    flash('Article {} Deleted'.format(id), 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)