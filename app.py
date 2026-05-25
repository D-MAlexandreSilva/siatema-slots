from flask import Flask, render_template, request, redirect, session
import banco as b

app = Flask(__name__)

app.secret_key = "minha_chave_secreta"


@app.route("/")
def home():
    return render_template("cadastro.html")

@app.route("/cadastrar", methods=['POST'])
def cadastrar():
    usuario = request.form['usuario']
    senha = request.form['senha']

    b.cadastrar_usuario(usuario, senha)
    return  redirect("/login")

@app.route("/login")
def logar():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def logando():
    usuario = request.form['usuario']
    senha = request.form['senha']

    resultado = b.login(usuario, senha)
    if resultado:
        session["usuario_id"] = resultado[0]

        return redirect("/painel")
    else:
        return render_template("erro_login.html")

@app.route("/painel")
def painel():
    return render_template("painel.html")



@app.route("/deposito", methods=['GET','POST'])
def deposito():

    if "usuario_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":

       usuario_id = session["usuario_id"]

       valor = request.form['valor']
 
       b.adicionar_deposito(usuario_id, valor)

       return redirect("/painel")

    return render_template("/deposito.html")

@app.route("/saque", methods=['GET','POST'])
def saque():

    if "usuario_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":

       usuario_id = session["usuario_id"]

       valor = request.form['valor']
 
       b.adicionar_saque(usuario_id, valor)

       return redirect("/painel")

    return render_template("/saque.html")

@app.route("/lista")
def lista():
    if "usuario_id" not in session:
        return redirect("/login")
    
    usuario_id = session["usuario_id"]

    depositos = b.listar_deposito(usuario_id)
    saques = b.listar_saque(usuario_id)
    soma_deposito = b.soma_deposito(usuario_id)
    soma_saque = b.soma_saque(usuario_id)
    saldo = soma_saque - soma_deposito


    return render_template("lista.html", depositos=depositos, saques=saques, soma_deposito=soma_deposito, soma_saque=soma_saque, saldo=saldo)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)                                                                                     