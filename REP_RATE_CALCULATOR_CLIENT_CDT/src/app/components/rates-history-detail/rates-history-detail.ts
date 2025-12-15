import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { formatDate } from '../../shared/utils/date_utils';

@Component({
  selector: 'app-rates-history-detail',
  imports: [CommonModule],
  templateUrl: './rates-history-detail.html',
  styleUrl: './rates-history-detail.css',
})
export class RatesHistoryDetail {
  @Input() isOpen = false;
  @Input() alerts: any[] = [];
  @Output() close = new EventEmitter<void>();


  closeModal(): void {
    this.close.emit();
  }

  formatDate(dateString: string): string {
    return formatDate(dateString);
  }

  getAlertTypeLabel(typeId: number): string {
    const alertTypes: { [key: number]: string } = {
      3: 'Rango Inválido',
      4: 'Valor en Cero',
      5: 'Tasa Inválida',
      6: 'Columna Inválida',
      7: 'Error de Conversión',
    };
    return alertTypes[typeId] || `Tipo ${typeId}`;
  }

  getAlertTypeColor(typeId: number): string {
    const colors: { [key: number]: string } = {
      3: 'bg-yellow-100 text-yellow-700',
      4: 'bg-red-100 text-red-700',
      5: 'bg-blue-100 text-blue-700',
      6: 'bg-purple-100 text-purple-700',
      7: 'bg-pink-100 text-pink-700',
    };
    return colors[typeId] || 'bg-gray-100 text-gray-700';
  }
}
