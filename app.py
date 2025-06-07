from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_sqlite_db():
    conn = sqlite3.connect('users.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            with sqlite3.connect('users.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                con.commit()
                msg = "Registered successfully!"
        except:
            con.rollback()
            msg = "Error occurred"
        finally:
            return render_template('result.html', msg=msg)
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con = sqlite3.connect('users.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        data = cur.fetchone()

        if data:
            session['username'] = data['username']
            return redirect('/dashboard/')
        else:
            msg = "Invalid credentials"
            return render_template('login.html', msg=msg)
    return render_template('login.html')

@app.route('/dashboard/')
def dashboard():
    if 'username' in session:
        return f"Welcome {session['username']}!"
    else:
        return redirect('/login/')

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect('/login/')

if __name__ == '__main__':
    app.run(debug=True)
