import React, {FC, useEffect, useState} from 'react';
import {Button, Flex, Space} from "antd";
import styles from "./Stocks.module.scss";
import Stock from "./Stock";
import {mainApi} from "../../../api/Api";
import {StockFeed} from "../../../types";

const styleBtn: typeof Button.arguments['styles'] = {
    textAlign: 'left',
    fontWeight: 'bold',
    fontSize: '12px',
    lineHeight: 'normal'
};

const Stocks: FC = () => {
    const [stocksData, setStocksData] = useState<StockFeed[]>([]);
    const [typeStocks, setTypeStocks] = useState<number>(0);
    useEffect(() => {
        mainApi.getStocks(typeStocks).then((data) => {
            if (data) {
                setStocksData(data.length < 7 ? [...data, ...data, ...data] : data as StockFeed[]);
            }
        });
    }, [typeStocks])

    return (
        <>
            <div className={styles.listWrapper + ' gradient-background'}>
                <Flex gap={5} wrap={'nowrap'} vertical>
                    <Button style={styleBtn} danger={typeStocks === 0} onClick={() => setTypeStocks(0)}>
                        Взлеты
                    </Button>
                    <Button danger={typeStocks === 1} style={styleBtn} onClick={() => setTypeStocks(1)}>
                        Падения
                    </Button>
                    <Button style={styleBtn} danger={typeStocks === 2} onClick={() => setTypeStocks(2)}>
                        Рекомендованные
                    </Button>
                </Flex>
                {stocksData?.length > 0 && <div className={styles.listWrapperHidden}>
                    <Space className={styles.list}>
                        {stocksData.map((value) => {
                            return <>
                                <Stock key={value.company_id}{...value}/>
                            </>
                        })}
                        {stocksData.map((value) => {
                            return <>
                                <Stock key={value.company_id} {...value}/>
                            </>
                        })}
                    </Space>
                </div>}

            </div>

        </>
    );
};

export default Stocks;
