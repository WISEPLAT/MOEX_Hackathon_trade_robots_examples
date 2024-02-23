# импорт необходимых библиотек
import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from moexalgo import Ticker
from collections import defaultdict
import requests


sess = requests.Session()
host = "http://127.0.0.1:8080/"
data = {"login": "user", "password": "user"}
sess.post(host + "user.login", json=data)


def get_user_balance():
    r = sess.get(host + "balance.user")
    balance = r.json()["data"]["balance"]
    return float(balance)


def get_metric():
    r = sess.get(host + "metric.join.list")
    metrics = r.json()["data"]["metrics"]
    return metrics


def get_user_briefcase():
    r = sess.get(host + "briefcase.join.list")
    briefcase = r.json()["data"]["briefcases"]
    if len(briefcase) > 0:
        df = pd.DataFrame(briefcase)
        df = (
            df.groupby(["tisker", "name"])[["price", "quantity", "amount"]]
            .agg({"price": "mean", "quantity": "sum", "amount": "sum"})
            .reset_index()
        )
        return df.rename(
            columns={
                "tisker": "Код инструмента",
                "name": "Наименование акции",
                "price": "Цена за ед., ₽",
                "quantity": "Количество",
                "amount": "      Итого, ₽      ",
            }
        )
    else:
        return briefcase

def get_tiskers():
    r = sess.get(host + "tisker.list")
    tiskers = r.json()["data"]["tiskers"]
    return tiskers

def make_metric(metric: dict):
    label = metric["tisker"]
    value = str(metric["value"]) + " ₽"
    delta = str(metric["delta"]) + " %"
    help = metric["name"]
    return {"label": label, "value": value, "delta": delta, "help": help}


if "balance" not in st.session_state:
    st.session_state.balance = get_user_balance()

if "briefcase" not in st.session_state:
    st.session_state.briefcase = get_user_briefcase()

if "clicked" not in st.session_state:
    st.session_state.clicked = False

if "df" not in st.session_state:
    st.session_state.df = defaultdict()

if "metric" not in st.session_state:
    st.session_state.metric = [make_metric(metric) for metric in get_metric()]


def click_button():
    st.session_state.clicked = True


def make_features(data, column_list, lags_list, shift_list):
    data = data.copy()

    data["month"] = data.index.month
    data["min_max_diff"] = data.high - data.low
    data["open_close_diff"] = data.open - data.low
    data["weekday"] = data.index.map(lambda x: x.weekday())
    column_list = column_list + ["min_max_diff", "open_close_diff"]

    for col in column_list:
        for lag in lags_list:
            data[f"{col}_lag_{lag}"] = data[col].shift(lag)

        for i in shift_list:
            data[f"{col}_rolling_mean_{i}"] = data[col].rolling(i).mean().shift(1)

    return data


lags_list = [6, 7, 8, 9]
shift_list = [1, 5, 3]


# голубые фишки Московской Биржи (код инструмента)
MOEXBC = [ticker["tisker"] for ticker in get_tiskers()]

# расшифровка кода инструмента (голубые фишки Московской Биржи)
MOEXBC_DICT = {ticker["tisker"]:ticker["name"] for ticker in get_tiskers()}

# конфигурация страницы web - сервиса
st.set_page_config(
    page_title="GO.ALGO, Сервис по построению торговых решений на основе данных AlgoPack",
    page_icon="https://static.tildacdn.com/tild3237-6136-4931-b732-333166393831/Group_1.svg",
    layout="wide",
)

# заголовок страницы web - сервиса (header)
col1, col2 = st.columns([1, 5])
col1.markdown(
    """<p><img src="https://static.tildacdn.com/tild3237-6136-4931-b732-333166393831/Group_1.svg" align="middle" /> </p>""",
    unsafe_allow_html=True,
)
col2.markdown(
    "<p style='text-align: center; font-size:30px; color: blac;'><STRONG>GO.ALGO, MOEX - Московская биржа</STRONG></p>",
    unsafe_allow_html=True,
)
col2.markdown(
    "<p style='text-align: center; font-size:20px; color: blac;'>Сервис по построению торговых решений на основе данных AlgoPack</p>",
    unsafe_allow_html=True,
)



