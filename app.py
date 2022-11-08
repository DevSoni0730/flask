
from flask import Flask,render_template,request
import pymysql

app=Flask(__name__)

db=None
cur=None

def connectDB():
    global db,cur
    db=pymysql.connect(host='localhost',
                    user='root',
                    password='',
                    database='itvedant')
    cur=db.cursor()    

def disconnectDB():
    db.close()
    cur.close()

def readallrecords():
    connectDB()
    query = 'select * from student'
    cur.execute(query)
    result=cur.fetchall()
    disconnectDB()
    return result

def searchrecord(sid):
    connectDB()
    query=f'select * from student where id={sid}'
    cur.execute(query)
    result=cur.fetchone()
    print(f'ID:{result[0]}\nName:{result[1]}\nMarks:result[2]')
    disconnectDB()
    return result

def insertrecord(sid,name,marks):
    connectDB()
    query = f'insert into student values({sid},"{name}",{marks})'
    cur.execute(query)
    db.commit()
    disconnectDB()

def updaterecord(sid,name,marks):
    connectDB()
    query = f'update student set name="{name}",marks={marks} where id={sid}'
    cur.execute(query)
    db.commit()
    disconnectDB()

def deleterecord(sid):
    connectDB()
    query = f'delete from student where id={sid}'
    cur.execute(query)
    db.commit()
    disconnectDB()

@app.route('/')
def homepage():
    return render_template('index.html',data=readallrecords())

@app.route('/insert')
def insert():
    sid=request.args.get('id')
    name=request.args.get('name')
    marks=request.args.get('marks')
    if sid==None or name==None or marks==None:
        return render_template('insert.html')
    else:
        insertrecord(sid,name,marks)
        return render_template('index.html',data=readallrecords())

@app.route('/update/<sid>',methods=["POST","GET"])
def update(sid):
    if request.method=='POST':
        name=request.form['name']
        marks=request.form['marks']
        updaterecord(sid,name,marks)
        return render_template('index.html',data=readallrecords())
    else:
        return render_template('update.html',data=searchrecord(sid))

@app.route('/delete/<sid>')
def delete(sid):
    deleterecord(sid)
    return render_template('index.html',data=readallrecords())

@app.route('/<name>')
def display(name):
    return render_template('index.html',name=name,msg='hello')

@app.route('/aboutus')
@app.route('/aboutus/<color>')
def aboutus(color='linear-gradient(45deg,pink,blue)'):
    return f'<h1 style="background:{color};padding:175px;font-style:italic;border:1px solid;line-height:40px;font-size:xxx-large;"><br>Address: Itvedant Education Andheri</br> 1st Floor Bina Apartments,<br>Beside Ganpati Mandir,</br>Opposite Arasa Hotel,<br>Near Andheri Metro Station,</br> Andheri (East), Mumbai 400069 <br>Pan India Branches</br> EMAIL ID: mail@itvedant.com </h1>'

@app.route('/contactnumber')
@app.route('/contactnumber/<color>')
def cno(color='linear-gradient(45deg,pink,blue)'):
    return f'<h2 style="background:{color};padding:50px;text-align:left;border:3px solid;">CONTACT NUMBER:+91 9205004404</h2>'

    
if __name__=='__main__':
    app.run(debug=True)


