import { Balance } from '@analytics/types/balance.types';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-balance',
  templateUrl: './balance.component.html',
  styleUrls: ['./balance.component.scss'],
})
export class BalanceComponent {
  @Input('balance') balance: Balance | null = null;
}
