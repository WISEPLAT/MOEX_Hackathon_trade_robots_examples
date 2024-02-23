import { FormControl } from '@angular/forms';
import { Ticker } from './ticker.types';

export interface SettigAnalyticsForm {
  ticker: FormControl<Ticker | null>;
  param1: FormControl<number>;
  param2: FormControl<number>;
}
export interface SettigAnalytics {
  ticker: Ticker | null;
  param1: number;
  param2: number;
}

export interface SettigAnalyticsRequest {
  ticker: string;
  param1: number;
  param2: number;
}
