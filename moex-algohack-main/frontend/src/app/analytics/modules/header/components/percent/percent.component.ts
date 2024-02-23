import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-percent',
  templateUrl: './percent.component.html',
  styleUrls: ['./percent.component.scss'],
})
export class PercentComponent {
  @Input('percent') percent: number = 0;
}
