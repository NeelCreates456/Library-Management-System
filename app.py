from flask import Flask, render_template, redirect, request, flash, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "library_secret"

issued_books = []
users = {}

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/dashboard")

        else:
            flash("Invalid username or password")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users[username] = password

        flash("Account created successfully!")

        return redirect("/login")

    return render_template("signup.html")


# ---------------- BOOKS PAGE ----------------
@app.route("/books")
def books():

    if "user" not in session:
        return redirect("/login")

    books_list = [
        {"title":"Artificial Intelligence","author":"Stuart Russell","image":"book1.png","category":"Programming"},
        {"title":"Machine Learning","author":"Tom Mitchell","image":"book2.png","category":"Programming"},
        {"title":"Python Programming","author":"Mark Lutz","image":"book3.png","category":"Programming"},
        {"title":"Data Structures","author":"Robert Lafore","image":"book4.png","category":"Programming"},

        {"title":"Rich Dad Poor Dad","author":"Robert Kiyosaki","image":"book5.png","category":"Business"},
        {"title":"Zero to One","author":"Peter Thiel","image":"book6.png","category":"Business"},
        {"title":"The Lean Startup","author":"Eric Ries","image":"book7.png","category":"Business"},
        {"title":"Think and Grow Rich","author":"Napoleon Hill","image":"book8.png","category":"Business"},

        {"title":"Spider Man","author":"Marvel","image":"book9.png","category":"Comics"},
        {"title":"Batman","author":"DC Comics","image":"book10.png","category":"Comics"},
        {"title":"Avengers","author":"Marvel","image":"book11.png","category":"Comics"},
        {"title":"Superman","author":"DC Comics","image":"book12.png","category":"Comics"}
    ]

    for book in books_list:
        book["issued"] = False
        for issued in issued_books:
            if issued["title"] == book["title"]:
                book["issued"] = True

    return render_template("books.html", books=books_list)

# ---------------- DASHBOARD ----------------
from datetime import datetime, timedelta

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        books=issued_books,
        timedelta=timedelta
    )
# ---------------- FINE -----------------
@app.route("/fine")
def fine():

    fine_amount = session.get("fine", 0)

    return render_template("fine.html", fine=fine_amount)

# ---------------- ISSUE BOOK ----------------
from datetime import datetime

@app.route("/issue/<book_title>")
def issue_book(book_title):

    for book in issued_books:
        if book["title"] == book_title:
            flash("Book already issued!")
            return redirect("/books")

    issued_books.append({
        "title": book_title,
        "issue_date": datetime.now()
    })

    flash("Book issued successfully!")
    return redirect("/dashboard")

# ---------------- RETURN BOOK ----------------
@app.route("/return/<book_title>")
def return_book(book_title):

    global issued_books

    for book in issued_books:
        if book["title"] == book_title:
            issued_books.remove(book)
            break

    flash("You have successfully returned the book!")

    return redirect("/dashboard")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)