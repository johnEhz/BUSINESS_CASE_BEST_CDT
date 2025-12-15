import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { RoiInterestCalculationResponse } from '../../models/rates';
import { JsonViewer } from '../json-viewer/json-viewer';

@Component({
  selector: 'app-roi-calculator',
  imports: [CommonModule, FormsModule, ReactiveFormsModule, JsonViewer],
  templateUrl: './roi-calculator.html',
  styleUrl: './roi-calculator.css',
})
export class RoiCalculator {
  roiForm: FormGroup;
  roiResults: RoiInterestCalculationResponse | null = null;
  roiLoading = false;
  roiLoadingError: string | null = null;

  constructor(private api: ApiService, private fb: FormBuilder) {
    this.roiForm = this.fb.group({
      roiAmount: ['5000000', [Validators.required, Validators.pattern(/^[0-9]+(\.[0-9]{1,2})?$/), this.positiveValidator.bind(this)]],
      roiTermDays: ['90', [Validators.required, Validators.pattern(/^[0-9]+(\.[0-9]{1,2})?$/), this.positiveValidator.bind(this)]],
      roiBaseDays: [360, [Validators.required, Validators.pattern(/^[0-9]+(\.[0-9]{1,2})?$/), this.positiveValidator.bind(this), Validators.min(1), Validators.max(366)]],
    });
  }

  positiveValidator(control: any) {
    if (!control.value) return null;
    const value = parseFloat(control.value);
    return value > 0 ? null : { positiveRequired: true };
  }

  getFieldError(fieldName: string): string | null {
    const control = this.roiForm.get(fieldName);
    if (!control || !control.errors || !control.touched) return null;

    if (control.errors['required']) return 'Este campo es requerido';
    if (control.errors['pattern']) return 'Solo se permiten números positivos';
    if (control.errors['positiveRequired']) return 'El valor debe ser mayor a 0';
    if (control.errors['min']) return 'Debe ser al menos 1';
    if (control.errors['max']) return 'No puede exceder 366 días';
    return null;
  }

  calculateRoi() {
    if (!this.roiForm.valid) {
      this.roiLoadingError = 'Por favor, completa todos los campos correctamente';
      return;
    }

    this.roiLoadingError = null;
    this.roiLoading = true;
    const formValue = this.roiForm.value;
    
    this.api.calculateRoiInterest({
      amount: String(formValue.roiAmount),
      term_in_days: String(formValue.roiTermDays),
      base_days_in_year: formValue.roiBaseDays,
    }).subscribe({
      next: (result: RoiInterestCalculationResponse) => {
        this.roiResults = result;
      },
      error: (err: any) => {
        this.roiLoadingError = String(err.error.error);
        this.roiLoading = false;
      },
      complete: () => {
        this.roiLoading = false;
      }
    });
  }
}
