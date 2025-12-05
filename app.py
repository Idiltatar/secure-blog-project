from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "insecure-secret-key" 



def get_db():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.context_processor
def inject_user():
    return dict(current_user=session.get("user"))



@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY created_at DESC
    """)
    posts = cur.fetchall()
    conn.close()
    return render_template("index.html", posts=posts)





@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]   

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, 'user')",
                (email, username, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except Exception as e:
            print("Register error:", e)
            error = "Registration failed."

    return render_template("register.html", error=error)



@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        
        query = f"""
            SELECT * FROM users
            WHERE email = '{email}' AND password = '{password}'
        """

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(query)  
            user = cur.fetchone()
            conn.close()
        except Exception as e:
            print("Login error:", e)
            user = None

        if not user:
            error = "Invalid credentials."
        else:
            session["user"] = {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "role": user["role"],
            }
            return redirect(url_for("index"))

    return render_template("login.html", error=error)



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))



def login_required(fn):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper



@app.route("/posts/new", methods=["GET", "POST"])
@login_required
def new_post():
    error = None

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        user_id = session["user"]["id"]

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
                (user_id, title, content)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
        except Exception as e:
            print("New post error:", e)
            error = "Could not save post."

    return render_template("new_post.html", error=error)



@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = ?
    """, (post_id,))
    post = cur.fetchone()

    if not post:
        conn.close()
        return "Post not found", 404

    cur.execute("""
        SELECT comments.*, users.username
        FROM comments
        LEFT JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = ?
        ORDER BY created_at ASC
    """, (post_id,))
    comments = cur.fetchall()
    conn.close()

    return render_template("post_detail.html", post=post, comments=comments)



@app.route("/posts/<int:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    content = request.form["content"]
    user_id = session["user"]["id"] if "user" in session else None

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)",
        (post_id, user_id, content)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("post_detail", post_id=post_id))




@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    conn = get_db()
    cur = conn.cursor()

   
    cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/search")
def search():
    q = request.args.get("q", "")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE title LIKE ? OR content LIKE ?
    """, (f"%{q}%", f"%{q}%"))
    posts = cur.fetchall()
    conn.close()

   
    return render_template("search.html", query=q, posts=posts)



if __name__ == "__main__":
    app.run(debug=True, port=5001)
