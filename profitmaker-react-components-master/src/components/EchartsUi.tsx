import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import * as echarts from 'echarts';

export const EchartsUi = ({ options }: { options: any }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    // Initialize ECharts instance
    const myChart = echarts.init(chartRef.current);

    // Set the custom options or use default options if not provided
    const chartOptions = options || {
      // ... (Default options if options prop is not provided)
    };

    // Set the options to the chart instance
    myChart.setOption(chartOptions);

    // Cleanup the ECharts instance when the component unmounts
    return () => {
      myChart.dispose();
    };
  }, [options]);

  return <div ref={chartRef} style={{ width: '100%', height: '400px' }} />;
};

EchartsUi.propTypes = {
  options: PropTypes.object, // PropTypes for the options prop
};
