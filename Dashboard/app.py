import pandas as pd 
import numpy as np 
from flask import Flask
from flask import render_template
import json
import csv
import logging
from flask import request
from collections import defaultdict

app = Flask(__name__)

df2 = pd.read_csv(r'data/finaldata.csv')
dfyear= pd.read_csv("data/finaldata.csv")

@app.route("/")
def d3():
  
    return render_template('index2.html')

def dfbycountry(countrycode):
    dfcountry= df2.loc[df2['Code'] == countrycode] 
    return dfcountry

def dfbycountrysun(countrycode):
    dfc1= dfyear.loc[dfyear['Code'] ==countrycode] 
    return dfc1

@app.route('/getDataPerCountryBar')
def getDataPerCountryBar():
    country = request.args.get('country', type=str)
    if country=='All':
        df3=df2.drop_duplicates(['Entity','Year','age']).groupby(['age'])['agecount'].sum().reset_index(name="count")
       
        print("df3")
        print(df3)
    else:
        print("insode app country selected is"+country)
        countryspecificdf = dfbycountry(country)
        df3=countryspecificdf.drop_duplicates(['Entity','Year','age']).groupby(['age'])['agecount'].sum().reset_index(name="count")

        print("df3")
        print(df3)

        #console.log("df3")
        #console.log(df3)
    
    bardata= df3.to_json(orient='records')
    bardata = json.dumps(bardata, indent=2)

    #print("final bar data is " + bardata)    
    return bardata  


@app.route('/getTextData')
def getTextData():
    country = request.args.get('country', type=str)
    if country=="All":
        #incidents = df2.shape[0]
        deaths_df = df2.drop_duplicates(['Entity','Year','drug_type','drug_death']).groupby(['Year','drug_type'])['drug_death'].sum()
        deaths=int(deaths_df.sum())

        print("printing ndeaths")
        print(deaths_df)
        print(deaths)
        sufferings = int(df2.drop_duplicates(['Entity','Year','nsufferings'])['nsufferings'].sum())
        Country="Global"
    else:
        countryspecificdf = dfbycountry(country)
        #incidents = countryspecificdf.shape[0]
        deaths_df = countryspecificdf.drop_duplicates(['Entity','Year','drug_type','drug_death']).groupby(['Year','drug_type'])['drug_death'].sum()
        deaths=int(deaths_df.sum())
        sufferings = int(countryspecificdf.drop_duplicates(['Entity','Year','nsufferings'])['nsufferings'].sum())
        Country = str(countryspecificdf['Entity'].unique()).split("[")[1].split("]")[0].strip("''")
    
    textdata = { "deaths":deaths, "sufferings":sufferings, "Country":Country }
    print("text data")
    print (textdata)
    return json.dumps(textdata)  


@app.route('/getDataPerCountryPie')
def getDataPerCountryPie():
    country = request.args.get('country', type=str)
    if country=='All':
        countdf=df2.drop_duplicates(['Entity','Year','gender']).groupby(['gender'])['gender_count'].sum().reset_index(name="count")
        #countdf["success"]= countdf["success"].astype(str)
        #countdf["success"].replace({"0": "Fail", "1": "Success"}, inplace=True)

        print("countdf")
        print(countdf)

        piedata= countdf.to_json(orient='records')
        piedata = json.dumps(piedata, indent=2)
        return piedata
    else:
        countdf1= dfbycountry(country)
        countdf1=countdf1.drop_duplicates(['Entity','Year','gender']).groupby(['gender'])['gender_count'].sum().reset_index(name="count")
        # countdf1["success"]= countdf1["success"].astype(str)
        # countdf1["success"].replace({"0": "Fail", "1": "Success"}, inplace=True)

        print("countdf1")
        print(countdf1)

        piedata1= countdf1.to_json(orient='records')
        piedata1 = json.dumps(piedata1, indent=2)
        return piedata1

@app.route('/getDataSun')
def getDataSun():
    country = request.args.get('country', type=str)
    #sun data
    
    dfk=dfyear.drop_duplicates(['Entity','Year','drug_type','drug_death']).groupby(['Year','drug_type'])['drug_death'].sum().reset_index(name="kill total")
    dfk.to_csv("year_attack.csv")
    if country=='All':
        #dictionary
        results = defaultdict(lambda: defaultdict(dict))
        with open('year_attack.csv') as csv_file:
            for val in csv.DictReader(csv_file):
                results[val['Year']][val['drug_type']] = (float(val['kill total']))

        
        output = {  'name': 'TOTAL','children': []}

        print("results sun")
        #print(results)

        print("output sun")
        #print(output)

        print("dfk")
        print(dfk)
        

        for k1,v1 in results.items(): 
                children1=[]
                for k2,v2 in v1.items():
                    children1.append({'name':k2,'size':float(v2)})
                
                output['children'].append({
                    'name':k1,
                    'children':children1
                    
                    
                })
        
        sundata = json.dumps(output)
        return sundata
    else:
        dfy= dfbycountrysun(country)
        dfk1=dfy.drop_duplicates(['Entity','Year','drug_type','drug_death']).groupby(['Year','drug_type'])['drug_death'].sum().reset_index(name="kill total")
        dfk1.to_csv("year_attack1.csv")
        results1 = defaultdict(lambda: defaultdict(dict))

        #nested dictionary
        with open('year_attack1.csv') as csv_file:
            for val in csv.DictReader(csv_file):
                results1[val['Year']][val['drug_type']] = (float(val['kill total']))

        print("results1")
        print(results1)
        #json object
        output1 = {  'name': 'TOTAL','children': []}

        
        print("dfk1")
        print(dfk1)

        print("output sun")
        print(output1)

        for k1,v1 in results1.items(): 
                children2=[]
                for k2,v2 in v1.items():
                    children2.append({'name':k2,'size':float(v2)})
                
                output1['children'].append({
                    'name':k1,
                    'children':children2
                    
                    
                })

        print("after output sun")
        print(output1)

        sundata1 = json.dumps(output1)
        return sundata1


if __name__ == "__main__":
    app.run( debug=True)