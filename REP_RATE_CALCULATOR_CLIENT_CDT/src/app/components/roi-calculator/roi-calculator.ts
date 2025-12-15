import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RoiInterestCalculationResponse } from '../../models/rates';
import { JsonViewer } from '../json-viewer/json-viewer';

@Component({
  selector: 'app-roi-calculator',
  imports: [CommonModule, FormsModule, JsonViewer],
  templateUrl: './roi-calculator.html',
  styleUrl: './roi-calculator.css',
})
export class RoiCalculator {
  roiAmount = '5000000';
  roiTermDays = '90';
  roiBaseDays = 360;
  roiResults: RoiInterestCalculationResponse | null = null;
  roiLoading = false;
  constructor(private api: ApiService) { }

  calculateRoi() {
    this.roiLoading = true;
    this.api.calculateRoiInterest({
      amount: this.roiAmount,
      term_in_days: this.roiTermDays,
      base_days_in_year: this.roiBaseDays,
    }).subscribe({
      next: (result: RoiInterestCalculationResponse) => {
        this.roiResults = result;
      },
      error: (err: unknown) => {
        console.error(err);
      },
      complete: () => {
        this.roiLoading = false;
      }
    });
  }
}
