import os
from datetime import datetime, timedelta
import pandas as pd

from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import streamlit as st
from moexalgo import Market, Ticker
from bokeh.models import Plot, GridPlot
from bokeh.plotting import figure
from bokeh.embed import file_html

from strategies import *

TOKEN = st.secrets["TOKEN"]


# # Page title
st.set_page_config(page_title='🛋️👨‍💻 GPT для анализа данных Московской биржи')
st.title('🛋️👨‍💻 GPT для анализа данных Московской биржи')

st.text("""MVP решения от команды "Диванные эксперты" хакатона Go Algo от Московской биржи""")


def generate_date_range(start_date, end_date):
    """Generate a list of dates within the specified range."""
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    return date_range


@st.cache_data
def load_market_data(option, start_date, end_date):
    """
    Load market data based on the specified option and date range.
    """
    stocks = Market('stocks')
    dates = generate_date_range(start_date, end_date)

    result_df = pd.DataFrame()

    if option == 'tradestats':
       for date in dates:
           response = stocks.tradestats(date=date)
           df = pd.DataFrame(response)
           result_df = pd.concat([result_df, df], ignore_index=True)
 
       with st.expander('Предпросмотр полученных данных по сделкам:'):
         st.write(result_df.head(10))
       
       return result_df

    if option == 'orderstats':   
       for date in dates:
           response = stocks.orderstats(date=date)
           df = pd.DataFrame(response)
           result_df = pd.concat([result_df, df], ignore_index=True)
 
       with st.expander('Предпросмотр полученных данных по заявкам:'):
         st.write(result_df.head(10))
       
       return result_df
    
    if option == 'obstats':
       for date in dates:
           response = stocks.obstats(date=date)
           df = pd.DataFrame(response)
           result_df = pd.concat([result_df, df], ignore_index=True)
       
       with st.expander('Предпросмотр полученных данных по стаканам заявок:'):
         st.write(result_df.head(10))
   
       return result_df
    

@st.cache_data
def load_ticker_data(selected_ticker, start_date_ticker, end_date_ticker, frequency):
    """
    Load ticker data based on the specified ticker, date range, and frequency.
    """
    ticker = Ticker(selected_ticker)
    response = ticker.candles(date=start_date_ticker, till_date=end_date_ticker, period=frequency) 
    result_df = pd.DataFrame(response)
    result_df = result_df[['open', 'close', 'high', 'low', 'volume']]
    result_df.rename(columns={'open': 'Open', 
                              'close': 'Close', 
                              'high': 'High', 
                              'low': 'Low',
                              'volume': 'Volume'}, inplace=True)
    with st.expander('Предпросмотр полученных данных по тикеру:'):
         st.write(result_df.head(10))

    return result_df


# Generate LLM response
def generate_response(df, input_query):
  """
  Generate a response using the specified dataframe and input query.
  """
  llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.2, openai_api_key=TOKEN)
  agent = create_pandas_dataframe_agent(llm, df, verbose=True, 
                                        agent_type=AgentType.OPENAI_FUNCTIONS, handle_parsing_errors=True)
  response = agent.run(input_query)
  return st.success(response, icon="✅")


# Streamlit app
def main(): 
    """
    Main function to run the Streamlit app.
    """
    # Options menu with business mapping

    st.subheader('Проведите разведочный анализ данных биржи', divider='rainbow')

    options_mapping = {
        "Сделки": "tradestats",
        "Заявки": "orderstats",
        "Стакан заявок": "obstats",
    }

    # Date selection - Start Date
    start_date = st.date_input("Выберите начало периода:", datetime.today(), key="start_date")

    # Date selection - End Date
    end_date = st.date_input("Выберите конец периода:", datetime.today(), key="end_date")

    # Options selection
    selected_option = st.radio("Выберите нужные данные для анализа:", options=list(options_mapping.keys()), index=None)

    question_list = [
      'Какая акция самая дорогая?',
      'По какой акции было больше всего сделок?',
      'Какая была средняя разница между ценой начала и ценой окончания торгов?',
      'Другое',
    ]
    query_text = st.selectbox('Выберите пример вопроса:', question_list, disabled=not selected_option)

    if query_text == 'Другое':
      query_text = st.text_input('Введите ваш запрос:', disabled=not selected_option)
    if selected_option is not None:
      st.header('Результаты:')
      try:
        result = load_market_data(options_mapping[selected_option], start_date, end_date)
        generate_response(result, query_text)
      except Exception as e:
        st.error(f"""
                 Проблемы с обработкой {selected_option}.
                 Что-то сервисом (а точнее {str(e)}) 😲
                 Повторите попытку позднее ❤️
                 """)
        
    
    st.subheader('Постройте торговую стратегию по интересующей акции', divider='rainbow')

    yesterday = (datetime.now() - timedelta(days=2)).date()
    result = load_market_data('tradestats', yesterday, yesterday)

    # Group by 'Ticker' and calculate the sum of 'Number_of_Trades' for each ticker
    total_trades_per_ticker = result.groupby('secid')['trades_b'].sum()
    # Sort the tickers based on the total number of trades in descending order
    sorted_tickers = total_trades_per_ticker.sort_values(ascending=False).index.tolist()
        
    # Use an expander to create a collapsible section
    with st.expander("Выбор тикера акции:"):
        # Display options in a dropdown inside the expander
        st.caption('В списке представлены акции, торговавшиеся на бирже вчера, отсортированные по количеству торгов')
        selected_ticker = st.selectbox('Выберите тикер акции:', sorted_tickers)

    # Date selection - Start Date
    start_date_ticker = st.date_input("Выберите начало периода по выбранному тикеру:", datetime.today(), key="start_date_ticker")

    # Date selection - End Date
    end_date_ticker = st.date_input("Выберите конец периода по выбранному тикеру:", datetime.today(), key="end_date_ticker")

    frequency_mapping = {
        "Минута": '1m',
        "10 минут": '10m',
        "Час": '1h',
        "День": 'D',
        "Неделя": 'W',
        "Месяц": 'M',
        "Квартал": 'Q',
    }

    frequency = st.radio("Выберите нужную частоту сбора данных по свечам:", options=list(frequency_mapping.keys()), index=None)

    strategies = ["SMA Cross", "Mean Reversion"]

    selected_strategy = st.radio("Выберите стратегию для запуска:", options=strategies, index=None)

    st.write("""Изучите дополнительную информацию о стратегиях [SMA Cross](https://docs.gunthy.org/docs/built-in-strategies/futures-strategies/builder/smacross/) 
             и [MeanReversion](https://www.cmcmarkets.com/en/trading-guides/mean-reversion) 
             """)

    if selected_ticker is not None and frequency is not None \
        and start_date_ticker is not None and end_date_ticker is not None:
      ticker_df = load_ticker_data(selected_ticker, start_date_ticker, end_date_ticker, frequency_mapping[frequency])

    if selected_strategy == "SMA Cross":
       st.write(pd.DataFrame(run_sma_cross_strategy_stats(ticker_df)))
       st.write(run_sma_cross_strategy_plot(ticker_df))
       # html_content = file_html(run_sma_cross_strategy_plot(ticker_df), CDN, "Result")
       # st.components.v1.html(html_content, width=800, height=400)

    if selected_strategy == "Mean Reversion":
       st.write(pd.DataFrame(run_mean_reversion_stats(ticker_df)))
       st.write(run_mean_reversion_plot(ticker_df))
       # html_content = file_html(run_mean_reversion_plot(ticker_df), CDN, "Result")
       # st.components.v1.html(html_content, width=800, height=400)


if __name__ == "__main__":
    main()
