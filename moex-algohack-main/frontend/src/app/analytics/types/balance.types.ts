import { AnalyticsChart } from './chart.types';
import { Ticker } from './ticker.types';

export interface Balance {
  total: number;
  income: number;
  tickersCount: number;
  analytics?: AnalyticsChart;
}
