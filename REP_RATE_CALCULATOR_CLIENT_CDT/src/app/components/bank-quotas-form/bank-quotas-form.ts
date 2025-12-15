import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { JsonViewer } from '../json-viewer/json-viewer';

@Component({
  selector: 'app-bank-quotas-form',
  imports: [CommonModule, FormsModule, JsonViewer],
  templateUrl: './bank-quotas-form.html',
  styleUrl: './bank-quotas-form.css',
})
export class BankQuotasForm {
  quotasLoading = false;
  quotasAmount = '5000000'
  quotasResults: any[] = [];
  quotasTermDays = '90';
  investmentSummary: any = null;
  apiError: string | null = null;

  constructor(private api: ApiService) { }

  getBankQuotas() {
    this.quotasLoading = true;
    this.api.getBankQuotas({
      amount: this.quotasAmount,
      term_in_days: this.quotasTermDays,
    }).subscribe({
      next: (result: any) => {
        this.quotasResults = result;
      },
      error: (err: unknown) => {
        this.apiError = String(err);
      },
      complete: () => {
        this.quotasLoading = false;
      }
    });
  }
}
