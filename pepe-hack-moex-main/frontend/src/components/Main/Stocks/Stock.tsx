import React, {FC} from 'react';
import {Card, Divider, Flex, Typography} from "antd";
import styles from "./Stocks.module.scss";
import {StockFeed} from "../../../types";
import {useNavigate} from "react-router-dom";

const Stock: FC<StockFeed> = ({price, pricePercentage, companyName, companyIcon, id}) => {
    const changeIsPositive = pricePercentage >= 0;
    const navigate = useNavigate();

    function onClick(): void {
        navigate(`/card/${id}`);
    }

    return (
        <Card className={styles.card} bordered={true} size={"small"} onClick={onClick} hoverable={true}>
            <Flex vertical align={'center'}>
                <Typography.Text strong><span>{price || '0,00'}</span> <Typography.Text
                    type={changeIsPositive ? 'success' : 'danger'}>{changeIsPositive && '+'} {pricePercentage}%</Typography.Text></Typography.Text>
                <Divider style={{margin: '5px 0'}}/>
                <Flex gap={5} align={'center'} flex={"0 0 0"} style={{width: '100%', minWidth: 0}} justify={'center'}>
                    <img alt="icon" src={companyIcon}
                         style={{display: 'inline-block', width: 20, height: 20, borderRadius: '50%'}}/>
                    <Typography.Text style={{
                        verticalAlign: 'middle',
                        gap: '5px',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                    }}>
                        {companyName}
                    </Typography.Text>
                </Flex>

            </Flex>
        </Card>
    );
};

export default Stock;
