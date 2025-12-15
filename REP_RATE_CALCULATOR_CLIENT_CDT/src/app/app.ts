import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from './services/api.service';
import { RatesManagement } from './pages/rates-management/rates-management';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, CommonModule, RatesManagement],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  title = 'CALCULADORA DE TASAS MEJOR CDT';
  developer = 'John Echeverry';
  cc = '1000901813';
  cel = '+57 301 607 0184';
  mail = 'johnhdz.160@gmail.com';
}
