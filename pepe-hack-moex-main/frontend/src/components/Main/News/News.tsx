import React, {FC} from 'react';
import {Col, Flex, Row, Space, Typography} from 'antd';
import NewsItem from "./NewsItem";


const News: FC = () => {
    return (
        <Space direction={"vertical"}>
            <Typography.Title level={2}>Лента</Typography.Title>
            <Row gutter={[16, 24]}>
                <Col span={4}>
                    <NewsItem title={'В БКС назвали топ-5 акций'}
                              description={'Декабрьская просадка ценных бумаг открывает возможность для инвесторов приобрести подешевевшие акции на перспективу\n' +
                              '\n'}
                              imgSrc={'https://s0.rbk.ru/v6_top_pics/resized/590xH/media/img/5/36/347023941698365.jpeg'}/>
                </Col>
                <Col span={4}>
                    <NewsItem title={'ЦБ установил курсы доллара, евро и юаня'}
                              description={'Центральный банк России установил официальный курс доллара США на 13 декабря в размере ₽90,2158, евро — ₽97,4030, юаня — ₽12,5636.'}
                              imgSrc={'https://s0.rbk.ru/v6_top_pics/resized/810x405_crop/media/img/0/26/347007432369260.jpeg'}/>
                </Col>
                <Col span={4}>
                    <NewsItem title={'«Мосгорломбард» продлил срок приема заявок на участие в IPO'}
                              description={'Головная компания группы «Мосгорломбард» разместит на Мосбирже до 322,58 млн акций, полученных в результате допэмиссии. Ожидается, что торги акциями компании начнутся 22 декабря 2023 года под тикером MGKL'}
                              imgSrc={'https://s0.rbk.ru/v6_top_pics/resized/810x405_crop/media/img/7/93/347023073203937.jpeg'}/>
                </Col>
                <Col span={4}>
                    <NewsItem title={'Газпромбанк поднял ставки по краткосрочным вкладам до 16% годовых'}
                              imgSrc={'https://s0.rbk.ru/v6_top_pics/resized/810x405_crop/media/img/7/38/347023708310387.jpeg'}
                              description={'15 декабря совет директоров ЦБ примет последнее в этом году решение о размере ключевой ставки. На фоне роста инфляции и ожидания очередного раунда ужесточения политики регулятора банки увеличивают доходность по вкладам'}/>
                </Col>
                <Col span={4}>
                    <NewsItem title={'«Удачный контекст»: чем интересно инвесторам IPO Совкомбанка'}
                              imgSrc={'https://s0.rbk.ru/v6_top_pics/resized/810x405_crop/media/img/6/98/347023692644986.jpeg'}
                              description={'Размещение акций Совкомбанка на Мосбирже состоится уже в ближайшее время. Это IPO станет первым в банковском секторе РФ с 2015 года. Чем еще привлекает внимание IPO банка, «РБК Инвестиции» разбирались вместе с экспертами'}/>
                </Col>
                <Col span={4}>
                    <NewsItem title={'Акции Сбербанка подешевели до минимума за два месяца'}
                              imgSrc={'https://s0.rbk.ru/v6_top_pics/resized/810x405_crop/media/img/0/90/347022944676900.jpeg'}
                              description={'Утром банк представил отчетность по РСБУ за ноябрь и 11 месяцев 2023 года. В ноябре чистая прибыль снизилась на 7,4% год к году и составила ₽115,4 млрд'}/>
                </Col>
            </Row>
        </Space>
    );
};

export default News;
