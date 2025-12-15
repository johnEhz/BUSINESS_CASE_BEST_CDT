import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './file-upload.html',
  styleUrl: './file-upload.css',
})
export class FileUpload {
  selectedFile: File | null = null;
  uploadMessage: string | null = null;
  uploadError: string | null = null;
  isLoading = false;

  constructor(private apiService: ApiService) { }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const files = input.files;

    if (files && files.length > 0) {
      const file = files[0];

      // Validar que sea CSV
      if (!file.name.endsWith('.csv')) {
        this.uploadError = 'Por favor selecciona un archivo CSV válido.';
        this.selectedFile = null;
        return;
      }

      // Validar tamaño (ej: máximo 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        this.uploadError = 'El archivo es muy grande. Máximo 5MB.';
        this.selectedFile = null;
        return;
      }

      this.selectedFile = file;
      this.uploadError = null;
      this.uploadMessage = null;
    }
  }

  uploadFile() {
    if (!this.selectedFile) {
      this.uploadError = 'Selecciona un archivo primero.';
      return;
    }

    this.isLoading = true;
    this.uploadError = null;
    this.uploadMessage = null;

    this.apiService.uploadFile(this.selectedFile).subscribe({
      next: (data) => {
        this.uploadMessage = `Archivo ${this.selectedFile?.name} subido exitosamente.`;
        this.selectedFile = null;
        const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
      },
      error: (err) => {
        this.uploadError = `Error: ${String(err.error.error)}`;
        this.isLoading = false;
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }
}
