import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { JsonViewer } from '../json-viewer/json-viewer';

@Component({
  selector: 'app-bank-quotas-form',
  imports: [CommonModule, FormsModule, ReactiveFormsModule, JsonViewer],
  templateUrl: './bank-quotas-form.html',
  styleUrl: './bank-quotas-form.css',
})
export class BankQuotasForm {
  quotasLoading = false;
  quotasResults: any[] = [];
  investmentSummary: any = null;
  investedSummaryError: string | null = null;
  quotasForm: FormGroup;

  constructor(private api: ApiService, private fb: FormBuilder) {
    this.quotasForm = this.fb.group({
      quotasAmount: [5000000, [Validators.required, Validators.pattern(/^[0-9]+(\.[0-9]{1,2})?$/), this.positiveValidator.bind(this)]],
      quotasTermDays: [90, [Validators.required, Validators.pattern(/^[0-9]+(\.[0-9]{1,2})?$/), this.positiveValidator.bind(this)]],
    });
  }

  positiveValidator(control: any) {
    if (!control.value) return null;
    const value = parseFloat(control.value);
    return value > 0 ? null : { positiveRequired: true };
  }

  getFieldError(fieldName: string): string | null {
    const control = this.quotasForm.get(fieldName);
    if (!control || !control.errors || !control.touched) return null;
    if (control.errors['required']) return 'Este campo es requerido';
    if (control.errors['pattern']) return 'Solo se permiten números positivos';
    if (control.errors['positiveRequired']) return 'El valor debe ser mayor a 0';
    return null;
  }

  getBankQuotas() {
    if (!this.quotasForm.valid) {
      this.investedSummaryError = 'Por favor, completa todos los campos correctamente';
      return;
    }

    this.investedSummaryError = null;
    this.quotasLoading = true;
    const formValue = this.quotasForm.value;

    this.api.getBankQuotas({
      amount: formValue.quotasAmount,
      term_in_days: formValue.quotasTermDays,
    }).subscribe({
      next: (result: any) => {
        this.quotasResults = result;
      },
      error: (err: any) => {
        this.investedSummaryError = String(err.error.error);
        this.quotasLoading = false;
      },
      complete: () => {
        this.quotasLoading = false;
      }
    });
  }
}
