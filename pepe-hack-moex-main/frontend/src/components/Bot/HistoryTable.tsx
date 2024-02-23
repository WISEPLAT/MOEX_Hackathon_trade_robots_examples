import React, {memo, useEffect, useState} from 'react';
import {Table as TableAnt} from 'antd';
import type {ColumnsType} from 'antd/es/table';
import {botApi} from "../../api/Api";

interface DataType {
    action: string;
    action_color: string;
    action_id: number;
    comment: string;
    company_name: string;
    datetime: string;
    profit: string;
    stocks_count: number;
    currentPrice: number;
    user_id: number;
}

const columns: ColumnsType<DataType> = [
    {
        title: <div>Время</div>,
        dataIndex: 'datetime',
        key: 'datetime',
        width: 280,
        className: 'styles.row',
        render: (text, record) => <div>
            {new Date(record.datetime).toLocaleDateString('ru', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                second: 'numeric'
            })}
        </div>,
    },
    {
        title: <div>Событие</div>,
        dataIndex: 'action',
        key: 'action',
        className: 'styles.row',
        render: (text, record) => <div style={{color: record.action_color}}>
            {record.action}
        </div>,
    },
    {
        title: <div>Компания</div>,
        dataIndex: 'company_name',
        key: 'company_name',
        className: 'styles.row',
        render: (text, record) => <div>
            {record.company_name}
        </div>,
    },
    {
        title: <div>Количество</div>,
        dataIndex: 'stocksCount',
        key: 'stocksCount',
        className: 'styles.row',
        render: (text, record) => <div>
            {record.stocks_count}
        </div>,
    },
    {
        title: <div>Прибыль</div>,
        dataIndex: 'profit',
        key: 'profit',
        className: 'styles.row',
        render: (text, record) => <div>
            {record.profit}
        </div>,
    },
    {
        title: <div>Коментарий</div>,
        dataIndex: 'comment',
        key: 'comment',
        className: 'styles.row',
        render: (text, record) => <div>
            {record.comment}
        </div>,
    },
];

const HistoryTable: React.FC = memo(() => {
    const [data, setData] = useState<any>(null);
    useEffect(() => {
        botApi.getBotHistory().then((data) => {
            setData(data);
        });
        const interval = setInterval(() => {
            botApi.getBotHistory().then((data) => {
                setData(data);
            });
        }, 1000);
        return () => clearInterval(interval);
    }, [])

    function onClick(): void {
        // navigate(`/card`);
    }


    return <TableAnt pagination={false} onRow={(record, rowIndex) => {
        return {
            onClick: onClick, // click row
        };
    }}
                     columns={columns} dataSource={data}/>;
});
export default HistoryTable;
