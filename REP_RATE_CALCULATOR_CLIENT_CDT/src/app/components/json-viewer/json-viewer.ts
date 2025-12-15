import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-json-viewer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './json-viewer.html',
  styleUrl: './json-viewer.css',
})
export class JsonViewer {
  @Input() data: any = null;
  copySuccess = false;
  copyError = false;

  get prettyJson(): string {
    return this.data ? JSON.stringify(this.data, null, 2) : '';
  }

  async copyJson(): Promise<void> {
    this.copySuccess = false;
    this.copyError = false;
    try {
      const text = this.prettyJson;
      if (!text) return;
      if (navigator?.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
      }
      this.copySuccess = true;
      setTimeout(() => this.copySuccess = false, 2000);
    } catch (err) {
      console.error('Error copying JSON', err);
      this.copyError = true;
      setTimeout(() => this.copyError = false, 2000);
    }
  }

  downloadJson(): void {
    const text = this.prettyJson;
    if (!text) return;
    const blob = new Blob([text], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'data.json';
    link.click();
    URL.revokeObjectURL(url);
  }
}
