import { API } from '@analytics/analytics.constants';
import {
  SettigAnalytics,
  SettigAnalyticsForm,
  SettigAnalyticsRequest,
} from '@analytics/types/settings.types';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Subject, finalize, tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class SettingService {
  loading$ = new Subject<boolean>();
  successMessage$ = new Subject<string>();
  errorMessage$ = new Subject<string>();

  form: FormGroup<SettigAnalyticsForm> = this.fb.group<SettigAnalyticsForm>({
    ticker: this.fb.control(null),
    param1: this.fb.control(1, { nonNullable: true }),
    param2: this.fb.control(50, { nonNullable: true }),
  });

  constructor(
    private readonly fb: FormBuilder,
    private readonly http: HttpClient
  ) {}

  post() {
    this.loading$.next(true);
    this.http
      .post(`${API}/analytics`, this.prepareData(this.form.getRawValue()))
      .pipe(
        tap({
          error: () => {
            this.loading$.next(false);
            this.errorMessage$.next('Ошибка сохраненения');
          },
        })
      )
      .subscribe(() => {
        this.successMessage$.next('Настройки сохранены');
        this.loading$.next(false);
      });
  }

  private prepareData(data: SettigAnalytics): SettigAnalyticsRequest {
    return {
      ...data,
      ticker: data.ticker?.code ?? '',
    };
  }
}
