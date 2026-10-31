# Student Result Portal – Beginner Guide

Students log in with their own Login ID and see **only their own** results.
Teachers see and manage **all** results. Admins can do that **and** create users / reset passwords.

Built with Python + Flask (the web server) and SQLite (the database – it is just one file, `portal.db`, so there is nothing separate to install).

---

## Part 1 – Run it on your own computer

### Step 1: Install Python
1. Go to https://www.python.org/downloads/ and download Python 3.11 or newer.
2. **Windows:** on the first installer screen tick **"Add python.exe to PATH"**, then Install.
3. Check it worked: open a terminal (Windows: search "Command Prompt"; Mac: "Terminal") and type `python --version` (on Mac/Linux you may need `python3 --version`).

### Step 2: Open the project folder in the terminal
Unzip `result_portal.zip`, then in the terminal go into the folder, e.g.:
```
cd Downloads\result_portal        (Windows)
cd ~/Downloads/result_portal      (Mac/Linux)
```

### Step 3: Create a virtual environment (a private box for this project's libraries)
```
python -m venv venv
```
Activate it:
```
venv\Scripts\activate             (Windows)
source venv/bin/activate          (Mac/Linux)
```
You should now see `(venv)` at the start of the line.

### Step 4: Install the libraries
```
pip install -r requirements.txt
```

### Step 5: Create the database and the first admin
```
python init_db.py
```
It asks for an admin Login ID, name and password. This creates the file `portal.db`.

### Step 6: Start the server
```
python app.py
```
Open http://127.0.0.1:5000 in your browser and log in as the admin.

### Step 7: Use it
1. **Users → Add user**: create a teacher, and create each student (Login ID could be their roll number).
2. **Add result**: pick a student, exam, subject, marks.
3. Log out, log in as a student, and confirm they see only their own marks.

Stop the server with `Ctrl + C`.

---

## Part 2 – How it works (so you can learn from it)

| File | What it does |
|---|---|
| `init_db.py` | Creates the two tables: `users` and `results` |
| `app.py` | The server: login, logout, and every page with its permission rules |
| `templates/*.html` | The pages you see |

**The key security idea:** the page `/my-results` never takes a student ID from the URL. It uses the ID stored in the logged-in session, so a student cannot change a number in the address bar to peek at someone else. Teacher/admin pages are guarded by `@login_required("teacher", "admin")`, and the user-management pages by `@login_required("admin")`.

Passwords are never stored as plain text – only a salted hash. Forms carry a CSRF token to stop other websites submitting forms on a user's behalf.

---

## Part 3 – Put it on the internet

Running on your computer only works for you. To let students use it, host it. Easiest beginner option: **PythonAnywhere** (free tier exists; paid is better for a real school).

1. Create an account at https://www.pythonanywhere.com
2. **Files** tab → upload `result_portal.zip` → in a **Bash console** run `unzip result_portal.zip`
3. In the console:
   ```
   cd result_portal
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   python init_db.py
   ```
4. **Web** tab → *Add a new web app* → *Manual configuration* → pick your Python version.
5. Set **Source code** to your `result_portal` folder and **Virtualenv** to `.../result_portal/venv`.
6. Open the **WSGI configuration file** link and replace its contents with:
   ```python
   import sys, os
   path = "/home/YOURUSERNAME/result_portal"
   if path not in sys.path:
       sys.path.insert(0, path)
   os.environ["SECRET_KEY"] = "PASTE-A-LONG-RANDOM-STRING-HERE"
   from app import app as application
   ```
   Make a random string by running `python -c "import secrets; print(secrets.token_hex(32))"`.
7. Click **Reload**. Your site is live at `YOURUSERNAME.pythonanywhere.com` (HTTPS is included).

Other options when you outgrow this: Render, Railway, or a VPS (run with `gunicorn app:app` behind Nginx).

---

## Part 4 – Before real students use it (checklist)

- [ ] Set a real `SECRET_KEY` (step 6 above). Never use the default.
- [ ] Use HTTPS only (PythonAnywhere/Render do this for you).
- [ ] Never run with `debug=True` on the internet (`python app.py` is for your own computer only).
- [ ] **Back up `portal.db`** regularly – copy the file somewhere safe. It *is* your whole database.
- [ ] Give students a strong starting password and ask them to keep it private (admins can reset passwords on the Users page).
- [ ] This is a solid starter, but it has no "student changes own password" page, no login-attempt limiting, and no bulk CSV import. Those are good next features to add.
- [ ] Results are personal data. Check what your school's/country's rules say about storing and showing student records.

## Common problems

- **`python` not recognised** – reinstall Python and tick "Add to PATH", or try `python3`.
- **`No module named flask`** – you forgot to activate the venv (Step 3) or run Step 4.
- **"Invalid form token"** – the page was open too long or cookies are blocked; reload and try again.
- **Forgot admin password** – delete `portal.db` only if you have no data you need; otherwise ask me and I'll give you a small reset script.
