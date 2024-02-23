from joblib import load
import moexalgo

try:
    tradestats_model = load('elasticCV_model.joblib')
except Exception:
    print('файл модели не найден')


'''
Функция для работы с моделью
На вход принимает саму модель и данные мониторинга акции 
На выходе получаем прогноз переменной pr_close
'''
def predict_pr_close(tradestats_model, X_pred):
    try:
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        X_pred = scaler.fit_transform(X_pred)

    except Exception:
        print('Ошибка при масштабировании признаков')

    return tradestats_model.predict(X_pred)


