from flask import Flask, render_template,redirect,request
import subprocess
import re
import os
import sys
import pandas as pd
import datetime
from utils.users_dataframe import *
from utils.check_link import *


app = Flask(__name__)

@app.route('/')
def index():
    file_path = './data/active_mac_addresses.txt'
    file_path2 = './data/users.txt'
    contact_count = 0

    with open('./data/current_user.txt','r') as inp:
        mac = inp.read()

    if os.stat(file_path).st_size == 0:
        test = 'Negative'
    else:  
        df,contact_count = check_link()
        df = pd.read_csv(file_path, header=None)
        df.columns = ['mac', 'date']

        if mac in df['mac'].values:
            test = 'Positive'
        else:
            test = 'Negative'
    df2=pd.read_csv(file_path2)
    if mac in df2['mac'].values:
        registered = True
    else:
        registered = False
    
    
    print(test)
    
    return render_template('index.html',test=test, registered = registered,contact_count=contact_count)

@app.route('/check_network', methods=['POST'])
def check_network():

    subprocess.run(['./utils/check_network.py'])
    print("Your connections have been successfully recorded in our database")
        
    return redirect('/')

@app.route('/check_connections', methods=("POST", "GET"))
def check_connections():
    df = users_df()
    del df['mac']
    return render_template("connections_list.html", column_names=df.columns.values, row_data=list(df.values.tolist()),link_column="mac", zip=zip)

@app.route('/return', methods=['POST'])
def go_back():
    return redirect('/')

@app.route('/register', methods=['POST'])
def get_form():
    return render_template('register_user.html')


@app.route('/signup', methods = ['POST'])
def signup():
    name = request.form['name']
    phone = request.form['phone']

    with open('./data/current_user.txt','r') as inp:
        mac = inp.read()
    df = pd.read_csv('./data/users.txt')
    df = df.append({'mac': mac, 'name': name, 'phone': phone}, ignore_index=True) 
    df.to_csv('./data/users.txt',index=None)
    
    return redirect('/')

@app.route('/positive', methods = ['POST'])
def positive_test():
    today = datetime.date.today()
    today = str(today)
    with open('./data/current_user.txt','r') as inp:
        mac = inp.read()
    with open('./data/active_mac_addresses.txt','a') as file:
        file.write(mac+','+today+'\n')
    return redirect('/')

@app.route('/negative', methods = ['POST'])
def negative_test():
    with open('./data/current_user.txt','r') as inp:
        mac = inp.read()
    df = pd.read_csv('./data/active_mac_addresses.txt', header=None)
    df.columns = ['mac', 'date']
    df = df[df.mac != mac]
    df.to_csv('./data/active_mac_addresses.txt',index=None, header=None)
    return redirect('/')

@app.route('/check_covid_link', methods=("POST", "GET"))
def check_covid_link():
    df,contact_count = check_link()
    del df['mac']
    return render_template("covid_contacts_list.html", column_names=df.columns.values, row_data=list(df.values.tolist()),link_column="mac", zip=zip,contact_count=contact_count)


if __name__ == '__main__':
    app.run(debug=True)