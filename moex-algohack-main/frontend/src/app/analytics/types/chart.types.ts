export interface AnalyticsChart {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
  }>;
}
