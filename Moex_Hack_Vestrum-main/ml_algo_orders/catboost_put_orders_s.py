import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

# Загрузка данных
file_path = '/home/honeypussy/Moex_Hack_Vestrum/sampled_data_order_test.csv' 
data = pd.read_csv(file_path)

# Предобработка данных
data['ts'] = pd.to_datetime(data['ts'])
data.set_index('ts', inplace=True)

# Инженерия признаков
# 1. Лаговые Признаки
data['lag_1'] = data['put_orders_s'].shift(1)

# 2. Скользящие Средние
data['rolling_mean_3'] = data['put_orders_b'].rolling(window=3).mean()

# 3. Разности
data['diff_1'] = data['put_orders_b'].diff(1)

# 4. Процентное Изменение
data['pct_change'] = data['put_orders_b'].pct_change()

# 5. Оконные Статистики
data['rolling_std_3'] = data['put_orders_b'].rolling(window=3).std()

# 6. Категориальные Признаки из Временных Меток
data['day_of_week'] = data.index.dayofweek
data['hour_of_day'] = data.index.hour
data.drop(columns=['Unnamed: 0'], inplace=True)
# Замена бесконечных значений на NaN
data.replace([np.inf, -np.inf], np.nan, inplace=True)


# Очистка данных от NaN, которые могут появиться после генерации лагов
data.dropna(inplace=True)

# Выбор признаков и целевой переменной
X = data.drop(['put_orders_s', 'secid'], axis=1)
y = data['put_orders_s']

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Стандартизация данных
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Обучение модели CatBoost
model = CatBoostRegressor(iterations=10000, learning_rate=0.1, depth=10, verbose=False)
model.fit(X_train_scaled, y_train, eval_set=(X_test_scaled, y_test), use_best_model=True)

# Сохранение модели
model.save_model('final_catboost_model_put_orders_s.cbm')

# Вычисление метрик
predictions = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# Вывод метрик
print(f'MSE: {mse}')
print(f'MAE: {mae}')
print(f'R2: {r2}')

# Сохранение метрик в файл
metrics = {'MSE': mse, 'MAE': mae, 'R2': r2}
metrics_df = pd.DataFrame([metrics])
metrics_df.to_csv('catboost_model_metrics.csv', index=False)
