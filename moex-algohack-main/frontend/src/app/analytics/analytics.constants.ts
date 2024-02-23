import { Ticker } from '@analytics/types/ticker.types';
import { Balance } from './types/balance.types';

export const API = 'api';
export const DELAY = 15000;

export const TICKERS: Ticker[] = [
  {
    name: 'МосБиржа',
    code: 'MOEX',
  },
  {
    name: 'МТС-ао',
    code: 'MTSS',
  },
  {
    name: 'Сбербанк',
    code: 'SBER',
  },
];

export const BALANCE: Balance = {
  income: 100,
  total: 100000,
  tickersCount: 10,
};
