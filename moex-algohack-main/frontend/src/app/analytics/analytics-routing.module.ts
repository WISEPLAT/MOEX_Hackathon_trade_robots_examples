import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AnalyticsComponent } from './analytics.component';

const rotues: Routes = [
  {
    path: '',
    component: AnalyticsComponent,
  },
];

@NgModule({
  imports: [RouterModule.forChild(rotues)],
  exports: [RouterModule],
})
export class AnalyticsRoutingModule {}
