
from unicodedata import name
from flask import Flask, request ,  render_template ,url_for,redirect
import json
import pandas as pd
import os
from werkzeug.utils import secure_filename
import subprocess

from random import randint

app = Flask(__name__)

# @app.route("/testview",methods = ['POST','GET'])
# def testview():
#    return render_template('testview.html')

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_files():
#    if request.method == 'POST':
#       f = request.files['file']
#       filename = secure_filename(f.filename)
#       f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#       return 'file uploaded successfully'


# @app.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)

##webapp
@app.route("/index",methods = ['POST','GET'])
def index():
    return render_template("index.html")

@app.route("/home",methods = ['POST','GET'])
def home():
    dbpd = pd.read_csv('webdb.csv')
    if request.method == "POST":
        car_id = request.form.get('car_id')
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        insu = request.form.get('insurance')
        namecar = request.form.get('namecar')
        subnamecar = request.form.get('subnamecar')
        f = request.files['file']
        filename = car_id + '.obj'
        filename2 = car_id + '.mtl'
        filename3 = car_id + '.png'
        os.makedirs('file/'+str(car_id))
        UPLOAD_FOLDER = 'file/'+str(car_id)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        os.makedirs('static/images/data/base/'+str(car_id)+"/"+str(car_id))
        path = 'base'
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
        dbpd = dbpd.append({'car_id':car_id,'fname':first_name
                            ,'lname':last_name,'insurance':insu
                            ,'modelname':filename,'tcar':namecar
                            ,'subtcar':subnamecar},ignore_index=True)
        dbpd.to_csv('webdb.csv',index=False)
        pro = subprocess.Popen(["python","updatejson.py","--obj",str(car_id),"--path",str(path)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pro.communicate()
        subprocess.run(["python","render.py"])

        return redirect(url_for('show'))



@app.route("/show",methods = ['POST','GET'])
def show():
    data = pd.read_csv('webdb.csv',on_bad_lines='skip')
    data = data.to_numpy()

    return render_template("showdata.html",datas= data)

@app.route("/view",methods = ['POST','GET']) #check
def view():
    datainsu = pd.read_csv('insu.csv')
    car_id = request.form.get('car_id')
    insu = request.form.get('insurance')

    #select price
    car_p = pd.read_csv('webdb.csv', on_bad_lines='skip')
    g = car_p['car_id'] == car_id
    q = car_p[g]
    zq = q['tcar']
    zq = zq.to_numpy()
    zqs = q['subtcar']
    zqs = zqs.to_numpy()


    cost = pd.read_excel('car_price.xlsx')
    zc = cost['ยี่ห้อ'] == zq[0]
    zsc = cost[zc] 
    zt = zsc['รุ่น'] == zqs[0]
    ztc = zsc[zt]
    u = ztc['ราคา']
    u = u.to_numpy()
 
 
    if u <= 700000:
        dataprice = pd.read_csv('Lower700k.csv')
    elif 700000 < u <= 1200000:
        dataprice = pd.read_csv('700k-1.2m.csv')
    elif u > 1200000:
        dataprice = pd.read_csv('more_than1.2m.csv')
    
    price = dataprice.to_numpy()
    
    #
    pro = subprocess.Popen(["python","compare.py","--c",str(car_id)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout,stderr) = pro.communicate()
    text = str(stdout,'utf-8')
    text = text.rstrip("\n")
    data = datainsu.to_numpy()
    c = randint(0,(len(data) - 1))
    b1 = os.path.join('static/images/data/dmg/'+str(car_id)+"/"+str(car_id)+"/"+str(car_id)+"_elev0_มุม0.png")
    b2 = os.path.join('static/images/data/dmg/'+str(car_id)+"/"+str(car_id)+"/"+str(car_id)+"_elev0_มุม90.png")
    b3 = os.path.join('static/images/data/dmg/'+str(car_id)+"/"+str(car_id)+"/"+str(car_id)+"_elev0_มุม180.png")
    b4 = os.path.join('static/images/data/dmg/'+str(car_id)+"/"+str(car_id)+"/"+str(car_id)+"_elev0_มุม270.png")

    t = [text[0],text[3],text[6],text[9]]
    a = []
    b = []
    ta = []
    tb = []
    for i in range(0,4):
        if t[i] == 'N':
            a.append(0)
            b.append(0)
        elif t[i] == 'L':
            a.append(price[i,1])
            b.append(price[i,2])
        elif t[i] == 'M':
            a.append(price[i,3])
            b.append(price[i,4])
        elif t[i] == 'H':
            a.append(price[i,5])
            b.append(price[i,6])
    ta = sum(a)
    tb = sum(b)



    return render_template("showran_insu.html",outs = text, pri = price,toa = ta,tob=tb,b1=b1,b2=b2,b3=b3,b4=b4)

@app.route("/testp",methods = ['POST','GET'])
def testp():
    return render_template("test.html")      

@app.route("/compare",methods = ['POST','GET'])
def compare():
    return render_template("render.html")      

@app.route("/render",methods = ['POST','GET'])
def render():

    datainsu = pd.read_csv('insu.csv')
    car_id = request.form.get('car_id')
    #select price
    car_p = pd.read_csv('webdb.csv', on_bad_lines='skip')
    g = car_p['car_id'] == car_id
    q = car_p[g]
    zq = q['tcar']
    zq = zq.to_numpy()
    zqs = q['subtcar']
    zqs = zqs.to_numpy()


    cost = pd.read_excel('car_price.xlsx')
    zc = cost['ยี่ห้อ'] == zq[0]
    zsc = cost[zc] 
    zt = zsc['รุ่น'] == zqs[0]
    ztc = zsc[zt]
    u = ztc['ราคา']
    u = u.to_numpy()
 
 
    if u <= 700000:
        dataprice = pd.read_csv('Lower700k.csv')
    elif 700000 < u <= 1200000:
        dataprice = pd.read_csv('700k-1.2m.csv')
    elif u > 1200000:
        dataprice = pd.read_csv('more_than1.2m.csv')
    
    price = dataprice.to_numpy()
    
    #
    f = request.files['file']
    data = datainsu.to_numpy()
    a = randint(0,(len(data) - 1))
    filename = car_id + '.obj'
    filename2 = car_id + '.mtl'
    filename3 = car_id + '.png'
    os.makedirs('file/'+str(car_id)+'dmg')
    UPLOAD_FOLDER = 'file/'+str(car_id)+'dmg'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs('static/images/data/dmg/'+str(car_id)+"/"+str(car_id))
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
    path = 'dmg'
    pro = subprocess.Popen(["python","updatejson_dmg.py","--obj",str(car_id),"--path",str(path)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pro.communicate()
    subprocess.run(["python","render.py"])
    pro = subprocess.Popen(["python","compare.py","--c",str(car_id)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout,stderr) = pro.communicate()
    text = str(stdout,'utf-8')
    text = text.rstrip("\n")
    #total price
    t = [text[0],text[3],text[6],text[9]]
    a = []
    b = []
    ta = []
    tb = []
    for i in range(0,4):
        if t[i] == 'N':
            a.append(0)
            b.append(0)
        elif t[i] == 'L':
            a.append(price[i,1])
            b.append(price[i,2])
        elif t[i] == 'M':
            a.append(price[i,3])
            b.append(price[i,4])
        elif t[i] == 'H':
            a.append(price[i,5])
            b.append(price[i,6])
    ta = sum(a)
    tb = sum(b)
    

    b1 = os.path.join('static/images/data/dmg/'+str(car_id)+"/"+str(car_id)+"/"+str(car_id)+"_elev0_มุม0.png")
    b2 = os.path.join('static/images/data/dmg/'+str(car_id)+"/"+str(car_id)+"/"+str(car_id)+"_elev0_มุม90.png")
    b3 = os.path.join('static/images/data/dmg/'+str(car_id)+"/"+str(car_id)+"/"+str(car_id)+"_elev0_มุม180.png")
    b4 = os.path.join('static/images/data/dmg/'+str(car_id)+"/"+str(car_id)+"/"+str(car_id)+"_elev0_มุม270.png")


    return render_template("showran_insu.html",outs = text,insu = data[a], pri = price,toa = ta,tob=tb,
    b1=b1,b2=b2,b3=b3,b4=b4)

@app.route("/homepage",methods = ['POST','GET'])
def homepage():
    return render_template("home.html")

# @app.route("/output",methods = ['POST','GET'])
# def output():
#     car_id = request.form.get('car_id')
#     pro = subprocess.Popen(["python","compare.py","--c",str(car_id)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     (stdout,stderr) = pro.communicate()
#     text = str(stdout,'utf-8')
#     text = text.rstrip("\n")
#     return render_template("out.html",outs = text)

if __name__ == "__main__":
    app.run(debug = True)# host ='0.0.0.0',port=5001 