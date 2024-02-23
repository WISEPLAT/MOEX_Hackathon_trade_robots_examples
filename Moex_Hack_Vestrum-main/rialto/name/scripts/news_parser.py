import requests
import json
import pprint


class Newsletter:
    import requests
    def __init__(self, url='https://newsapi.org/v2/top-headlines?'
                                'country=ru&'
                            'apiKey=1f10d9fcb90542dd9757640309a1c71e'):
        self.url = url


    def top_10_news(self) -> dict:
        final_dict = {}
        try:

            response = requests.get(self.url)
            for i in range(10):
                final_dict[i] = response.json()['articles'][i]

        except Exception:
            print('Ошибка получения информации от сервера')
        finally:
            return final_dict


news = Newsletter()

pprint.pprint(news.top_10_news())
