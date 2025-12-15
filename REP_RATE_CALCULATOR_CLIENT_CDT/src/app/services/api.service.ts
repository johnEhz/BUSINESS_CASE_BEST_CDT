import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom, lastValueFrom, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { RoiInterestCalculationResponse } from '../models/rates';

@Injectable({ providedIn: 'root' })
export class ApiService {
    private base = environment.apiBaseUrl;

    constructor(private http: HttpClient) { }

    uploadFile(file: File): Observable<any> {
        const formData = new FormData();
        formData.append('file', file);
        return this.http.post<any>(`${this.base}/upload-file`, formData);
    }

    calculateRoiInterest(body: {
        amount: string;
        term_in_days: string;
        base_days_in_year: number;
    }): Observable<RoiInterestCalculationResponse> {
        return this.http.post<RoiInterestCalculationResponse>(`${this.base}/calculate-roi-interest`, body)
    }

    calculatePeriodRate(body: {
        annual_effective_rate: string;
        period_frequency: number;
    }): Observable<any> {
        return this.http.post<any>(`${this.base}/calculate-period-rate`, body);
    }

    getBankQuotas(body: { amount: number; term_in_days: number }): Observable<any> {
        return this.http.post<any>(`${this.base}/get-bank-quotas`, body);
    }

    getUploadHistory(): Observable<any> {
        return this.http.get<any>(`${this.base}/get-file-upload-history`);
    }

    getUploadHistoryDetail(id_file: number): Observable<any> {
        return this.http.get<any>(`${this.base}/get-file-upload-history-detail?id_file=${id_file}`);
    }
}
