import React, {FC, memo, useState} from 'react';
import Bot from "./Bot";
import {Button, Flex, Image, Select, Typography} from "antd";
import Img from './empty.jpg';
import {ToolOutlined} from "@ant-design/icons";

const AuthBot: FC = memo(() => {
    const localBroker = localStorage.getItem('broker');
    const [isAuth, setIsAuth] = useState(!!localBroker);
    const [loading, setLoading] = useState(false);
    const [options, setOptions] = useState<any>(localBroker ? JSON.parse(localBroker) : null);

    function auth(): void {
        setLoading(true);
        setTimeout(() => {
            setLoading(false);
            setIsAuth(true);
        }, 2000);
    }

    function onChangeBroker(value: any): void {
        setOptions(value);
        localStorage.setItem('broker', value ? JSON.stringify(value) : '');
        if (!value) {
            setIsAuth(false);
        }
    }

    return (
        <>
            {isAuth ? <Bot broker={options} removeBroker={() => onChangeBroker(null)}/> :
                <Flex vertical gap={20}>
                    <Typography.Title level={4}>Чтобы воспользоваться ботом нужно авторизоваться на
                        бирже</Typography.Title>
                    <Flex gap={16}>
                        <Select
                            disabled={loading}
                            value={options}
                            style={{width: 220}}
                            placeholder={'Выберите брокера'}
                            onChange={onChangeBroker}
                            options={[
                                {value: 'Tinkoff', label: 'Tinkoff'},
                                {value: 'БКС', label: 'БКС'},
                                {value: 'ИФК Солид', label: 'ИФК Солид'},
                                {value: 'Альфа-Инвестиции', label: 'Альфа-Инвестиции'},
                                {value: 'Сбер Инвестиции', label: 'Сбер Инвестиции'},
                            ]}
                        />
                        {options ? <Button loading={loading} onClick={auth}>Авторизоваться</Button> : null}
                    </Flex>
                </Flex>}
        </>
    );
});

export default AuthBot;
