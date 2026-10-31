import os
import secrets
import sqlite3
from functools import wraps

from flask import (Flask, abort, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "portal.db")

app = Flask(__name__)
# IMPORTANT: set a real secret in production (see README).
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


# ---------------------------------------------------------------- database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ---------------------------------------------------------------- security
@app.before_request
def csrf_protect():
    """Every POST form must carry the secret token we gave the browser."""
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    if request.method == "POST":
        sent = request.form.get("csrf", "")
        if not secrets.compare_digest(sent, session["csrf"]):
            abort(400, "Invalid form token. Go back and try again.")


@app.context_processor
def inject_globals():
    return {"csrf_token": session.get("csrf", ""), "current_role": session.get("role"),
            "current_name": session.get("name")}


def login_required(*roles):
    """Allow only logged-in users, optionally only certain roles."""
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if roles and session.get("role") not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


# ---------------------------------------------------------------- auth
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] == "student":
        return redirect(url_for("my_results"))
    return redirect(url_for("all_results"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()  # fresh session on login
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["name"] = user["full_name"]
            session["csrf"] = secrets.token_hex(16)
            return redirect(url_for("home"))
        flash("Wrong login ID or password.")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------- students
@app.route("/my-results")
@login_required("student")
def my_results():
    # The student id comes from the SESSION, never from the URL.
    # That is what guarantees a student can only see their own marks.
    rows = get_db().execute(
        "SELECT exam, subject, marks, max_marks FROM results "
        "WHERE student_id = ? ORDER BY exam, subject",
        (session["user_id"],),
    ).fetchall()
    return render_template("my_results.html", rows=rows)


# ---------------------------------------------------------------- teachers/admin
@app.route("/results")
@login_required("teacher", "admin")
def all_results():
    q = request.args.get("q", "").strip()
    sql = ("SELECT r.id, u.username, u.full_name, r.exam, r.subject, r.marks, r.max_marks "
           "FROM results r JOIN users u ON u.id = r.student_id ")
    params = ()
    if q:
        sql += "WHERE u.username LIKE ? OR u.full_name LIKE ? "
        params = (f"%{q}%", f"%{q}%")
    sql += "ORDER BY u.full_name, r.exam, r.subject"
    rows = get_db().execute(sql, params).fetchall()
    return render_template("all_results.html", rows=rows, q=q)


@app.route("/results/add", methods=["GET", "POST"])
@login_required("teacher", "admin")
def add_result():
    db = get_db()
    students = db.execute(
        "SELECT id, username, full_name FROM users WHERE role='student' ORDER BY full_name"
    ).fetchall()
    if request.method == "POST":
        try:
            student_id = int(request.form["student_id"])
            marks = float(request.form["marks"])
            max_marks = float(request.form["max_marks"])
        except (KeyError, ValueError):
            flash("Please fill all fields with valid numbers.")
            return render_template("add_result.html", students=students)
        exam = request.form.get("exam", "").strip()
        subject = request.form.get("subject", "").strip()
        valid_student = db.execute(
            "SELECT 1 FROM users WHERE id=? AND role='student'", (student_id,)).fetchone()
        if not (exam and subject and valid_student and 0 <= marks <= max_marks and max_marks > 0):
            flash("Check the values: marks must be between 0 and the maximum.")
            return render_template("add_result.html", students=students)
        db.execute(
            "INSERT INTO results (student_id, exam, subject, marks, max_marks) VALUES (?,?,?,?,?)",
            (student_id, exam, subject, marks, max_marks))
        db.commit()
        flash("Result saved.")
        return redirect(url_for("all_results"))
    return render_template("add_result.html", students=students)


@app.route("/results/<int:result_id>/delete", methods=["POST"])
@login_required("teacher", "admin")
def delete_result(result_id):
    db = get_db()
    db.execute("DELETE FROM results WHERE id = ?", (result_id,))
    db.commit()
    flash("Result deleted.")
    return redirect(url_for("all_results"))


# ---------------------------------------------------------------- admin only
@app.route("/users")
@login_required("admin")
def users():
    rows = get_db().execute(
        "SELECT id, username, full_name, role FROM users ORDER BY role, full_name").fetchall()
    return render_template("users.html", rows=rows)


@app.route("/users/add", methods=["GET", "POST"])
@login_required("admin")
def add_user():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        full_name = request.form.get("full_name", "").strip()
        role = request.form.get("role", "")
        password = request.form.get("password", "")
        if not (username and full_name and role in ("student", "teacher", "admin")):
            flash("Please fill all fields.")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.")
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (username, password_hash, full_name, role) VALUES (?,?,?,?)",
                    (username, generate_password_hash(password), full_name, role))
                db.commit()
                flash(f"User '{username}' created.")
                return redirect(url_for("users"))
            except sqlite3.IntegrityError:
                flash("That login ID already exists.")
    return render_template("add_user.html")


@app.route("/users/<int:user_id>/reset-password", methods=["POST"])
@login_required("admin")
def reset_password(user_id):
    password = request.form.get("password", "")
    if len(password) < 8:
        flash("Password must be at least 8 characters.")
    else:
        db = get_db()
        db.execute("UPDATE users SET password_hash=? WHERE id=?",
                   (generate_password_hash(password), user_id))
        db.commit()
        flash("Password updated.")
    return redirect(url_for("users"))


@app.errorhandler(403)
def forbidden(_e):
    return render_template("error.html", msg="You are not allowed to view this page."), 403


if __name__ == "__main__":
    app.run(debug=True)
