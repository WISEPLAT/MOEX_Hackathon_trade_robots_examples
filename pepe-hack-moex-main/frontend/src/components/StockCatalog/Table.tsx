import React, {useEffect, useState} from 'react';
import {Avatar, Flex, Space, Table as TableAnt, TablePaginationConfig, Tag} from 'antd';
import type {ColumnsType} from 'antd/es/table';
import styles from "./StockCatalog.module.scss";
import {useNavigate} from "react-router-dom";
import {StockFeed} from "../../types";
import {mainApi} from "../../api/Api";

interface DataType {
    id: number;
    description: string;
    companyIcon: string;
    companyName: string;
    background: string;
    stockPrice: number;
}

const columns: ColumnsType<DataType> = [
    {
        title: <div style={{marginLeft: 44}}>Название</div>,
        dataIndex: 'name',
        key: 'name',
        className: styles.row,
        render: (text, record) => <Flex align={'center'} gap={16} style={{marginLeft: 44}}>
            <Avatar
                style={{alignSelf: 'center', flexShrink: 0}}
                size={50}
                src={record.companyIcon}
            />
            <Flex gap={5} vertical>
                <p style={{fontSize: 13, fontWeight: 600}}>{record.companyName}</p>
                <p style={{fontSize: 13, fontWeight: 500, color: '#787878'}}>{record.description}</p>
            </Flex>
        </Flex>,
    },
    {
        title: <div style={{marginRight: 44}}>Текущая цена</div>,
        key: 'price',
        width: 200,
        render: (_, record) => (
            <Flex gap={5} vertical style={{marginRight: 44}}>
                <p style={{fontSize: 15, fontWeight: 400}}>{record.stockPrice}</p>
                <p style={{fontSize: 13, fontWeight: 400}}>1 лот = 1 акция</p>
            </Flex>
        ),
    },
];


const Table: React.FC<{ searchValue?: string }> = ({searchValue}) => {
    const navigate = useNavigate();
    const [stocksData, setStocksData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [tableParams, setTableParams] = useState<{ pagination: TablePaginationConfig }>({
        pagination: {
            current: 1,
            pageSize: 10
        },
    });

    function onClick(record: any): void {
        navigate(`/card/${record.id}`);
    }

    useEffect(() => {
        setLoading(true)
        mainApi.getStocksCatalog({
            searchValue,
            pageSize: 10,
            page: tableParams.pagination.current
        }).then((data) => {
            setStocksData(data || [] as any[]);
            setLoading(false);
        });
    }, [searchValue, tableParams]);

    const handleTableChange = (
        pagination: any
    ) => {
        setTableParams({
            pagination
        });

        if (pagination.pageSize !== tableParams.pagination?.pageSize) {
            setStocksData([]);
        }
    };


    return <TableAnt pagination={tableParams.pagination} loading={loading}
                     onRow={(record, rowIndex) => {
                         return {
                             onClick: () => onClick(record), // click row
                         };
                     }}
                     onChange={handleTableChange}
                     columns={columns} dataSource={stocksData}/>;
};
export default Table;
