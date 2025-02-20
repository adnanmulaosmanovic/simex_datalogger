import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, dash_table
import sqlite3
import requests
from bs4 import BeautifulSoup

update_frequency=20*1000

# conn=sqlite3.connect('DB_datalogger.db')
# data= pd.read_sql_query('SELECT * FROM datalogger1 ORDER BY id DESC LIMIT 10', conn)
# conn.close()
#print(data)

app=Dash(__name__)

# ...
# app.layout=html.Div([
#     html.H1(id="chanel_03_live"),
#     dcc.Interval(id="update", interval=update_frequency),
# ])

def settings_data_from_datalogger():
    try:

        response = requests.get('http://192.168.1.2/cgi-bin/data.cgi?cmd=settings')
        
        soup=BeautifulSoup(response.text, 'html.parser')
        data = soup.get_text()
        
        data_split=data.split("\n")
        out=[]
        for i in range (0, 10, 1):
            temp=data_split[i]
            out.append(temp.split("\t"))
    
        ch_name=[]
        ch_unit=[]
        ch_max=[]
        ch_min=[]
        for j in range (0,10,1):
            #kreiranje nizova sa podacima - za tabelu
            ch_name.append(out[j][1])
            ch_unit.append(out[j][3])
            ch_max.append(out[j][7])
            ch_min.append(out[j][8])
        #df=pd.DataFrame(out, columns=["Chanel", "Value"])
        #print(ch_max )


    except Exception as e:
    
        print("Error: ", e)
        print("Nije uspjelo povezivanje  111")

    return ch_name, ch_unit, ch_max, ch_min

def data_from_datalogger():
    try:

        response = requests.get('http://192.168.1.2/currentinfo')
        
        soup=BeautifulSoup(response.text, 'html.parser')
        data = soup.get_text()       
        data_split=data.split("\n")
        
        out=[]
        ch_name, ch_unit, ch_max, ch_min =settings_data_from_datalogger()
        for i in range (0, 10, 1):
            temp=data_split[i]
            out.append(temp.split("\t"))
            #dodavanje procitanih vrijednosti - kreiranje tabele
            out[i].insert(1, ch_name[i])
            out[i].append(ch_unit[i])
            out[i].append(ch_max[i])
            out[i].append(ch_min[i])
        #print(out)
    

        df=pd.DataFrame(out, columns=["Chanel","Name", "Value", "Unit", "Max", "Min"])
    #    print(df )
        
    except Exception as e:
    
        print("Error: ", e)
        print("Nije uspjelo povezivanje")

    return df


#########

app.layout = html.Div(
    children=[
        html.H1(children="Pregled"),
        html.P(
            children=(
                "Pregled mjerenja"
                " ----"
            ),
        ),
        html.P(
            children=("Kanal 03:  ")
        ),

        html.H2(id="chanel_03_live",
            style={
                "text-align":"center",
                "padding-top":"30px",
                "background-color":"#CFCFCF"
            }),
        dcc.Graph(
            id="graph_ch_03",
            figure={
                "data": [
                    {
                        "x": [], #data["time"],
                        "y": [], #data["chanel_03"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Temperatura kanal 03 test"},
            },
        ),
         html.H2(id="chanel_07_live",
            style={
                "text-align":"center",
                "padding-top":"30px",
                "background-color":"#CFCFCF"
            }),
        dcc.Graph(
            id="graph_ch_07",
            figure={
                "data": [
                    {
                        "x": [], #data["time"],
                        "y": [], #data["chanel_07"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Temperatura kanal 07"},
            },
        ),
        html.P(
            children=("TEST:::")
        ),
    
        html.Div(id="test"),
        html.Div(id="test_graph"),
        dcc.Interval(id="update", interval=update_frequency),
    ]
)

@app.callback (
    Output("chanel_03_live","children"),
    Output("graph_ch_03", "extendData"),
    Output("chanel_07_live","children"),
    Output("graph_ch_07", "extendData"),
    Output("test", "children"),
    Output("test_graph", "children"),
    Input("update", "n_intervals"),
)

def update_data(intervals):
    conn=sqlite3.connect('DB_datalogger.db')
    cursor=conn.cursor()
    data= cursor.execute("SELECT * FROM datalogger1 ORDER BY id DESC LIMIT 10").fetchall()
    #data= pd.read_sql_query('SELECT * FROM datalogger1 ORDER BY id DESC LIMIT 20', conn)
    conn.close()
    time_last=data[0][1]
    data_ch_07=data[0][9]
    data_ch_03=data[0][5]
    #print(data[0])
#######
    graph_time, graph_ch_1 = data_columns(data)
    
###
    figure1=dict(x= [[time_last]],  y= [[data_ch_03]] )
    figure2=dict(x= [[time_last]],  y= [[data_ch_07]] )
    # kreiranje tabele za prikaz u HTMLu 
    table_data=data_from_datalogger()
    table=dash_table.DataTable(
        id="table",
        data=table_data.to_dict('records')
    )
  #  print(graph_time)
 #    kreiranje grafikona sa arhivskim i live podacima
    chart_fig={
        "data":[
            {
                "x":graph_time,
                "y":graph_ch_1,
                "type":"lines"
            },
        ],
        "layout":{
            "title":{
                "text":"Pregled prethodnih vrijednosti"
            },
            "colorway":["#17B897"]
        },

    }
    graph=dcc.Graph(
        id="graph_test",figure=chart_fig
    )
    return data[0][5], figure1, data_ch_07, figure2, table, graph


def data_columns(data):
    column_time=[]
    column_chanel_1=[]
    for i in range(0, 10, 1):
        column_time.append(data[i][1])
        column_chanel_1.append(data[i][2])
    #print(column_chanel_1)
    return column_time, column_chanel_1

if __name__=="__main__":
    app.run_server(debug=True)