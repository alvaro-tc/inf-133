from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/saludar",methods=['GET'])
def saludar():
    nombre = request.args.get("nombre")
    if not nombre:
        return(
            jsonify({"error":"Se requiere un nombre en los parametros de la URL"}),400,
        )
    return jsonify({"mensaje":f"Hola, {nombre}!"})

@app.route("/sumar",methods=['GET'])
def sumar():
    num1 = request.args.get("num1")
    num2 = request.args.get("num2")
    if not num1:
        return(
            jsonify({"error":"Se requiere un num1 en los parametros de la URL"}),400,
        )
    if not num2:
        return(
            jsonify({"error":"Se requiere un num2 en los parametros de la URL"}),400,
        )

    return jsonify({"mensaje":f"La suma es: {int(num1)+int(num2)}"})


@app.route("/palindromo",methods=['GET'])
def palindromo():
    cadena = request.args.get("cadena")
    if not cadena:
        return(
            jsonify({"error":"Se requiere un cadena en los parametros de la URL"}),400,
        )
    print(cadena.reversed())
    if cadena==cadena[::-1]:
        return jsonify({"mensaje":"La cadena es palindromo"})
    return jsonify({"mensaje":"La cadena NO es palindromo"})

@app.route("/contar",methods=['GET'])
def contar():
    cadena = request.args.get("cadena")
    vocal =request.args.get("vocal")
    if not cadena:
        return(
            jsonify({"error":"Se requiere un cadena y una vocal en los parametros de la URL"}),400,
        )
    if not vocal:
        return(
            jsonify({"error":"Se requiere un vocal en los parametros de la URL"}),400,
        )
    return jsonify({"mensaje":f"La cadena tiene: {cadena.count(vocal)} de letras {vocal}"})
    


if __name__ == "__main__":
    app.run()