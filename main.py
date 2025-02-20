from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'idksecretkeyorsm'
# Configure the database URI to use SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movieJourney.db"

# Initialize the database
db = SQLAlchemy(app)

#new changes 
# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password= db.Column(db.String(),nullable=False)
    logged_in= db.Column(db.Boolean())
    movies = db.relationship('Movie') #creates the relationship between movies and user. A singlew user acn have multiple movies


#Movie Model
class Movie(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    name= db.Column(db.String(), nullable= False)
    genre = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Float)
    review = db.Column(db.Text)
    image_url = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Create the database tables (run this only once after model)
# with app.app_context():
#     db.create_all()

def check_logged_in_user():
    return User.query.filter_by(logged_in=True).first()
def logout():
    user = User.query.filter_by(logged_in=True).first() #find the user (who is currently using)
    if user:
        user.logged_in = False  #Logout the user
        db.session.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    logged_in = check_logged_in_user()
    if logged_in:
        return redirect(url_for('home'))  # If logged in, redirect to home page
    else:
        return redirect(url_for('login'))  # If not logged in, redirect to login page

@app.route("/signup",methods=["GET","POST"])
def signup():
    logged_in = check_logged_in_user()
    if logged_in:
        logout()
    if request.method=="POST":
        name=request.form.get("username")
        password= request.form.get("password")
        user = User.query.filter_by(username=name).first()
        if user:
            return render_template("signup.html", error="Username already taken.")

        #Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=name,password=hashed_password.decode("utf-8"),logged_in=True)
        db.session.add(new_user) # add the user to the session and commit it to the database
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    logged_in = check_logged_in_user()
    if logged_in:
        logout()

    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        #find the user
        user = User.query.filter_by(username=name).first()

     # check if the username and password match
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

            user.logged_in = True
            db.session.commit()
            return redirect(url_for('home'))  # Redirect to home.html page
        else:
            return render_template("login.html", error="Incoorect Credentials.")
    return render_template("login.html")


@app.route("/home")
def home():
    logged_in = check_logged_in_user()
    if logged_in:
        return render_template("home.html")
    else:
        return redirect(url_for("login"))
@app.route("/logout")
def log_out():
        logged_in=check_logged_in_user()

        if logged_in:
            logout()
        return redirect(url_for('login'))

##WACTHED
@app.route("/watched",methods=["GET","POST"])
def watchlist():
    print("tyest")
    logged_in = check_logged_in_user()
    if not logged_in:
        return redirect(url_for('login'))
    user = User.query.filter_by(logged_in=True).first()

    movies = Movie.query.filter_by(user_id=user.id, status='Watched').all()
    return render_template("watched.html",movies=movies,source="watched")

#ADD WACTHED MOVIE
@app.route("/watched/add",methods=["GET","POST"])
def m_add():
    logged_in = check_logged_in_user()
    user = User.query.filter_by(logged_in=True).first()  # find the user (who is currently using)

    if logged_in:
        if request.method == "POST":
            m_name = request.form.get("m_name")
            m_review = request.form.get("m_review")
            m_rating = request.form.get("m_rating")
            m_genre = request.form.get("m_genre")
            m_img = request.form.get("m_img")
            new_movie = Movie(name=m_name, rating=float(m_rating),image_url=m_img,review=m_review,genre=m_genre, user_id=user.id,status="Watched")
            db.session.add(new_movie)
            db.session.commit()

            return redirect(url_for("watchlist"))
        return render_template('add.html',source="watched")
    else:
        return redirect(url_for('login'))  # If not logged in, redirect to login page



##Wishlist
@app.route("/wishlist",methods=["GET","POST"])
def wishlist():
    logged_in = check_logged_in_user()
    if not logged_in:
        return redirect(url_for('login'))
    user = User.query.filter_by(logged_in=True).first()
    movies = Movie.query.filter_by(user_id=user.id, status='Wishlist').all()
    return render_template("wishlist.html",movies=movies,source="wishlist")

## WIHLIST ADD
@app.route("/wishlist/add",methods=["GET","POST"])
def w_add():
    logged_in = check_logged_in_user()
    user = User.query.filter_by(logged_in=True).first()  # find the user (who is currently using)
    movies = Movie.query.filter_by(user_id=user.id, status='Wishlist').all()
    if logged_in:
        if request.method == "POST":
            m_name = request.form.get("m_name")
            m_review = request.form.get("m_review")
            m_rating = request.form.get("m_rating")
            m_genre = request.form.get("m_genre")
            m_img = request.form.get("m_img")
            new_movie = Movie(name=m_name, rating=float(m_rating),image_url=m_img,review=m_review,genre=m_genre, user_id=user.id,status="Wishlist")
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for('wishlist')) ##redirects After adding
        return render_template('add.html', movies=movies,source="wishlist")
    else:
        return redirect(url_for('login'))  # If not logged in, redirect to login page


#DELETE FOR BOTH
@app.route('/delete_movie/<int:m_id>', methods=['POST'])
def delete_movie(m_id):
    logged_in = check_logged_in_user()
    if logged_in:
        movie = Movie.query.get(m_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            user = User.query.filter_by(logged_in=True).first()
            movies = Movie.query.filter_by(user_id=user.id).all()
            source = request.form.get('source') #kun bata aako ho (/home or /wishlist)
            if source == 'wishlist':
                return redirect(url_for('wishlist')) #wishslit delete garyo bhane wishlist mai redirect
            return redirect(url_for('watchlist'))
    else:
        return redirect(url_for('login'))

@app.route('/completed/<int:m_id>', methods=['POST'])
def completed(m_id):
    logged_in = check_logged_in_user()
    if logged_in:
        movie = Movie.query.get(m_id)
        if movie:
            movie.status="Watched"
            db.session.commit()
            return redirect(url_for('wishlist'))
    else:
        return redirect(url_for('login'))

@app.route('/edit/<int:m_id>',methods=["GET","POST"])
def edit(m_id):
    logged_in= check_logged_in_user()

    if logged_in:
        movie = Movie.query.get(m_id)
        print(movie)
        print(movie.name)
        if movie:
          if request.method == 'POST':
            movie.name = request.form.get("m_name")
            movie.review = request.form.get("m_review")
            movie.rating = request.form.get("m_rating")
            movie.genre = request.form.get("m_genre")
            movie.image_url = request.form.get("m_img")
            db.session.commit()
            return redirect(url_for("watchlist"))
        return render_template('edit.html',movie=movie,source="wishlist")
    else:
     return redirect(url_for('login'))
if __name__ == "__main__":
    app.run(debug=True)
