import React, {FC, memo} from 'react';
import {Stock} from '@ant-design/plots';

const CandleChart: FC<{ data: any }> = memo(({data}) => {
    const config = {
        data,
        xField: 'trade_date',
        yField: ['open', 'close', 'high', 'low'],
        slider: {
            start: 0.8,
            end: 1,
        }
    };

    return <Stock {...config as any} />;
});

export default CandleChart;
