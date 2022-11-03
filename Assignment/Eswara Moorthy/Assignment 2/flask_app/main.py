from flask import Flask,redirect,url_for,render_template,request,make_response
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=abc.crt;UID=mwk61981;PWD=0HaiGW1Nunm8YlI5",'','')
print(conn)
print("connection successful...")
app = Flask(__name__)




@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        roll_no = request.form['roll_no']
        sql = "INSERT into user values(?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt,1,email)
        ibm_db.bind_param(prep_stmt,2,username)
        ibm_db.bind_param(prep_stmt,3,roll_no)
        ibm_db.bind_param(prep_stmt,4,password)
        ibm_db.execute(prep_stmt)
        #db post operation
        return redirect(url_for('login'))
    elif request.method=='GET':
        return render_template('signup.html')



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM user where username=? and password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        dic = ibm_db.fetch_assoc(stmt)
        print(dic)
        if dic:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    elif request.method=='GET':
        return render_template('login.html')




if __name__=='__main__':
    app.run(debug = True)