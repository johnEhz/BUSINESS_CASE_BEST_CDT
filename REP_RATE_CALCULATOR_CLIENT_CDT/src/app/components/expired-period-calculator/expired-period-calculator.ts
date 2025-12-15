import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { JsonViewer } from '../json-viewer/json-viewer';

@Component({
  selector: 'app-expired-period-calculator',
  imports: [CommonModule, FormsModule, ReactiveFormsModule, JsonViewer],
  templateUrl: './expired-period-calculator.html',
  styleUrl: './expired-period-calculator.css',
})
export class ExpiredPeriodCalculator {
  periodForm: FormGroup;
  periodResults: any = null;
  periodLoading = false;
  expiredPeriodError: string | null = null;

  constructor(private api: ApiService, private fb: FormBuilder) {
    this.periodForm = this.fb.group({
      periodRateAer: [0.12, [Validators.required, Validators.pattern(/^[0-9]+(\.[0-9]{1,4})?$/), this.positiveValidator.bind(this)]],
      periodFrequency: [12, [Validators.required, Validators.pattern(/^[0-9]+(\.[0-9]{1,2})?$/), this.positiveValidator.bind(this)]],
    });
  }

  positiveValidator(control: any) {
    if (!control.value) return null;
    const value = parseFloat(control.value);
    return value > 0 ? null : { positiveRequired: true };
  }

  getFieldError(fieldName: string): string | null {
    const control = this.periodForm.get(fieldName);
    if (!control || !control.errors || !control.touched) return null;
    if (control.errors['required']) return 'Este campo es requerido';
    if (control.errors['pattern']) return 'Solo se permiten números positivos';
    if (control.errors['positiveRequired']) return 'El valor debe ser mayor a 0';
    return null;
  }

  calculatePeriodRate() {
    if (!this.periodForm.valid) {
      this.expiredPeriodError = 'Por favor, completa todos los campos correctamente';
      return;
    }
    this.expiredPeriodError = null;
    this.periodLoading = true;
    const formValue = this.periodForm.value;
    this.api.calculatePeriodRate({
      annual_effective_rate: String(formValue.periodRateAer),
      period_frequency: formValue.periodFrequency
    }).subscribe({
      next: (result: any) => this.periodResults = result,
      error: (err: any) => { this.expiredPeriodError = String(err.error.error); this.periodLoading = false; },
      complete: () => this.periodLoading = false
    });
  }
}