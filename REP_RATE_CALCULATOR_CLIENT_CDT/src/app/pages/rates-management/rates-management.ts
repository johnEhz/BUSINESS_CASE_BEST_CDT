import { Component } from '@angular/core';
import { BankQuotasForm } from '../../components/bank-quotas-form/bank-quotas-form';
import { ExpiredPeriodCalculator } from '../../components/expired-period-calculator/expired-period-calculator';
import { FileUpload } from '../../components/file-upload/file-upload';
import { RatesHistory } from '../../components/rates-history/rates-history';
import { RoiCalculator } from '../../components/roi-calculator/roi-calculator';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-rates-management',
  imports: [BankQuotasForm, ExpiredPeriodCalculator, RoiCalculator, FileUpload, RatesHistory],
  templateUrl: './rates-management.html',
  styleUrl: './rates-management.css',
})
export class RatesManagement {
  constructor(apiService: ApiService) { }
}
