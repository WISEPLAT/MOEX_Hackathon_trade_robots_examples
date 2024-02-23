import React, {FC, useState} from 'react';
import {Card, Flex, Typography} from 'antd';
import Search from "antd/es/input/Search";
import Table from "./Table";

const StockCatalog: FC = () => {
    const [searchValue, setSearchValue] = useState('');

    function onChangeSearch(e: typeof Search.arguments.onChange) {
        setSearchValue(e.target.value);
    }

    return (
        <Card bordered={true} size={"small"}
              headStyle={{background: 'black', padding: '24px 64px'}}
              title={
                  <Flex vertical
                        gap={'small'} style={{color: 'white'}}
                  >
                      <Typography.Title level={2} style={{margin: 0, marginBottom: 8, color: 'white'}}>Каталог
                          акций</Typography.Title>
                      <Typography.Text style={{marginBottom: 4, fontWeight: 300, color: 'white'}}>
                          Выберете необходимую компанию для получения
                          прогноза</Typography.Text>
                      <Search value={searchValue} onChange={onChangeSearch}
                              style={{maxWidth: '500px'}} allowClear placeholder={"Название или тикер"} width={'100%'}/>
                  </Flex>
              }
              style={{boxShadow: '0px 4px 4px 0px rgba(0, 0, 0, 0.25)', padding: 0}}
              bodyStyle={{padding: '0px 0px'}}
        >
            <Table searchValue={searchValue}/>
        </Card>

    );
};

export default StockCatalog;
