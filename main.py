import plotly.utils
from flask import Flask,render_template,send_file,send_from_directory
import os
import plotly.express as px
import pandas as pd
import base64
import json

app = Flask(__name__)

#loading html page
@app.route('/')
def home():
    pd.options.display.float_format = '{:,.2f}'.format
    df_cars = pd.read_csv("datasets/cars.csv")
    df_clean = df_cars.dropna()
    df_clean.MPG = pd.to_numeric(df_clean.MPG)
    df_clean.sort_values('MPG', ascending=False)
    final_chart = df_clean.groupby(by=['Origin', 'MPG']).sum().groupby(level=[0]).cumsum()
    final_chart.reset_index(inplace=True)
    cat_cntry_bar = px.bar(x=final_chart.MPG,
                           y=final_chart.Origin,
                           color=final_chart.Origin,
                           orientation='h',
                           title='Countries with Maximum Mileage')

    cat_cntry_bar.update_layout(xaxis_title='Cars MPG',
                                yaxis_title='Origin')
    graph1JSON=json.dumps(cat_cntry_bar,cls=plotly.utils.PlotlyJSONEncoder)

    df_cereals = pd.read_csv('datasets/cereals.csv')
    df_clean_c = df_cereals.dropna()
    df_clean_c.Calories = pd.to_numeric(df_clean_c.Calories)
    df_clean_c.sort_values('Calories', ascending=False)
    f_chart = df_clean_c.groupby(by=['Manufacturer', 'Calories']).sum().groupby(level=[0]).cumsum()
    f_chart.reset_index(inplace=True)
    cerial_bar = px.bar(x=f_chart.Calories,
                           y=f_chart.Manufacturer,
                           color=f_chart.Manufacturer,
                           orientation='h',
                           title='Cerials Analysis')

    cerial_bar.update_layout(xaxis_title='Number of calories',
                                yaxis_title='Manufacturer')
    graph2JSON = json.dumps(cerial_bar, cls=plotly.utils.PlotlyJSONEncoder)

    df_data = pd.read_csv("datasets/film.csv")
    df_data.Year = pd.to_datetime(df_data.Year)
    final_df = df_data.groupby(['Subject', 'Popularity'],
                               as_index=False).agg({'Awards': pd.Series.count})

    movies_bar = px.bar(final_df,
                   x='Subject',
                   y='Popularity',
                   title='Movies Popularity Analysis',
                   color='Subject'
                   )

    movies_bar.update_layout(xaxis_title='Movies Categories',
                        yaxis_title='Popularity')
    graph3JSON = json.dumps(movies_bar, cls=plotly.utils.PlotlyJSONEncoder)

    df_grocery = pd.read_csv('datasets/grocerystoresurvey.csv')

    df_grocery_final = df_grocery.groupby(['Gender', 'Income'],
                                          as_index=False).agg({'Occupation': pd.Series.count})
    df_grocery_final = df_grocery_final.sort_values('Income')
    grocery_bar = px.bar(df_grocery_final,
                   x='Gender',
                   y='Income',
                   title='Men vs Women Categories',
                   color='Gender',
                   )

    grocery_bar.update_layout(xaxis_title='Sex',
                        yaxis_title='Incomes',
                        )
    graph4JSON = json.dumps(grocery_bar, cls=plotly.utils.PlotlyJSONEncoder)

    df_mutual = pd.read_csv('datasets/mutualfunds.csv')
    df_mutual_final = df_mutual.groupby(['Category', '5YR'],
                                        as_index=False).agg({'Net assets': pd.Series.count})
    df_mutual_finals = df_mutual_final.sort_values('5YR', ascending=False)
    mutual_bar = px.bar(df_mutual_finals,
                   x='Category',
                   y='5YR',
                   title='Mutual Funds Analysis',
                   color='Category'
                   )

    mutual_bar.update_layout(xaxis_title='Funds Categories',
                        yaxis_title='Revenue')

    graph5JSON = json.dumps(mutual_bar, cls=plotly.utils.PlotlyJSONEncoder)







    return render_template("index.html",graph5JSON=graph5JSON,graph4JSON=graph4JSON,graph3JSON =graph3JSON,graph1JSON=graph1JSON,graph2JSON=graph2JSON,car="cars.png",funds="funds.png",store="grocery-store.png",film = "films.png",cereal = "cereals-data.png")

@app.route("/pyscript/<path>")
def sendpyscript(path):
    return send_file(os.path.join("./pyscript",path))
@app.route("/dataset/<path>")
def senddataSet(path):
    return send_file(os.path.join("./datasets",path))
@app.route("/assets/<path>")
def sendfavicon(path):
    return send_file(os.path.join("./assets",path))
# main driver function
if __name__ == '__main__':
    app.run(debug=True,port=8000)
