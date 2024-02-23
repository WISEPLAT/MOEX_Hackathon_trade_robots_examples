import { API, TICKERS } from '@analytics/analytics.constants';
import { Ticker } from '@analytics/types/ticker.types';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject, catchError, delay, of, tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class TickerService {
  loaded$ = new Subject<boolean>();
  data$ = new BehaviorSubject<Ticker[]>([]);

  constructor(private readonly http: HttpClient) {}

  load(): void {
    this.loaded$.next(false);

    this.http
      .get<Ticker[]>(`/${API}/tickers`)
      .pipe(tap(() => this.loaded$.next(true)))
      .subscribe((data) => this.data$.next(data));
  }
}
