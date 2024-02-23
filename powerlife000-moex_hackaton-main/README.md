# Исходные коды микросервисов пайплайна создания торговых и инвестиционных стратегий на базе нейронных сетей

Перечень скриптов микросервисов:   
- data_markup.py		Оценка потенциальной доходности торговли и инвестиций (тестирование гипотез разметки данных).
- data_gen.py			Генерация датасетов
- edu_neural.py			Обучение нейронных сетей
- calc_profit.py		Оценка доходности нейронных сетей (бек тесты)
- calc_signals.py		Генерация торговых и инвестиционных сигналов

Для редактирования файлов скриптов микросервисов доступны их ноутбуки в коревой папке.

#Описание параметров и работы микросервисов
- Описание параметров микросервисов доступно по ссылке: [ссылка](./info/О сервисе 2.docx)
- Также описание параметров доступно по тексту скриптов
- Гайдбук по работе микросервисов и созданию стратегий доступен по ссылке: [ссылка](./how-to-guide.docx)
- Презентация работы миросервисов доступна по ссылке: [ссылка](./info/NullPointerExeption v1.pptx)

# Запуск скриптов
Расчёт доходности нейронных сетей
python calc_profit.py \ 
	--cmd_config \
	--task_id 123
	--scaler_path app/scalers/1D \
	--neural_path app/neurals/1D \
	--ticker SBER \
	--timeframe 1D \
	--start_date 2007-01-01 \
	--end_date 2023-11-26 \
	--count_points 6 \
	--extr_bar_count 10 \
	--max_unmark 0.33 \
	--respos_url "127.0.0.1:8080"

Расчёт сигналов
python calc_signals.py  \
	--cmd_config \
	--task_id 123 \
	--ticker ["SBER", "ABIO"] \
	--scaler_path app/scalers/1D \
	--neural_path app/neurals/1D \
	--timeframe 1D \
	--count_points 6 \
	--extr_bar_count 10 \
	--max_unmark 0.33 \
	--count_days 360 \
	--respos_url "127.0.0.1:8080"

Генерация датасетов
python data_gen.py \
	--cmd_config \
	--task_id 123 \
	--timeframe 1D \
	--start_date 2007-01-01 \
	--end_date 2023-11-26 \
	--count_points 6 \
	--extr_bar_count 10 \
	--size_df 2 \
	--max_unmark 0.33 \
	--data_path app/data/1D \
	--respos_url "127.0.0.1:8080"

Разметка данных
python data_markup.py \
	--cmd_config \
	--task_id 123 \
	--ticker SBER \
	--timeframe 1D \
	--start_date 2007-01-01 \
	--end_date 2023-11-26 \
	--count_points 6 \
	--extr_bar_count 10 \
	--respos_url "127.0.0.1:8080"

Обучение нейронных сетей
python edu_neural.py \
	--cmd_config \
	--task_id 123 \
	--data_path app/data/1D \
	--scaler_path app/scalers/1D \
	--neural_path app/neurals/1D \
	--new_model_flag True \
	--learning_rate 0.00001 \
	--epochs 10 \
	--steps_per_epoch 128 \
	--validation_steps 128 \
	--respos_url "127.0.0.1:8080"