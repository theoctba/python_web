from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
SECRET_KEY = "pudim"
DATABASE = "blog.bd"
app.config.from_object(__name__)


# USER MOCKS
USERNAME = "admin"
PASSWORD = "admin"


def conecta_bd():
    return sqlite3.conecta_bd(DATABASE)


@app.route('/')
def exibir_entradas():
    return render_template("exibir_entradas.html", entradas=posts)


@app.route('/login', methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logado'] = True
            flash("login efetuado com sucesso")
            return redirect(url_for('exibir_entradas'))
        erro = "Usuário ou senha inválidos"
    return render_template("login.html", erro=erro)


@app.route('/logout')
def logout():
    session.pop('logado', None)
    flash("Logout efetuado com sucesso")
    return redirect(url_for('logout'))


@app.route('/inserir', methods=["POST"])
def inserir_entradas(): 
    if not session['logado']: abort(401)
    sql = "INSERT INTO entradas(titulo, texto) VALUES (?, ?)"
    g.bd.execute(sql, [request.form['titulo'], request.form['texto']])
    g.bd.commit()
    flash("Novo Post criado com sucesso!") 
    return redirect(url_for('exibir_entradas'))
