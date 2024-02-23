import React, {memo, useEffect, useState} from 'react';
import {mainApi} from "../../api/Api";
import {useParams} from "react-router-dom";
import CandleChart from "./CandleChart";
import {Button, DatePicker, Flex, TimeRangePickerProps} from "antd";
import LineChart from "./LineChart";
import type {Dayjs} from 'dayjs';
import dayjs from 'dayjs';

const Chart = memo(() => {
    const id = useParams().id;
    const [data, setData] = useState<any>([]);
    const [dateRange, setDateRange] = useState<any>([dayjs().add(-180, 'd'), dayjs()]);
    const [typeChart, setTypeChart] = useState<number>(0);

    useEffect(() => {
        if (!id || !dateRange || !dateRange[0] || !dateRange[1])
            return;
        asyncFetch(id, dateRange);
    }, [id, dateRange]);

    const asyncFetch = (id: any, dateRange: any) => {
        mainApi.getChartStock(id, [dateRange[0].format('YYYY-MM-DD'), dateRange[1].format('YYYY-MM-DD')])
            .then((json) => setData(json))
            .catch((error) => {
                console.log('fetch data failed', error);
            });
    };

    const rangePresets: TimeRangePickerProps['presets'] = [
        {label: 'Последняя неделя', value: [dayjs().add(-7, 'd'), dayjs()]},
        {label: 'Последний месяц', value: [dayjs().add(-30, 'd'), dayjs()]},
        {label: 'Последние полгода', value: [dayjs().add(-180, 'd'), dayjs()]},
        {label: 'Последний год', value: [dayjs().add(-365, 'd'), dayjs()]},
    ];

    function onChangeDate(dates: null | (Dayjs | null)[], dateStrings: string[]): void {
        setDateRange(dates);
    }

    return <div>
        <DatePicker.RangePicker style={{width: 250, marginBottom: 8}}
                                presets={rangePresets}
                                value={dateRange}
                                onChange={onChangeDate}
                                placeholder={['Старт', 'Конец']}/>
        <Flex gap={5} wrap={'nowrap'} style={{paddingBottom: 16}}>
            <Button danger={typeChart === 0} onClick={() => setTypeChart(0)}>
                Линия
            </Button>
            <Button danger={typeChart === 1} onClick={() => setTypeChart(1)}>
                Свечи
            </Button>
        </Flex>
        {typeChart === 0 ? <LineChart data={data}/> : <CandleChart data={data}/>}
    </div>;
});

export default Chart;
