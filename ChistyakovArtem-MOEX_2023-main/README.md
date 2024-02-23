# MOEX_2023

Мой фреймворк для разработки альф на Московской Бирже.
Альфа состоит из класса с конструктором и формулой, а также параметров (нейтрализация). После создания - ее можно протестировать и увидеть результаты, метрики и также фидбек по ним.

Альфы могут быть вам полезны, если вы
1) Хотите торговать как Трейдер (руками). Вместо этого вы можете реализовать свою логику исполнения сделок в python в качестве альфы. Например if close / open - 1 > 0.1: return 1; else: return 0.
2) Если хотите торговать как Квант (при помощи математического нахождения информации в данных).

Для трейдера плюсы альф такие:
1) Минимальный риск потери денег за счет бектеста (если альфа хорошо показывает себя на бектесте, она должна себя хорошо показывать и в реальных условиях)
2) Автоматическое исполнение (не придется каждый раз совершать сделку руками).
3) Возможность разместить несколько альф одновременно (руками по нескольким стратегиям торговать одновременно будет куда сложнее)
4) Возможность использовать количество потоков данных сильно превосходящее вместимость человеческого мозга.

Для кванта
1) Возможно строить альфы при помощи анализа зависимости между какой-то формулой из прошлого и будущим return.
2) Нет необходимости в сложном кодинге и инфре.
3) В отличие от подобных соревнований - можно зарабатывать деньги.