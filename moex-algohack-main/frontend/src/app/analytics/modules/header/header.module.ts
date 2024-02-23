import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LogoComponent } from './components/logo/logo.component';
import { UserComponent } from './components/user/user.component';
import { BalanceComponent } from './components/balance/balance.component';
import { PercentComponent } from './components/percent/percent.component';
import { HeaderComponent } from './header.component';
import { SkeletonModule } from 'primeng/skeleton';

@NgModule({
  declarations: [
    LogoComponent,
    UserComponent,
    BalanceComponent,
    PercentComponent,
    HeaderComponent,
  ],
  imports: [CommonModule, SkeletonModule],
  exports: [HeaderComponent],
})
export class HeaderModule {}
