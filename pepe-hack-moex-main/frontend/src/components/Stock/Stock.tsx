import React, {FC, useEffect, useState} from 'react';
import {Avatar, Button, Card, Col, Flex, Row, Space, Typography} from 'antd';
import Search from "antd/es/input/Search";
import Chart from "./Chart";
import {mainApi} from "../../api/Api";
import {useParams} from "react-router-dom";

const Stock: FC = () => {
    const [dataCard, setDataCard] = useState<any>(null);
    const id = useParams().id;
    useEffect(() => {
        if (!id)
            return;
        mainApi.getStock(id as any).then((data) => {
            setDataCard(data || {} as any[]);
        });
    }, [id])

    function onChangeSearch(e: typeof Search.arguments.onChange) {
        setDataCard(e.target.value);
    }

    if (!dataCard)
        return <></>;
    const forecastHour = Math.ceil(dataCard.forecast.hour.price * dataCard.forecast.hour.changePercentage) / 100;
    const forecastDay = Math.ceil(dataCard.forecast.hour.price * dataCard.forecast.day.changePercentage) / 100;
    const forecastWeek = Math.ceil(dataCard.forecast.hour.price * dataCard.forecast.week.changePercentage) / 100;
    return (
        <Space size={'large'} direction={"vertical"} style={{width: '100%'}}>
            <Card bordered={true} size={"small"}
                  style={{boxShadow: '0px 4px 4px 0px rgba(0, 0, 0, 0.25)', padding: '36px 62px', marginBottom: 10}}
                  bodyStyle={{padding: 0}}
            >
                <Row>
                    <Col span={11}>
                        <Card bordered={true} size={"small"}
                              style={{
                                  background: dataCard.background,
                                  width: '100%',
                                  marginBottom: 30,
                                  padding: '24px 28px'
                              }}
                              bodyStyle={{padding: 0}}
                        >
                            <Flex gap={28}>
                                <Avatar
                                    style={{
                                        alignSelf: 'center',
                                        flex: '0 0 auto',
                                        boxShadow: '0px 4px 4px 0px rgba(0, 0, 0, 0.25)'
                                    }}
                                    size={{xs: 24, sm: 32, md: 40, lg: 64, xl: 80, xxl: 94}}
                                    src={dataCard.companyIcon}
                                />
                                <Flex style={{
                                    color: dataCard.textColor || 'white',
                                    minWidth: 0,
                                    width: '100%',
                                    flex: '1 1 auto'
                                }} vertical>
                                    <p style={{
                                        fontSize: '32px',
                                        fontWeight: '600',
                                        whiteSpace: 'nowrap',
                                        textOverflow: 'ellipsis',
                                        overflow: 'hidden'
                                    }}>{dataCard.companyName}</p>
                                    <p style={{fontSize: '16px', fontWeight: '500'}}>Сектор</p>
                                    <p style={{fontSize: '18px'}}>
                                        Финансовый
                                    </p>
                                </Flex>
                            </Flex>
                        </Card>

                        <Chart/>

                    </Col>
                    <Col offset={2} span={12} style={{maxWidth: 425}}>
                        <div style={{paddingBottom: 20}}>
                            <p style={{fontSize: '24px', fontWeight: '500', marginBottom: 8}}>
                                О компании {dataCard.companyName}</p>

                            <p style={{fontSize: '13px', fontWeight: '500', marginBottom: 8}}>{dataCard.description}</p>
                            <Button size={'small'} type={'default'} target={'_blank'}
                                    style={{padding: 5, height: 'auto', fontSize: 13}}

                                    href={`https://www.moex.com/ru/issue.aspx?board=TQBR&code=${id}`}>
                                Открыть компанию на Московской бирже
                            </Button>
                        </div>
                        <div>
                            <h2 style={{paddingBottom: 16, fontWeight: '500'}}>Сводный прогноз</h2>
                            <Space direction={'vertical'} size={'large'} style={{width: '100%'}}>
                                <div style={{padding: '12px 16px', border: 'solid 1px black', borderRadius: 8}}>
                                    <p>Прогнозная цена на час</p>
                                    <p>{dataCard.forecast.hour.price} <Typography.Text
                                        type={forecastHour >= 0 ? 'success' : 'danger'}>{forecastHour > 0 ? `+ ${forecastHour}` : forecastHour} ₽
                                        ({dataCard.forecast.hour.changePercentage}%)</Typography.Text></p>
                                </div>

                                <div style={{padding: '12px 16px', border: 'solid 1px black', borderRadius: 8}}>
                                    <p>Прогнозная цена на день</p>
                                    <p>{dataCard.forecast.day.price} <Typography.Text
                                        type={forecastWeek >= 0 ? 'success' : 'danger'}>{forecastDay > 0 ? `+ ${forecastDay}` : forecastDay} ₽
                                        ({dataCard.forecast.day.changePercentage}%)</Typography.Text></p>
                                </div>

                                <div style={{padding: '12px 16px', border: 'solid 1px black', borderRadius: 8}}>
                                    <p>Прогнозная цена на неделю</p>
                                    <p>{dataCard.forecast.week.price}
                                        <Typography.Text
                                            type={forecastWeek >= 0 ? 'success' : 'danger'}>{forecastWeek > 0 ? `+ ${forecastWeek}` : forecastWeek} ₽
                                            ({dataCard.forecast.week.changePercentage}%)</Typography.Text></p>
                                </div>
                            </Space>
                        </div>
                    </Col>
                </Row>
            </Card>
        </Space>
    );
};

export default Stock;
