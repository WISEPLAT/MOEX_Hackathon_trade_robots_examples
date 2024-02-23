import React from 'react';
import {Avatar, Flex, Space, Table as TableAnt, Tag} from 'antd';
import type {ColumnsType} from 'antd/es/table';
import {useNavigate} from "react-router-dom";

interface DataType {
    companyName: string;
    stocksCount: number;
    currentPrice: number;
    purchasePrice: number;
}

const columns: ColumnsType<DataType> = [
    {
        title: <div>Компания</div>,
        dataIndex: 'company',
        key: 'company',
        className: 'styles.row',
        render: (text, record) => <div>
            {record.companyName}
        </div>,
    },
    {
        title: <div>Кол-во</div>,
        dataIndex: 'count',
        key: 'count',
        className: 'styles.row',
        render: (text, record) => <div>
            {record.stocksCount}
        </div>,
    },
    {
        title: <div>Цена покупки</div>,
        dataIndex: 'purchasePrice',
        key: 'purchasePrice',
        className: 'styles.row',
        render: (text, record) => <div>
            {record.purchasePrice}
        </div>,
    },
    {
        title: <div>Текущая цена</div>,
        dataIndex: 'currentPrice',
        key: 'currentPrice',
        className: 'styles.row',
        render: (text, record) => <div>
            {record.currentPrice}
        </div>,
    },
];

const StockTable: React.FC<{data: any}> = ({data}) => {
    const navigate = useNavigate();

    function onClick(): void {
        // navigate(`/card`);
    }

    return <TableAnt pagination={false}
                     style={{maxHeight: '300px', overflowY: 'auto'}}
                     onRow={(record, rowIndex) => {
        return {
            onClick: onClick, // click row

        };
    }}
                     columns={columns} dataSource={data}/>;
};
export default StockTable;
