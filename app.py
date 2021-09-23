from flask import Flask, render_template, request,redirect, url_for
import requests
import json
from view import getdata,insert
from datetime import datetime,time
import math


app = Flask(__name__)



@app.route('/data')
def date():
    stet = getdata()
    data = requests.get('https://gitlab.com/-/snippets/2094509/raw/master/sample_json_3.json')
    info = data.content
    data1 = json.loads(info)


    count = 0
    for i in stet[::-1]:
        count = count + 1
        if count >= 2:
            break
        #print(i)
        try:
            startt = datetime.strptime(i[1],'%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise ValueError('Incorrect data format, should be %Y-%m-%dT%H:%M:%SZ')
        try:
            endt = datetime.strptime(i[2], '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise ValueError('Incorrect data format, should be %Y-%m-%dT%H:%M:%SZ')
        if startt > endt:
            return render_template('404.html')

        start_t = startt.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_t = endt.strftime('%Y-%m-%dT%H:%M:%SZ')
        flag = 0

        l = []
        sum1 = []
        sum2 = []
        final_content = []
        total_belt1 = {}
        total_belt2 = {}
        element_num = {}
        for x in data1:
            datet = datetime.strptime(x['time'], '%Y-%m-%d %H:%M:%S')
            date_time = datet.strftime('%Y-%m-%dT%H:%M:%SZ')
            if start_t <= date_time <= end_t:
                l.append(x['id'][-1])
                if x['state'] == True:
                    x['belt1'] = 0
                    sum1.append(x['belt1'])
                    sum2.append(x['belt2'])
                else:
                    x['belt2'] = 0
                    sum1.append(x['belt1'])
                    sum2.append(x['belt2'])


        #print(l)
        #print(sum1)
        #print(sum2)

        for id, b1, b2 in zip(l, sum1, sum2):
            if id in total_belt1:
                total_belt1[id] += b1
                total_belt2[id] += b2
                element_num[id] += 1
            else:
                total_belt1[id] = b1
                total_belt2[id] = b2
                element_num[id] = 1
        for id in total_belt1:
            total_belt1[id] = total_belt1[id] /(element_num[id])
        #print(total_belt1)
        for id in total_belt2:
            total_belt2[id] = total_belt2[id] / (element_num[id])
        #print(total_belt2)

        for id in sorted(total_belt1.keys()):
            sh = {
            'id': id,
            'avg_belt1': math.trunc(total_belt1[id]),
            'avg_belt2': math.trunc(total_belt2[id])
            }
            final_content.append(sh)

        #print(final_content)

        json_object = json.dumps(final_content)

        with open('def.json','w') as file:
            file.write(json_object)



    return render_template('state.html',jsonfile=json.dumps(final_content,indent = 3))


@app.route('/' ,methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        insert(start_time, end_time)
        return redirect(url_for('date'))


    return render_template('index.html')




if __name__ == '__main__':
    app.run()

