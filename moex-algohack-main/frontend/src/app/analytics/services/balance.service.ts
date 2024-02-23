import { API } from '@analytics/analytics.constants';
import { Balance } from '@analytics/types/balance.types';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Subject, delay, tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class BalanceService {
  loading$ = new Subject<boolean>();
  balance$ = new Subject<Balance>();

  constructor(private readonly http: HttpClient) {}

  getBalance(): void {
    this.loading$.next(true);
    this.http
      .get<Balance>(`${API}/balance`)
      .pipe(
        tap({
          error: () => this.loading$.next(false),
        })
      )
      .subscribe((data) => {
        this.balance$.next(data);
        this.loading$.next(false);
      });
  }
}
