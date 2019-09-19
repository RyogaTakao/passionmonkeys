from flask import Flask, request, jsonify, make_response, render_template, redirect
import sqlite3
from flask import Blueprint

app = Flask(__name__)

import res 
app.register_blueprint(res.app)
dbname = 'database.db'
conn = sqlite3.connect(dbname,check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

@app.route("/", methods=['GET', 'POST'])
def index():
    return redirect("/j_index")

@app.route("/j_index", methods=['GET', 'POST'])
def j_index():
    user_id = request.args.get('user_id')
    if user_id is None:
        user_id = 1
    cur.execute('SELECT * FROM request, user where request.user_id = user.id and request.status = 0')
    data = cur.fetchall()
    cur.execute('SELECT * FROM user where user.id = ?', (user_id,))
    user = cur.fetchone()

    return render_template('j_index.html', data=data, user=user)

@app.route("/j_detail/<request_id>", methods=['GET', 'POST'])
def j_detail(request_id):
    cur.execute("SELECT * FROM request, user where request.user_id = user.id and request.id = ?", (request_id, ))
    data = cur.fetchone()
    print(dict(data))

    return render_template('j_detail.html', data=data)

@app.route("/j_accept_request", methods=['POST'])
def j_accept_request():
    user_id = request.form['user_id']
    request_id = request.form['request_id']
    cur.execute("update request set helper_id=?, status=1 where id = ?", (user_id, request_id, ))
    conn.commit()

    return render_template('j_approching.html', request_id=request_id)

@app.route("/j_confluence", methods=['POST'])
def j_confluence():
    request_id = request.form['request_id']
    cur.execute('SELECT * FROM request where request.id = ?', (request_id,))
    data = cur.fetchone()

    return render_template('j_guiding.html', data=data)

@app.route("/j_done", methods=['POST'])
def j_done():
    request_id = request.form['request_id']
    cur.execute("update request set status=3 where id = ?", (request_id, ))
    conn.commit()
    cur.execute("select * from user, request where user.id = request.user_id and request.id = ?", (request_id, ))
    data = cur.fetchone()
    print('j_done', dict(data))

    return render_template('j_done.html', data=data)

@app.route("/j_evaluate", methods=['POST'])
def j_evaluate():
    request_id = request.form['request_id']
    rating = request.form['rating']

    return render_template('j_thankyou.html')

@app.route("/f_index", methods=['GET', 'POST'])
def f_index():
    # TODO
    user_id = request.args.get('user_id')
    if user_id is None:
        user_id = 6

    cur.execute('SELECT * FROM user where user.id = ?', (user_id,))
    user = cur.fetchone()

    return render_template('f_categories.html', user_id=user_id, user=user)

@app.route("/f_map", methods=['GET', 'POST'])
def f_map():
    user_id = request.args.get('user_id')
    category = request.args.get('category')
    return render_template('f_map.html', user_id=user_id, category=category)

@app.route("/f_make_request", methods=['GET', 'POST'])
def f_make_request():
    user_id = request.form['user_id']
    category = request.form['category']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    message = request.form['message']
    # APIはここで使う

    cur.execute("insert into request(user_id, category, latitude, longitude, message)  values(?, ?, ?, ?, ?)", (user_id, category, latitude, longitude, message))

    conn.commit()

    return render_template('f_waiting.html', request_id=cur.lastrowid)

@app.route("/f_helper_find", methods=['GET', 'POST'])
def f_helper_find():
    request_id = request.form['request_id']
    return render_template('f_approching.html', user_id=user_id, category=category)

@app.route("/f_confluence", methods=['GET', 'POST'])
def f_confluence():
    request_id = request.form['request_id']
    return render_template('f_guiding.html', request_id=request_id)

@app.route("/f_done", methods=['GET', 'POST'])
def f_done():
    request_id = request.form['request_id']
    cur.execute('SELECT * FROM request, user where request.id = ? ', (request_id,))
    data = cur.fetchone()
    cur.execute('select * from user where id = ?', (data['helper_id'],))
    print("f_done", dict(data))

    return render_template('f_done.html', data=data)

@app.route("/f_evaluate", methods=['GET', 'POST'])
def f_evaluate():
    request_id = request.form['request_id']
    rating = request.form['rating']

    return render_template('f_thankyou.html')


@app.route("/getname", methods=['GET'])
def getname():
    params = request.args
    response = {}
    cur.execute('SELECT name FROM userlist WHERE userID='+ params.get('userID'))
    data = cur.fetchall()
    response.setdefault('name',data[0][0])
    return make_response(jsonify(response))

@app.route("/getdetail", methods=['GET'])
def getdetail():
    params = request.args
    response = {}
    cur.execute('SELECT * FROM userlist WHERE userID='+ params.get('userID'))
    data = cur.fetchall()
    response.setdefault('ID',data[0][0])
    response.setdefault('name',data[0][1])
    response.setdefault('rating',data[0][2])
    response.setdefault('nationality',data[0][3])
    response.setdefault('photo',data[0][4])
    return make_response(jsonify(response))

@app.route("/askforhelp", methods=['POST'])
def askforhelp():
    params = request.get_json()
    userID = params["userID"]
    lat = params["lat"]
    long = params["long"]
    cur.execute('INSERT into requestlist values('+userID+','+lat+','+long+')')
    conn.commit()
    response = {}
    return make_response(response)

@app.route("/removereq", methods=['POST'])
def removereq():
    params = request.get_json()
    userID = params["userID"]
    cur.execute('delete from requestlist where userID =' + userID)
    conn.commit()
    response = {}
    return make_response(response)

@app.route("/regrun", methods=['POST'])
def regrun():
    params = request.get_json()
    #cur.execute('select count(*) from helpinglist')
    #data = cur.fetchall()
    #TaskID = data[0][0] + 1
    helperID = params["helperID"]
    helpeeID = params["helpeeID"]
    cur.execute('INSERT into helpinglist(helperID,helpeeID) values('+helperID+','+helpeeID+')')
    conn.commit()
    response = {}
    cur.execute("SELECT SEQ from sqlite_sequence WHERE name='helpinglist'")
    data=cur.fetchall()
    TaskID=data[0][0]
    response.setdefault('TaskID',str(TaskID))
    return make_response(jsonify(response))

@app.route("/regdone", methods=['POST'])
def regdone():
    params = request.get_json()
    TaskID = params["TaskID"]
    cur.execute('delete from helpinglist where TaskID =' + TaskID)
    conn.commit()
    response = {}
    return make_response(response)

@app.route("/adduser", methods=['POST'])
def adduser():
    params = request.get_json()
    #cur.execute('select count(*) from userlist')
    #data = cur.fetchall()
    #newID = data[0][0] + 1
    newname = params["name"]
    newnationality = params["nationality"]
    newphoto = params["photo"]
    cur.execute("INSERT into userlist(name,rating,nationality,photo) values('"+ newname + "',3.0,'" + newnationality + "','" + newphoto + "')")
    conn.commit()
    response = {}
    cur.execute("SELECT SEQ from sqlite_sequence WHERE name='userlist'")
    data=cur.fetchall()
    newID=data[0][0]
    response.setdefault('userID',str(newID))
    return make_response(jsonify(response))

app.run(debug=False, host='0.0.0.0', port=7070)
