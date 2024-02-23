import dash
import numpy as np
from dash import html,dcc
from dash.dependencies import Input, Output, State
from dash import callback
from dash import html,dcc,dash_table
from dash.dependencies import Input,Output
from flask_apscheduler import APScheduler
# from utils.utils import Data,ML
from flask import send_from_directory
import os
from utils.callback_py import get_callback

app = dash.Dash(__name__)
# callback_managers.attach_to_app(app)
server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

from flask_apscheduler import APScheduler
from utils.utils import Data,ML



# @callback(
#     Output('id_list_none', 'style'),
#     [Input('all_stock', 'n_clicks')]
# )
# def call_display_stocks(n_clicks):
#     if n_clicks is not None and n_clicks % 2 == 1:
#         return {"display":"block"}
#     else:
#         return {"display":"none"}

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

data = Data()
# data.load_data()
# data.take_uniq_val("secid")

ML_d = ML()
ML_d.predict()


# options=[{"label":"Обзор","value":"Obzor"},{"label":"Свечной анализ","value":"Svecha"},{"label":"Биржевой стакан","value":"Stakan"}
# {"label":"Прогноз. Доходности","value":"Predict"},{"label":"Точности прогноза","value":"Predict"}
@app.server.route('/css/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'css')
    return send_from_directory(static_folder, path)
    
app.layout = html.Div([
                html.Header([
                    html.Div([
                        dcc.Location(id='url',refresh=False),
                        html.Link(rel="stylesheet",href="/css/main.css"),
                    ],className="Main_Color"),html.H1(["OneHotDay"],className="LOGO")
                ],className="header"),
                html.Div([html.Div(
                    [html.Div([dcc.Dropdown(options=[{"label":"Прогноз. Доходности","value":"Benefits"},{"label":"Точности прогноза","value":"MAPE"}],optionHeight=50,clearable=False,placeholder="Сортировка по ......",className="Sorted",id="sorted_val"),dcc.Dropdown(options=[{"label":key[1],"value":key[0]} for key in ML_d.PD_sorted[['tickers','name']].values]
                                  ,searchable=True,placeholder="Выберите или введите акцию....",className="DropDown_stocks",id="DropDown",value="SBER"),html.Div([html.Button(["Информация о акции"],className="Information_stocks",id="button_inform"),html.Div([html.P([],id="head_desc"),html.P([],id="sector_desc"),html.P([],id="desc")],className="list_none",id="id_list_none")],className="button_and_list")],className="Head_doxod"),
                html.Div([html.H1("",id="Name_stocks")],className="TicketName")],className="Take_ticket"),
                html.Div([
                    html.Div([dcc.Dropdown(options=[{"label":"Обзор","value":"Obzor"},{"label":"Свечной анализ","value":"Svecha"}],className="Side_drop_down_1",value="Obzor",id='Obzor',optionHeight=50,clearable=False)],className="Left_sidebar"),
                    html.Div([dcc.Graph(id="Graphic_obzor_r",className="Graphic_obzor")],className="Central_Graphic"),
                    html.Div([dash_table.DataTable(id="Right_table",style_table={'height': '400px', 'overflowY': 'auto'},style_data={'backgroundColor': '#fff7ef',
                                                                                                                                     "font-size":"20px"} 
)],className="Right_sidebar"),
                    
                ],className="panel_body"),
                html.Div([html.H1(["Рекомендательная система"])],className="Rec_system"),
                html.Div([html.Div([dcc.Graph(className="First_Graph",id="One_graph"),html.Div([html.Div([html.P(["Метрика ошибки нейросетевого прогноза"])],className="left_side_div"),html.Div([html.P(["Какая-либо инфа"],id="left_loss")],className="left_side_div")],className="addon_left_side")],className="left_side"),html.Div([dcc.Graph(className="Second_Graph",id="Second_graph"),html.Div([html.Div([html.P(["Максимальная цена"],id="Max_val"),html.P(["Максимальная цена"],id="Min_val")],className="Right_side_div"),html.Div([html.P(["Какая-либо инфа"],id="benifits_doxod")],className="left_side_div")],className="addon_left_side")],className="right_side")],className="Content_body")
]),html.Button(["Оставить заявку"],className="Pos_button"),])


get_callback(app,data,ML_d)
if __name__ == "__main__":
    
    app.run_server(debug=True,host='localhost')