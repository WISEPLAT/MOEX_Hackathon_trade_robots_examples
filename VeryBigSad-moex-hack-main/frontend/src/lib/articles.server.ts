export type ArticleInfo = { id: string; title: string; description: string; source: { name: string, href: string } };
export type Article = ArticleInfo & { content: ArticleEntry[] };
export type ArticleEntry =
    | { kind: "header"; content: string }
    | { kind: "paragraph"; content: string }
    | { kind: "image"; src: string }
    | { kind: "code"; content: string };

export const Articles = [
    {
        id: "guide",
        title: "Входим в алготрейдинг",
        description: "Наш гайд о том, как сделать первые шаги в алготрейдинге!",
        source: { name: "Мы!", href: "https://khromdev.ru/" },
        content: [
            { kind: "header", content: "Шаг 1: Создание Стратегии"},
            { kind: "paragraph", content: "1. Создайте новый файл стратегии: Создайте Python файл (например, `my_strategy.py`)." },
            { kind: "paragraph", content: "2. Наследуйтесь от класса IStrategy: Это базовый класс для создания стратегий в Freqtrade." },
            { kind: "code", content: `from freqtrade.strategy.interface import IStrategy\nclass MyStrategy(IStrategy):\n  pass` },
            { kind: "header", content: "Шаг 2: Определение Параметров"},
            { kind: "paragraph", content: "1. Установите минимальные параметры: Определите необходимые параметры, такие как minimal_roi, stoploss, и trailing_stop." },
            { kind: "paragraph", content: "2. Определите индикаторы: Используйте библиотеки, такие как TA-Lib, для создания технических индикаторов." },
            { kind: "code", content: `def populate_indicators(self, dataframe: DataFrame) -> DataFrame:\n  # пример: SMA (простая скользящая средняя)\n  dataframe['sma'] = ta.SMA(dataframe, timeperiod=20)\n  return dataframe` },
            { kind: "header", content: "Шаг 3: Торговые Сигналы"},
            { kind: "paragraph", content: "1. Определите условия для входа: Укажите, когда ваша стратегия должна входить в позицию." },
            { kind: "code", content: "def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:\n  # Пример условия на покупку\n  dataframe.loc[((dataframe['sma'] > dataframe['close'])), 'buy'] = 1\n  return dataframe" },
            { kind: "paragraph", content: "2. Определите условия для выхода: Аналогично укажите, когда стратегия должна выходить из позиции." },
            { kind: "header", content: "Шаг 4: Оптимизация и Тонкая Настройка"},
            { kind: "paragraph", content: "1. Оптимизируйте параметры: Используйте гипероптимизацию для настройки параметров стратегии." },
            { kind: "paragraph", content: "2. Повторяйте тестирование и настройку: Повторяйте тесты и настройки, пока не достигнете удовлетворительных результатов." },
            { kind: "header", content: "Шаг 5: Запуск на Реальном Рынке"},
            { kind: "paragraph", content: "Запустите стратегию в реальных торговых условиях: Используйте команду freqtrade trade --strategy MyStrategy для запуска стратегии в реальных условиях рынка." }
        ],
    },
    {
        id: "51",
        title: "Python для алготрейдинга",
        description:
            "В этом посте я собрал все известные мне полезные штуки, которые могут пригодится в алготрейдинге. Чем-то я пользуюсь сам, что-то пробовал и не мне понравилось, а чем-то не пользовался вовсе, но это не значит что это не может быть вам полезным. Не все относиться к алготрейдингу напрямую, но может быть полезным в какой-то степени.",
        source: { name: "day0markets.ru", href: "https://day0markets.ru/python-algotrading/" },
        content: [
            { kind: "header", content: "Общие инструменты для удобства разработки" },
            {
                kind: "paragraph",
                content:
                    "black - code formatter. Делает код единообразным, что очень удобно при просмотре git diff - сильно снижает когнитивную нагрузку."
            },
            {
                kind: "paragraph",
                content:
                    "isort - сортировка кода. Я использую только для сортировки импортов, плюсы такие же как и от black."
            },
            {
                kind: "paragraph",
                content:
                    "pre-commit - удобная конфигурация precommit hook’ов. Я обычно в хуки добавляю black & isort. Это спасло меня от многих багов + репозиторий всегда в чистоте"
            },
            {
                kind: "paragraph",
                content:
                    "coockiecutter - позволяет создать шаблон для проекта и переиспользовать. Очень удобно, если под каждого бота создается свой проект. Раньше я им часто пользовался. Туда же можно запихнуть конфиг для pre-commit, что очень удобно."
            },

            { kind: "header", content: "Библиотеки" },
            {
                kind: "paragraph",
                content: "numpy - не могу не упомянуть, must have в любом проекте"
            },
            {
                kind: "paragraph",
                content:
                    "pandas - аналогично. Этакий excel на стероидах. Must have почти в любом проекте. Если только начинаете знакомство с python, то советую изучить это библиотеку в первую очередь."
            },
            {
                kind: "paragraph",
                content: "matplotib - визуализация, эквити строить и прочие красивые штуки"
            },
            {
                kind: "paragraph",
                content: "seaborn - matplotlib на стероидах, чуть красивее и удобнее"
            },
            {
                kind: "paragraph",
                content: "plotly - красивая визуализация"
            },
            {
                kind: "paragraph",
                content:
                    "bokeh - интерактивная визуализация. Можно фильтровать данные и график будет обновляться - модно и молодежно, почти как в JS"
            },
            {
                kind: "paragraph",
                content:
                    "asyncio - асинхронность, вебсокеты и все такое. Используется почти в любом live проекте"
            },
            {
                kind: "paragraph",
                content:
                    "gevent - удобные корутины (greenlet’ы). Библиотека сильно упрощает жизнь, если надо работать с несколькими тредами. Не очень хорошо дружит с asyncio, поэтому вместе использовать иногда сложно, но вполне возможно. Я использую в каждом втором проекте."
            },
            {
                kind: "paragraph",
                content:
                    "msgpack - как json, только гораздо быстрее. Есть реализации почти под все языки. Я использую очень часто для коммуникации между сервисами."
            },
            {
                kind: "paragraph",
                content:
                    "zmq (zeromq) - networking library. Похожа на очередь сообщений, но ей не является. Для передачи сообщений между процессами/компонентами пока ничего быстрее не встречал. Использую очень часто. Есть реализации почти под любой язык"
            },
            {
                kind: "paragraph",
                content:
                    "quantlib - C++ библиотека с кучей функционала - pricing, stochastic processes, volatility estimation и все в этом духе."
            },
            {
                kind: "paragraph",
                content: "TA-lib - библиотека для технического анализа, индикаторы и все такое."
            },
            {
                kind: "paragraph",
                content: "scikit-learn - классические алгоритмы ML и подготовки данных."
            },
            {
                kind: "paragraph",
                content:
                    "CCXT - интеграция почти со всеми более менее ликвидными криптобиржами. Must have, если приходится торговать криптой"
            },
            {
                kind: "paragraph",
                content:
                    "pyside и pyqt5 - если нужны красивые и современные интерфейсы для десктопа (биндинги для QT)"
            },
            { kind: "header", content: "Бектестеры" },
            {
                kind: "paragraph",
                content:
                    "Их написано невероятное количество. Но, увы, готовых для live торговли решений мало. Зачастую каждый бектестер позволяет реализовывать какие-то определенные типы стратегий. В целом, для старта можно найти нечто подходящее и допиливать под свои нужды, благо почти все open-source."
            }
        ]
    },
    {
        id: "1111",
        title: "Торговые роботы на Python",
        description:
            "Привет! На связи команда Тинькофф Инвестиций. В этой статье рассказываем про Tinkoff Invest API, объясняем, как написать робота на Python, и разбираем плюсы этого языка в сравнении с другими. А вместо заключения ловите гайд по созданию робота на примере работы победителя нашего конкурса Tinkoff Invest Robot Contest.",
        source: { name: "habr.ru", href: "https://habr.com/ru/companies/tinkoff/articles/709166/" },
        content: []
    },
    {
        id: "4124",
        title: "100 строк Python-кода: Автоматизируем биржевую торговлю",
        description: "Алгоритмическая торговля еще никогда не была такой доступной, как в настоящее время. Совсем недавно этот вид деятельности был по плечу лишь институциональным инвесторам с миллионными бюджетами, однако сегодня фактически любой желающий при наличии ноутбука и подключения к Интернет может заняться алгоритмической торговлей.",
        source: { name: "datareview.info", href: "https://datareview.info/article/100-strok-python-koda-avtomatiziruem-birzhevuyu-torgovlyu/" },
        content: []
    },
    {
        id: "120",
        title: "О практической пользе transformer для торговли на бирже",
        description:
            "В этой статье рассмотрим, как Transformer может улучшить торговлю на бирже. Разберем, как эта технология улучшает анализ данных и помогает принимать более точные решения, оптимизируя стратегии трейдинга.",
        source: { name: "habr.com", href: "https://habr.com/ru/articles/651607/" },
        content: []
    }
] satisfies Article[];

export function articles(): ArticleInfo[] {
    return Articles.map(o => {
        let { content, ...o2 } = o;
        return o2;
    });
}

export function article(id: string): Article | undefined {
    return Articles.find(o => o.id == id);
}

export function headers(id: string): { index: number; content: string }[] | undefined {
    let res = [];
    let article = Articles.find(o => o.id == id);
    if (!article) return undefined;
    for (let index = 0; index < article.content.length; index++) {
        const elem = article.content[index];
        if (elem.kind != "header") continue;
        res.push({ index, content: elem.content });
    }
    return res;
}