def get_data_candle(ticker: str):
    data = Ticker(ticker)
    data_candles = data.candles(date="2022-09-03", till_date="2023-12-01", period="D")
    data_df = [candle for candle in data_candles]
    df = pd.DataFrame(data_df)
    return {ticker: df}


st.session_state.df = [get_data_candle(ticker) for ticker in MOEXBC]


def show_data_candles(df: pd.DataFrame, ticker: str):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["begin"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
            )
        ]
    )

    fig.update_layout(
        title=f"Тренд акций {ticker}",
        yaxis_title=f"{ticker} Stock",
        height=600,
        shapes=[
            dict(
                x0="2023-09-01",
                x1="2023-09-01",
                y0=0,
                y1=1,
                xref="x",
                yref="paper",
                line_width=2,
            )
        ],
        annotations=[
            dict(
                x="2023-09-01",
                y=0.05,
                xref="x",
                yref="paper",
                showarrow=False,
                xanchor="left",
                text="Прогнозный период на 3 (три) месяца",
            )
        ],
    )

    return fig


# стиль отображения метрик
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 20px;
}
</style>
""",
    unsafe_allow_html=True,
)

# стиль отображения даты и времени
st.markdown(
    """
    <style>
    .time {
        font-size: 40px !important;
        font-weight: 400 !important;
        color: #ec5953 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# стиль отображения вкладок графиков
st.markdown(
    """
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# стиль отображения вкладок графиков
st.markdown(
    """
<style>
   button[data-baseweb="tab"] {
   font-size: 30px;
   margin: 0;
   width: 100%;
   }
</style>
""",
    unsafe_allow_html=True,
)


# определяет основные праметры тренда
def trend_params(data, feature, current_price):
    # храним тренд
    trend = ""

    ind_min = data[feature].argmin()
    price_min = data[feature].min()
    ind_max = data[feature].argmax()
    price_max = data[feature].max()

    # храним дельту индексов макс и мин
    ind_delta = ind_max - ind_min if ind_min < ind_max else ind_min - ind_max

    # переменные хранящие цены откытия и закрытия позиции
    open_price = 0
    close_price_50 = 0
    close_price_75 = 0
    close_price = 0
    stop_loss = 0

    # если минимальный меньше макимального и больше либо равен 3, тренд растущий
    if ind_min < ind_max:
        if ind_delta >= 15:
            trend = "long"
            open_price = (
                current_price
                if current_price < price_min
                else price_min + (price_min * 1 / 100)
            )
            close_price_50 = price_max - ((price_max - price_min) * 50 / 100)
            close_price_75 = price_max - ((price_max - price_min) * 25 / 100)
            close_price = price_max - ((price_max - price_min) * 10 / 100)
            stop_loss = open_price - (open_price * 10 / 100)

        # если менее 3 то считаем тренда нет
        else:
            trend = "no trend"
    # при падающем тренде условия такие же
    else:
        if ind_delta >= 15:
            trend = "short"
            open_price = (
                current_price
                if current_price > price_max
                else price_max - (price_max * 1 / 100)
            )
            close_price_50 = price_min + ((price_max - price_min) * 50 / 100)
            close_price_75 = price_min + ((price_max - price_min) * 25 / 100)
            close_price = price_min + ((price_max - price_min) * 10 / 100)
            stop_loss = open_price + (open_price * 10 / 100)
        else:
            trend = "no trend"

    return {
        "trend": trend,
        "ind_delta": ind_delta,
        "ind_min": ind_min,
        "ind_max": ind_max,
        "open_price": open_price,
        "close_price_50": close_price_50,
        "close_price_75": close_price_75,
        "close_price": close_price,
        "stop_loss": stop_loss,
    }


def get_results(
    val_money,
    trend,
    ind_delta,
    ind_min,
    ind_max,
    open_price,
    close_price_50,
    close_price_75,
    close_price,
    stop_loss,
):
    # количество акций
    stocs = val_money // open_price

    # на какую сумму куплены акции
    stocs_sum_total = stocs * open_price

    # количество акций после take profit
    stocs_50 = stocs * 50 // 100
    stocs_75 = stocs * 25 // 100
    stocs_100 = stocs * 25 // 100

    # прибыль с части take_profit
    profit_50 = (stocs_50 * close_price_50) - (stocs_50 * open_price)

    profit_75 = ((stocs_75 * close_price_75) - (stocs_75 * open_price)) + profit_50

    full_profit = (
        ((stocs_100 * close_price) - (stocs_100 * open_price)) + profit_50 + profit_75
    )
    res_stop_loss = (stocs * stop_loss) - stocs_sum_total
    res_stop_loss_50 = (stocs_50 * stop_loss) - (stocs_50 * open_price) + profit_50
    res_stop_loss_75 = (
        (stocs_75 * stop_loss) - (stocs_75 * open_price) + profit_50 + profit_75
    )

    if trend == "short":
        full_profit *= -1
        res_stop_loss *= -1
        res_stop_loss_50 *= -1
        res_stop_loss_75 *= -1

    return {
        "full_profit": full_profit,
        "res_stop_loss": res_stop_loss,
        "res_stop_loss_50": res_stop_loss_50,
        "res_stop_loss_75": res_stop_loss_75,
    }


st.write(f"## Ваш баланс: {st.session_state.balance} ₽")


if len(st.session_state.briefcase) > 0:
    st.dataframe(st.session_state.briefcase)


st.divider()

(
    col1,
    col2,
    col3,
    col4,
    col5,
    col6,
    col7,
    col8,
    col9,
    col10,
    col11,
    col12,
    col13,
    col14,
    col15,
) = st.columns(15)
with col1:
    st.metric(**st.session_state.metric[0])
with col2:
    st.metric(**st.session_state.metric[1])
with col3:
    st.metric(**st.session_state.metric[2])
with col4:
    st.metric(**st.session_state.metric[3])
with col5:
    st.metric(**st.session_state.metric[4])
with col6:
    st.metric(**st.session_state.metric[5])
with col7:
    st.metric(**st.session_state.metric[6])
with col8:
    st.metric(**st.session_state.metric[7])
with col9:
    st.metric(**st.session_state.metric[8])
with col10:
    st.metric(**st.session_state.metric[9])
with col11:
    st.metric(**st.session_state.metric[10])
with col12:
    st.metric(**st.session_state.metric[11])
with col13:
    st.metric(**st.session_state.metric[12])
with col14:
    st.metric(**st.session_state.metric[13])
with col15:
    st.metric(**st.session_state.metric[14])

st.divider()

(
    tab1,
    tab2,
    tab3,
    tab4,
    tab5,
    tab6,
    tab7,
    tab8,
    tab9,
    tab10,
    tab11,
    tab12,
    tab13,
    tab14,
    tab15,
) = st.tabs(MOEXBC)

with tab1:
    fig = show_data_candles(st.session_state.df[0][MOEXBC[0]], MOEXBC[0])
    st.plotly_chart(fig, theme=None, use_container_width=True)

with tab2:
    fig = show_data_candles(st.session_state.df[1][MOEXBC[1]], MOEXBC[1])
    st.plotly_chart(fig, theme=None, use_container_width=True)

with tab3:
    fig = show_data_candles(st.session_state.df[2][MOEXBC[2]], MOEXBC[2])
    st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab4:
#     fig = show_data_candles(st.session_state.df[3][MOEXBC[3]], MOEXBC[3])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab5:
#     fig = show_data_candles(st.session_state.df[4][MOEXBC[4]], MOEXBC[4])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab6:
#     fig = show_data_candles(st.session_state.df[5][MOEXBC[5]], MOEXBC[5])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab7:
#     fig = show_data_candles(st.session_state.df[6][MOEXBC[6]], MOEXBC[6])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab8:
#     fig = show_data_candles(st.session_state.df[7][MOEXBC[7]], MOEXBC[7])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab9:
#     fig = show_data_candles(st.session_state.df[8][MOEXBC[8]], MOEXBC[8])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab10:
#     fig = show_data_candles(st.session_state.df[9][MOEXBC[9]], MOEXBC[9])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab11:
#     fig = show_data_candles(st.session_state.df[10][MOEXBC[10]], MOEXBC[10])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab12:
#     fig = show_data_candles(st.session_state.df[11][MOEXBC[11]], MOEXBC[11])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab13:
#     fig = show_data_candles(st.session_state.df[12][MOEXBC[12]], MOEXBC[12])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab14:
#     fig = show_data_candles(st.session_state.df[13][MOEXBC[13]], MOEXBC[13])
#     st.plotly_chart(fig, theme=None, use_container_width=True)

# with tab15:
#     fig = show_data_candles(st.session_state.df[14][MOEXBC[14]], MOEXBC[14])
#     st.plotly_chart(fig, theme=None, use_container_width=True)


list_params = {}
recommended_long = []
recommended_short = []
for i in range(len(MOEXBC)):
    nuw_df = st.session_state.df[i][MOEXBC[i]]
    param = trend_params(
        nuw_df[nuw_df["begin"] > "2023-09-01"],
        "close",
        nuw_df[nuw_df["begin"] > "2023-09-01"].iloc[0, 0],
    )
    if param["trend"] == "long":
        recommended_long.append(MOEXBC[i])
        list_params[MOEXBC[i]] = param
    elif param["trend"] == "short":
        recommended_short.append(MOEXBC[i])
        list_params[MOEXBC[i]] = param


st.divider()
col1, col2 = st.columns(2)
col1.write("### Рекомендовано к покупке - стратегия long")
col2.write("### Рекомендовано к продаже - стратегия short")

show_long_recommended = ""
for i in range(len(recommended_long)):
    show_long_recommended += (
        f"✔️ {recommended_long[i]}, {MOEXBC_DICT[recommended_long[i]]}<br>"
    )

if len(show_long_recommended) > 0:
    col1.write(show_long_recommended, unsafe_allow_html=True)
else:
    col2.write("рекомендаций нет")

show_short_recommended = ""
for i in range(len(recommended_short)):
    show_short_recommended += (
        f"✔️ {recommended_short[i]}, {MOEXBC_DICT[recommended_short[i]]} <br>"
    )


if len(show_short_recommended) > 0:
    col2.write(show_short_recommended, unsafe_allow_html=True)
else:
    col2.write("рекомендаций нет")

st.divider()
col1, col2, cok3 = st.columns(3)
with col2:
    my_form = st.form("my_form")
    ticker = my_form.selectbox(
        label="Выбрать акцию",
        index=None,
        placeholder="SBER",
        options=recommended_long + recommended_short,
        help="выбирете акцию",
    )
    number = my_form.number_input(
        label="Сумма покупки/продажи",
        min_value=5000.00,
        max_value=st.session_state.balance,
        step=5000.00,
        help="введите сумму покупки/продажи",
    )
    form_button = my_form.form_submit_button("Рассчитать", on_click=click_button)


st.divider()
if st.session_state.clicked:
    params = list_params[ticker]
    res = get_results(number, **params)
    st.write(f"### Прогнозный расчёт на {number} ₽")

    st.write(
        f"""
                
        📌 Код инструмента: {ticker}, {MOEXBC_DICT[ticker]}
            
        ✔️ Текущая цена покупки:  {str(params["open_price"].round(2)) + " ₽"}

        ✔️ Количество акций: {int(number // params["open_price"].round(2))}

        ✔️ Определенный тренд:  {params["trend"]}

        ✔️ Цена закрытия в районе максимума:  {str(params["close_price"].round(2)) + " ₽"}

        ✔️ Расчёт прибыли при срабатывании стратегии:  {str(res["full_profit"].round(2)) + " ₽"}

        ✔️ Расчёт результата при срабатывании до 50%
                и потом закрытии по стоп лоссу:  {str(res["res_stop_loss_50"].round(2)) + " ₽"}

        ✔️ Расчёт результата при срабатывании до 70%
                и потом закрытии по стоп лоссу:  {str(res["res_stop_loss_75"].round(2)) + " ₽"}

        ✔️ Расчет результата при стоп лоссе
                без фиксировании любой части прибыли:  {str(res['res_stop_loss'].round(2)) + " ₽"}"""
    )
    st.divider()

    total = (
        number // params["open_price"].round(2) * params["open_price"].round(2)
    ).round(2)


def change_name(total, ticker, price, quantity):
    balance = get_user_balance()
    sess.put(host + "balance.update", data={"balance": balance - total})
    st.session_state["balance"] = get_user_balance()
    r = sess.post(
        host + "briefcase.add",
        data={
            "tisker": ticker,
            "price": price,
            "quantity": quantity,
            "amount": total,
        },
    )
    st.session_state.briefcase = get_user_briefcase()


if st.session_state.clicked:
    price = params["open_price"].round(2)
    quantity = int(number // params["open_price"].round(2))
    send_button = st.button(
        "Отправить заявку", on_click=change_name, args=[total, ticker, price, quantity]
    )

    if send_button:
        if params["trend"] == "long":
            st.json(
                {
                    "date": "2023-09-01",
                    "ticker": ticker,
                    "application": {
                        "step1": {
                            "action": "buy",
                            "open_price": price,
                            "quantity_open_price": quantity,
                        },
                        "step2": {
                            "action": "sale",
                            "lose_price_50": params["close_price_50"].round(2),
                            "quantity_close_price_50": quantity // 2
                            if quantity % 2 == 0
                            else quantity // 2 + 1,
                        },
                        "step3": {
                            "action": "sale",
                            "close_price_75": params["close_price_75"].round(2),
                            "quantity_close_price_75": quantity // 4
                            if quantity % 2 == 0
                            else quantity // 4 + 1,
                        },
                        "step4": {
                            "action": "sale",
                            "close_price": params["close_price"].round(2),
                            "quantity_close_price": quantity % 4
                            if quantity % 2 == 0
                            else quantity % 4 + 1,
                        },
                        "step5": {
                            "action": "sale",
                            "stop_loss": params["stop_loss"].round(2),
                            "quantity_stop_loss": quantity,
                        },
                    },
                }
            )
        elif params["trend"] == "short":
            st.json(
                {
                    "date": "2023-09-01",
                    "ticker": ticker,
                    "application": {
                        "step1": {
                            "action": "sale",
                            "open_price": price,
                            "quantity_open_price": quantity,
                        },
                        "step2": {
                            "action": "buy",
                            "lose_price_50": params["close_price_50"].round(2),
                            "quantity_close_price_50": quantity // 2
                            if quantity % 2 == 0
                            else quantity // 2 + 1,
                        },
                        "step3": {
                            "action": "buy",
                            "close_price_75": params["close_price_75"].round(2),
                            "quantity_close_price_75": quantity // 4
                            if quantity % 2 == 0
                            else quantity // 4 + 1,
                        },
                        "step4": {
                            "action": "buy",
                            "close_price": params["close_price"].round(2),
                            "quantity_close_price": quantity % 4
                            if quantity % 2 == 0
                            else quantity % 4 + 1,
                        },
                        "step5": {
                            "action": "buy",
                            "stop_loss": params["stop_loss"].round(2),
                            "quantity_stop_loss": quantity,
                        },
                    },
                }
            )
