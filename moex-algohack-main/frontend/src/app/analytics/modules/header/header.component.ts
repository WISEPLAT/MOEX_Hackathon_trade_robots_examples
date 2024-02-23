import { BalanceService } from '@analytics/services/balance.service';
import { Component } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {
  constructor(protected readonly balacneSerivce: BalanceService) {}
}
