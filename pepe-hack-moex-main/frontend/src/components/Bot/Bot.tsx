import React, {FC, memo, useEffect, useState} from 'react';
import {
    Button,
    Card,
    Col,
    DatePicker,
    DatePickerProps,
    Divider,
    Flex,
    notification,
    Row,
    Slider,
    Space,
    Typography
} from 'antd';
import StockTable from "./StockTable";
import {BellOutlined, SettingFilled} from "@ant-design/icons";
import {botApi} from "../../api/Api";
import HistoryTable from "./HistoryTable";
import {SliderMarks} from "antd/es/slider";
import {RangePickerProps} from "antd/es/date-picker";
import styles from './Bot.module.scss';
import dayjs from "dayjs";

const locStorageValue = localStorage.getItem('notify');

const marks: SliderMarks = {
    1: {
        style: {
            color: '#06AB03',
        },
        label: <strong>1</strong>,
    },
    5: {
        style: {
            color: '#FF0000',
        },
        label: <strong>5</strong>,
    },
};

const Bot: FC<{ removeBroker: () => void, broker: string }> = memo(({broker, removeBroker}) => {
    const [riskLvl, setRiskLvl] = useState(0);
    const [date, setDate] = useState<any>(dayjs().add(+1, 'd'));
    const [notify, setNotify] = useState(typeof locStorageValue === "undefined" ? true : locStorageValue === 'true');
    const [api, contextHolder] = notification.useNotification();
    const [dataBot, setDataBot] = useState<any>({
        "initialBalance": null,
        "currentBalance": null,
        "state": 0,
        "stocks": []
    });
    useEffect(() => {
        botApi.getBotInfo().then((data) => {
            setDataBot(data);
        });
        const interval = setInterval(() => {
            if (dataBot.state === 1) {
                botApi.getBotInfo().then((data) => {
                    setDataBot(data);
                    setRiskLvl(data.risk_level);
                });
            }
        }, 1000);
        return () => clearInterval(interval);
    }, [])

    const openNotification = (message: string) => {
        api.open({
            message: message,
            placement: 'topRight'
        });
    };

    function onNotifyClick(): void {
        setNotify((prev) => !prev);
        localStorage.setItem('notify', !notify ? 'true' : 'false');
        openNotification(!notify ? 'Уведомления включены' : 'Уведомления выключены');
    }

    function startStopBot(): void {
        if (!botIsStarted) {
            if (!date) {
                openNotification('Выберите дату');
                return;
            }
            botApi.startBot({risk_level: riskLvl, date_to: date.toISOString()});
            setDataBot({...dataBot, state: 1});
        } else {
            botApi.stopBot();
            setDataBot({...dataBot, state: 0});
        }
    }

    function onChangeDate(value: DatePickerProps['value'] | RangePickerProps['value'],
                          dateString: [string, string] | string,
    ): void {
        setDate(value);
    }

    const botIsStarted = dataBot.state === 1;
    return (
        <>
            {contextHolder}
            <Card bordered={true} size={"small"}
                  headStyle={{background: 'black', padding: '24px 64px'}}
                  title={<>
                      <Flex gap={16} align={'baseline'}>
                          <Typography.Title level={2} style={{margin: 0, marginBottom: 0, color: 'white'}}>Трейдер
                              бот
                          </Typography.Title>
                          <Button type="primary" shape="circle"
                                  style={!notify ? {background: '#dedcdc', color: 'black', borderColor: 'black'} : {}}
                                  ghost={!notify}
                                  title={notify ? 'Уведомления включены' : 'Уведомления выключены'}
                                  onClick={onNotifyClick}
                          >
                              <Flex vertical justify={'center'} align={'center'}>
                                  <BellOutlined/>
                              </Flex>
                          </Button>

                          <Typography.Title level={4}
                                            style={{margin: 0, marginBottom: 0, color: 'white', marginLeft: 'auto'}}>
                              Брокер: {broker}
                          </Typography.Title>
                          <Button onClick={removeBroker} type={'primary'}>
                              Сменить брокера
                          </Button>
                      </Flex>
                  </>
                  }
                  style={{boxShadow: '0px 4px 4px 0px rgba(0, 0, 0, 0.25)', padding: 0}}
                  bodyStyle={{padding: '20px 64px'}}
            >

                <Row justify={'space-between'} align={'stretch'}>
                    <Col span={6} style={{height: '100%', paddingTop: 25}}>
                        <Space direction={'vertical'} size={20}>
                            <div>
                                <h2 style={{paddingBottom: 20}}>Настройки {'  '}
                                    <span
                                        className={styles.startedBot + ' ' + (botIsStarted ? styles.startedBot__visible : '')}
                                        style={{
                                            fontSize: '0.7em',
                                            marginLeft: 10,
                                            color: 'gray'
                                        }}>бот запущен <SettingFilled spin/></span>
                                </h2>

                                <h3 style={{fontSize: 16, fontWeight: 600, marginBottom: 10}}>Время
                                    инвестирования</h3>
                                <DatePicker showTime style={{width: 300}} value={date} placeholder={'Выберите дату'}
                                            onChange={onChangeDate} disabled={botIsStarted}/>
                            </div>
                            <div>
                                <h3 style={{fontSize: 16, fontWeight: 600, marginBottom: 10}}>Уровень
                                    риска</h3>
                                <Slider max={5} min={1} onChange={setRiskLvl} value={riskLvl} disabled={botIsStarted}
                                        marks={marks}
                                        tooltip={{formatter: null}}/>
                                <p style={{fontSize: 13, color: 'gray', margin: 0}}>Чем выше уровень риска, тем более
                                    рисковые
                                    вложения будет совершать бот</p>
                            </div>
                            <Button size={'large'} type={'primary'} style={{width: '100%'}} className={styles.box}
                                    onClick={startStopBot}>
                                {botIsStarted ? 'Стоп' : 'Запустить'}</Button>
                        </Space>
                    </Col>
                    <Col span={16}>

                        <Card style={{width: '100%', boxShadow: '0px 4px 4px 0px rgba(0, 0, 0, 0.25)'}}>
                            <h2 style={{paddingBottom: 20}}>Мой портфель</h2>
                            <Row justify={'space-between'}>
                                <Col span={8}>
                                    <div style={{
                                        paddingBottom: 37,
                                        paddingTop: 16
                                    }}>
                                        {(dataBot.initialBalance && dataBot.currentBalance) ?
                                            <div>
                                                <h3 style={{fontSize: 16, fontWeight: 600}}>Текущее
                                                    состояние:</h3>
                                                <p style={{
                                                    fontSize: 24,
                                                    fontWeight: "bold",
                                                    whiteSpace: 'nowrap',
                                                    overflow: 'hidden',
                                                    textOverflow: 'ellipsis'
                                                }}>
                                                    {dataBot.currentBalance}<span
                                                    style={{color: '#06AB03'}}>+ {Math.ceil(dataBot.currentBalance / dataBot.initialBalance * 1000) / 10}%</span>
                                                </p>
                                                <Divider style={{margin: '10px 0'}}/>
                                                <h3 style={{fontSize: 16, fontWeight: 600, marginTop: 20}}>Внесено:</h3>
                                                <p style={{
                                                    fontSize: 24,
                                                    fontWeight: "bold",
                                                    whiteSpace: 'nowrap',
                                                    overflow: 'hidden',
                                                    textOverflow: 'ellipsis'
                                                }}>{dataBot.initialBalance}</p>
                                            </div>
                                            : null
                                        }
                                    </div>
                                </Col>
                                <Col>
                                    <div style={{marginTop: -62}}>
                                        <StockTable data={dataBot.stocks}/>
                                    </div>
                                </Col>
                            </Row>
                        </Card>
                    </Col>

                </Row>

                <h2 style={{fontSize: 24, marginBottom: 30, marginTop: 20}}>
                    История действий бота:
                </h2>

                <HistoryTable/>
            </Card>
        </>
    );
});

export default Bot;
