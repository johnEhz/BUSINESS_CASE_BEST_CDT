import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { JsonViewer } from '../json-viewer/json-viewer';

@Component({
  selector: 'app-expired-period-calculator',
  imports: [CommonModule, FormsModule, JsonViewer],
  templateUrl: './expired-period-calculator.html',
  styleUrl: './expired-period-calculator.css',
})
export class ExpiredPeriodCalculator {
  periodRateAer = '0.12';
  periodFrequency = 12;
  periodResults: any = null;
  periodLoading = false;
  constructor(private api: ApiService) { }

  calculatePeriodRate() {
    this.periodLoading = true;
    this.api.calculatePeriodRate({
      annual_effective_rate: this.periodRateAer,
      period_frequency: this.periodFrequency
    }).subscribe({
      next: (result: any) => {
        this.periodResults = result;
      },
      error: (err: unknown) => {
        console.error(err);
      },
      complete: () => {
        this.periodLoading = false;
      }
    });
  }
}
