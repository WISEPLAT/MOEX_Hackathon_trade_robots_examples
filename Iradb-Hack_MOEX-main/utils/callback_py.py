import dash
from dash import html,dcc
from dash.dependencies import Input, Output, State
from dash import callback
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
background_Graph = '#2C304D'
paper_backgroud="#252946"
size = '13'
color_green = '#3d9970'
color = 'black'
def get_callback(app,data,ML_d):
    # @app.callback(
    #     Output('id_list_none', 'style'),
    #     [Input('all_stock', 'n_clicks')])
    # def call_display_stocks(n_clicks):
    #     if n_clicks is not None and n_clicks % 2 == 1:
    #         return {"display":"block"}
    #     else:
    #         return {"display":"none"}
    # @app.callback(Output("stocks_val","children"),
    #               Output("Graphic_obzor",'figure'),
    #               Output("Change_price","children"),
    #               State("Date_time","value"),
    #               [Input(key,"n_clicks") for key,value in data.dict_name.items()])
    # def something_do(*value):
    #     print(*value)
    #     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #     value_one = value[0]
    #     # button_number = int(changed_id.split('.')[0].split('-')[-1])
    #     if changed_id.replace(".n_clicks","") == ".":
    #         return ["",{ 'layout': {'font':{'color': color, 'size': size}
    #         }},""]
    #     ticket = data.dict_name[changed_id.replace(".n_clicks","")]
    #     data_back = data.load_data_from_url(changed_id.replace(".n_clicks",""),value_one)
    #     last_val_change = data_back["pr_change"].values[-1]
    #     print(data_back["pr_change"])
    #     last_val_change = "Изменение цены за"+str(value[1])+" % "+str(last_val_change)
    #     figure = {
    #         'data': [
    #             go.Scatter(x=(data_back['tradedate']),
    #                 y=data_back['pr_open'],
    #                 mode='lines+markers'),
                
    #         ],
    #         'layout': {
    #             'xaxis':{"type":'array',
    #                      "tickvals":data_back['tradedate'][::3],
    #                     #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
    #                     "ticktext":data_back['tradedate'].dt.strftime('%H:%M').where((data_back['tradedate'] -data_back['tradedate'].shift(1)).dt.days != 0, data_back['tradedate'].dt.strftime('%Y-%m-%d %H:%M')),
    #                      "tickangle":"-55"}
    #         }
    #     }

    #     return [ticket,figure,last_val_change]

    @app.callback(
        Output('id_list_none', 'style'),
        Output('head_desc', 'children'),
        Output('sector_desc', 'children'),
        Output('desc', 'children'),
        Input('button_inform', 'n_clicks'),
        State('DropDown','value'))
    def call_display_stocks(n_clicks,value): # Функция вывода информации о тикете по нажатию на кнопку
        if n_clicks is not None and n_clicks % 2 == 1:
            data_sec = ML_d.data_ticket[ML_d.data_ticket["ticker"]==value]
            return [{"display":"block"},str(f"Индетификатор : {value}"),str(f"Сектор : {data_sec['sector'].values[0]}",),str(f"{data_sec['short_desc'].values[0]}",)]
        else:
            return [{"display":"none"},str(),str(),str()]

    @app.callback(Output("DropDown","options"),
                  Input("sorted_val","value"))
    def sorted_dropdown(value): # Функция сортировки тикетов
        print(value)
        if value != None:
            if value == "Benefits":
                ML_d.PD_sorted = ML_d.PD_sorted.sort_values(by=["benefits"],ascending=False)
                options=[{"label":str(key[1])+"......."+str(round(key[2],3))+"%","value":key[0]} for key in ML_d.PD_sorted[['tickers','name',"benefits"]].values]
            if value == "MAPE":
                ML_d.PD_sorted = ML_d.PD_sorted.sort_values(by=["mape"])
                options=[{"label":str(key[1])+"......."+str(round(key[2],3))+"^","value":key[0]} for key in ML_d.PD_sorted[['tickers','name',"mape"]].values]
            return options
        else:
            options=[{"label":str(key[1]),"value":key[0]} for key in ML_d.PD_sorted[['tickers','name']].values]
            return options

    @app.callback(Output("Graphic_obzor_r","figure"), 
                  Output("Right_table","columns"),
                  Output("Right_table","data"),
                  Output("Right_table","style_data_conditional"),
                  Input("Obzor","value"),
                  Input("DropDown","value"),)
    def change_drop_down(*value): # Функция вывода информации на графики по выбору значений из выпадающего списка
        print(value)
        if value[1] != None:
            data_back = data.load_data_from_url(value[1],1,value[0])
            if value[0] == "Svecha":
                style_data_conditional=[
            {
                'if': {'filter_query': '{pr_change} > 0'},
                'color': f'{color_green}'
            },
            {
                'if': {'filter_query': '{pr_change} < 0'},
                'color': 'red'
            }]
                figure = {
                        'data' : [
                                    go.Ohlc(x=data_back['tradedate'],
                                                open=data_back["pr_open"],
                                                high=data_back["pr_high"],
                                                low=data_back["pr_low"],
                                                close=data_back["pr_close"])
                                ],
                        'layout': {
                            "title": "Свечной график - Текущая сессия",
                            'xaxis':{"type":'time',
                                    #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
                                    "tickangle":"-55"}
                                }
                            }
                return [figure,[{"name":value,"id":key } for key,value in {'tradetime':'Время','pr_open':'Цена открытия','pr_close':'Цена закрытия','pr_change':'Изменение цены %'}.items()],data_back[['tradetime','pr_open','pr_close','pr_change']].to_dict("records"),style_data_conditional]
            


            elif value[0] == "Obzor":
                # data_back['Color'] = data_back['pr_change'].apply(lambda x: 'green' if x > 0 else 'red')
                # # style_data_conditional = table_value_red_green(data_back,"pr_change")
                style_data_conditional=[
            {
                'if': {'filter_query': '{pr_change} > 0'},
                'color': f'{color_green}'
            },
            {
                'if': {'filter_query': '{pr_change} < 0'},
                'color': 'red'
            }]
                figure = {
                    'data': [
                        go.Scatter(x=(data_back['tradedate']),
                            y=data_back['pr_close'],
                            mode='lines+markers',
                            line = {'color':'rgba(255, 0, 10,1)'}),
                    ],
                    'layout': {
                        "title": "График закрытия - Текущая сессия",
                        'xaxis':{"type":'time',
                                #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
                                # "ticktext":data_back['tradedate'].dt.strftime('%H:%M').where((data_back['tradedate'] -data_back['tradedate'].shift(1)).dt.days != 0, data_back['tradedate'].dt.strftime('%Y-%m-%d %H:%M')),
                                "tickangle":"-55"}
                    }}
                return [figure,[{"name":value,"id":key } for key,value in {'tradetime':'Время','pr_close':'Цена закрытия','pr_change':'Изменение цены %'}.items()],data_back[['tradetime','pr_close','pr_change']].to_dict("records"),style_data_conditional]
            elif value[0] == "Stakan":
                figure = {
                    # 'data': [
                    #     ff.create_distplot(hist_data=[data_back["put_orders_b"],data_back["put_orders_s"]],group_labels=["Открытие","Закрытие"],
                    #                                  colors=['#2BCDC1', '#F66095'])
                    # ],
                    'data': [
                        go.Scatter(y=data_back["put_val_b"], x=data_back["put_val"],mode='lines+markers'),
                        go.Scatter(y=data_back["put_val_s"], x=data_back["put_val"],mode='lines+markers')
                    ],
                    'layout': {
                        "title": "Биржевой стакан - Текущая сессия",
                    }}
                return [figure,[{"name":value,"id":key } for key,value in {'put_val_b':'Сделок на покупку','put_val_s':'Сделок на продажу','put_val':'Объем в деньгах'}.items()],data_back[['put_val_b','put_val_s','put_val']].to_dict("records"),[{}]]
                    # "pr_open","pr_high","pr_low","pr_close","pr_change"
        else:
            return [{'data': [], 'layout': {'font':{'color': color, 'size': size}}},[{"name":" ","id":"1"}],[{}],[{}]]


    def table_value_red_green(data,columns): # Функция окраски данных в таблице, на красный,если ниже 0 или на зеленый,если выше
        style_data_conditional = []
        for row in data[columns]:
            if row > 0:
                style_data_conditional.append({'if': {'row_index': row}, 'color': 'green'})
            else:
                style_data_conditional.append({'if': {'row_index': row}, 'color': 'red'})
        return style_data_conditional

    @app.callback(Output("Name_stocks","children"),
                  Output("One_graph",'figure'),
                  Output("Second_graph",'figure'),
                  Output("left_loss",'children'),
                  Output("Max_val",'children'),
                  Output("Min_val",'children'),
                  Output("benifits_doxod",'children'),
                  Input("DropDown","value"))
    def something_new_do(value): # Вывод данных по рекомендательной системы на графиках
        if value is not None:
            ticket = ML_d.PD_sorted[ML_d.PD_sorted["tickers"]==value]['name']
            data_ML,loss,Max_val,Min_val,benefits_doxod = ML_d.show(value)
            data_back = data.load_data_from_url(value,1,"Obzor")
            figure = {
            'data': [
                go.Scatter(x=(data_ML['tradetime']),
                    y=data_ML['PrognozValAbs'],
                    mode='lines+markers',name="Прогноз"),
                go.Scatter(x=data_back['tradetime'],y=data_back['pr_close'],mode='lines+markers',name="Торги")
            ],
            'layout': {
                "title": "Прогноз и тренд прошлой сессии",
                'xaxis':{"type":'time',
                        #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
                         "tickangle":"-55"}
            }
        }
            figure_1 = {
            'data': [
                go.Scatter(x=(data_ML['tradetime']),
                    y=data_ML['PrognozNewAbs'],
                    mode='lines+markers',name="Прогноз"),
            ],
            'layout': {
                "title":'Прогноз на след. сессию',
                'xaxis':{"type":'time',
                        #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
                         "tickangle":"-55"}
            }
        }
            return [str(ticket.values[0]),figure,figure_1,round(loss,3),"Максимальная цена :"+str(Max_val),"Минимальная цена :"+str(Min_val),f"Прогнозируемый доход :{benefits_doxod} %"]
        else:
            return ["",{ 'layout': {'font':{'color': color, 'size': size}
            }},{ 'layout': {'font':{'color': color, 'size': size}
            }},"","",""]