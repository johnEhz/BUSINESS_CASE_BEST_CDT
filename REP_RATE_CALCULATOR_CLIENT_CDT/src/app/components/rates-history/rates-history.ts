import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { RatesHistoryDetail } from '../rates-history-detail/rates-history-detail';
import { formatDate } from '../../shared/utils/date_utils';

@Component({
  selector: 'app-rates-history',
  standalone: true,
  imports: [CommonModule, RatesHistoryDetail],
  templateUrl: './rates-history.html',
  styleUrl: './rates-history.css',
})
export class RatesHistory implements OnInit {

  constructor(private api: ApiService) { }
  loadingHistory = false;
  historyRecords: any[] = [];
  isVisible = true;
  showDetailModal = false;
  selectedAlerts: any[] = [];

  ngOnInit(): void {
    this.getUploadHistory();
  }

  toggleVisibility(): void {
    this.isVisible = !this.isVisible;
  }

  getUploadHistory(): any {
    this.loadingHistory = true;
    this.api.getUploadHistory().subscribe({
      next: (result: any) => {
        this.historyRecords = result.data;
      },
      error: (err: unknown) => {
        console.error(err);
      },
      complete: () => {
        this.loadingHistory = false;
      }
    });
  }

  getStatusLabel(status: string): string {
    const labels: { [key: string]: string } = {
      1: 'Pendiente',
      2: 'Error',
      3: 'Completado',
      4: 'Archivo cargado',
      5: 'Procesando...',
    };
    return labels[status] || status;
  }

  getStatusColor(status: string): string {
    const colors: { [key: string]: string } = {
      1: 'bg-yellow-100 text-yellow-800',
      2: 'bg-red-100 text-red-800',
      3: 'bg-green-100 text-green-800',
      4: 'bg-blue-100 text-blue-800',
      5: 'bg-purple-100 text-purple-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  }

  formatDate(dateString: string): string {
    return formatDate(dateString);
  }

  viewAlerts(fileId: number): void {
    this.api.getUploadHistoryDetail(fileId).subscribe({
      next: (result: any) => {
        this.selectedAlerts = result.data;
      },
      error: (err: unknown) => {
        console.error(err);
      }
    });
    this.showDetailModal = true;
  }

  closeDetailModal(): void {
    this.showDetailModal = false;
    this.selectedAlerts = [];
  }
}
