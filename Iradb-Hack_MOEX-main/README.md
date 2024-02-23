<h1 style="text-align:center">OneHotDay</h1>




```
Приложение, являющееся рекомендательной системой для однодневных торгов по акциям MOEX на основе прогностической модели CatBoost   по данным AlgoPack (https://www.moex.com/ru/algopack)
```

**Скачиваем проект с гитхаба**
```
Переходим в папку с проектом
```
`
Если на Windows вводим в консоль py -m venv lenv 
`

`
Если на Linux вводим в консоль python3 -m venv lenv
`

`
После вводим на Windows lenv\Scripts\activate
`
После вводим на Linux source lenv/bin/activate

```
Устанавливаем библиотеки и зависимости

Вводим в консоль
pip install -r requirements.txt
```
`
После успешного завершения установки вводим
py app.py (Windows) или python3 app.py (Если на linux)
`

```
Дожидаемся строки
Dash is running on http://localhost:8050/
и переходим по ссылке http://localhost:8050/
```