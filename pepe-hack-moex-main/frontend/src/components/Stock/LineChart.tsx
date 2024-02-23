import React, {FC, memo, useEffect, useState} from 'react';
import {Line} from '@ant-design/plots';
import {mainApi} from "../../api/Api";
import {Datum} from "@ant-design/charts";
import {useParams} from "react-router-dom";

const Chart: FC<{ data: any }> = memo(({data}) => {
    const config: any = {
        data,
        padding: 'auto',
        xField: 'trade_date',
        yField: 'close',
        xAxis: {
            tickCount: 5,
        },
        slider: {
            start: 0.8,
            end: 1,
        },
        meta: {
            'close': 'Стоимость'
        }
    };

    return <Line {...config} />;
});

export default Chart;
