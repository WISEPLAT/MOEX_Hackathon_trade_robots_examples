#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_usd_rub(mt5):
    #Получаем данные о долларе
    try:
        # ticker USDRUB
        usd_ticker = "USDRUB"
        mt5.market_book_add(usd_ticker)

        symbol_info=mt5.symbol_info(usd_ticker)
        if symbol_info!=None:
            symbol_info_dict = mt5.symbol_info(usd_ticker)._asdict()

        usd_rub = symbol_info_dict['bid']

        if usd_rub == 0.0:
            #Пытаемся получить данные с Яху
            import requests
            url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/USDRUB=X?modules=summaryDetail'
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            response = requests.get(url, headers=headers)

            if response.status_code==200:
                import json
                response_json = json.loads(response.text)
                usd_rub = response_json['quoteSummary']['result'][0]['summaryDetail']['ask']['raw']
            else:
                quit()

        #print("usd_rub: ", usd_rub)
        
        return usd_rub
    except:
        print("Error get price of currency pair usd_rub")
#         if is_notebook() != True:
#             quit()
        
        return None    

