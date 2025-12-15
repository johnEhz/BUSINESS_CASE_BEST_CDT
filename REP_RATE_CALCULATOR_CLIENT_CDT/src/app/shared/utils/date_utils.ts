export const formatDate = (dateString: string): string => {
  const utcDate = new Date(dateString + 'Z');

  return new Intl.DateTimeFormat('es-CO', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
    timeZone: 'America/Bogota',
  }).format(utcDate);
}