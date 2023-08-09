from flask import Flask,render_template,request
from weather import main as get_weather

import time
from data import insert,getdata
from flask_apscheduler import APScheduler

sched=APScheduler()

app=Flask(__name__)

def getlabels(temp):
    lt=[]
    keys_view = temp.keys()
    keys_list = list(keys_view)
    for key in keys_list:
        lt.append(temp.get(key).get('name'))
    return lt    

def getvalues(temp):
    lt=[]
    keys_view = temp.keys()
    keys_list = list(keys_view)
    for key in keys_list:
        lt.append(temp.get(key).get('main').get('temp'))
    return lt    

@app.route('/', methods=['GET','POST'])
def index():

    data = None
    dt=[]
    labels=[]
    values=[]
    city_name =["Toronto","Vancouver","Ottawa","Montreal","Calgary"]
    state_code=["ON","BC","ON","QC","AB"]
    for x in range(5):
        dt.append(get_weather(city_name[x],state_code[x],"Canada"))
        temp=getdata(city_name[x])
        labels.append(getlabels(temp))
        values.append(getvalues(temp))

    
        

    if request.method =='POST':

       
        city=request.form['cityName']
        state=request.form['stateName']
        country=request.form['countryName']
        data = get_weather(city,state,country)
        # print(data)
        # print(city)
        # # insert()
        # print(labels[0])
        # print(values[0])
    return render_template('index.html',data=data,dt=dt,label=labels,value=values)


if __name__=='__main__':
    
    sched.add_job(id='insert',func=insert,trigger='interval',minutes=60)
    sched.start()
    # sched.add_job(id='getdata',func=getdata,trigger='interval',seconds=10)
    # sched.start()
    app.run(debug=True ,use_reloader=False)
