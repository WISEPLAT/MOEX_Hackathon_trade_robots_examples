import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'analytics',
    loadChildren: () => import('./analytics/analytics.module'),
  },
  {
    path: '**',
    redirectTo: 'analytics',
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
