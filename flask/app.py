from flask import Flask, render_template, request,url_for,redirect,request
from flask_mysqldb import MySQL


app = Flask(__name__)

#mysql connection
app.config["MYSQL HOST"]="Localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="suse"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

#loading home page
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)

#new user
@app.route("/addusers",methods=['GET','POST'])
def addusers():
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con=mysql.connection.cursor()
        sql="insert into users(NAME,CITY,AGE) value (%s,%s,%s)"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))    
    return render_template("addusers.html")

#update user
@app.route("/edituser/<string:id>",methods=['GET','POST'])
def edituser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        sql="update users set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,[name,city,age,id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
        con=mysql.connection.cursor()
    
    sql="select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("edituser.html",datas=res)

#Delete user
@app.route("/deleteuser/<string:id>",methods=['GET','POST'])
def deleteuser(id):
        con=mysql.connection.cursor()
        sql="delete from users where ID=%s"
        con.execute(sql,id)
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    


if __name__ == "__main__":
    app.run(debug=True)
