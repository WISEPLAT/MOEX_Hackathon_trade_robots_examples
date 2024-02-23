import { Component, OnDestroy, OnInit } from '@angular/core';
import { TickerService } from '@analytics/services/ticker.service';
import { SettingService } from '@analytics/services/setting.service';
import { BalanceService } from '@analytics/services/balance.service';
import { MessageService } from 'primeng/api';
import {
  Subscriber,
  Subscription,
  filter,
  interval,
  map,
  startWith,
} from 'rxjs';
import { DELAY } from '@analytics/analytics.constants';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  providers: [MessageService],
})
export class DashboardComponent implements OnInit, OnDestroy {
  data: any;
  options: any;

  private subscriptions: Subscription[] = [];

  constructor(
    protected readonly tickerService: TickerService,
    protected readonly settingService: SettingService,
    protected readonly balanceService: BalanceService,
    private readonly messageService: MessageService
  ) {}

  ngOnInit(): void {
    this.tickerService.load();

    this.subscriptions.push(
      this.settingService.errorMessage$.subscribe((msg) =>
        this.messageService.addAll([
          {
            severity: 'error',
            detail: msg,
          },
        ])
      ),
      this.settingService.successMessage$.subscribe((msg) =>
        this.messageService.addAll([
          {
            severity: 'success',
            detail: msg,
          },
        ])
      ),
      interval(DELAY)
        .pipe(startWith(0))
        .subscribe(() => this.balanceService.getBalance()),
      this.balanceService.balance$
        .pipe(filter((data) => Boolean(data.analytics)))
        .subscribe((data) => {
          if (data.analytics) {
            this.data = {
              labels: data.analytics.labels ?? [],
              datasets: data.analytics.datasets.map(({ label, data }) => ({
                label,
                fill: false,
                yAxisID: 'y',
                tension: 0.4,
                data,
              })),
            };
          }
        })
    );

    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue(
      '--text-color-secondary'
    );
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    this.options = {
      stacked: false,
      maintainAspectRatio: false,
      responsive: true,
      aspectRatio: 0.6,
      plugins: {
        legend: {
          labels: {
            color: textColor,
          },
        },
      },
      scales: {
        x: {
          ticks: {
            color: textColorSecondary,
          },
          grid: {
            color: surfaceBorder,
          },
        },
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          ticks: {
            color: textColorSecondary,
          },
          grid: {
            color: surfaceBorder,
          },
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          ticks: {
            color: textColorSecondary,
          },
          grid: {
            drawOnChartArea: false,
            color: surfaceBorder,
          },
        },
      },
    };
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach((item) => item.unsubscribe());
  }
}
