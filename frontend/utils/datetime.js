export const DATE_OPTIONS = {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  hour: 'numeric',
  minute: 'numeric',
  second: 'numeric',
}

export function formatDateTime(dateTimeISO, options) {
  return new Date(Date.parse(dateTimeISO)).toLocaleString('ru-RU', options || DATE_OPTIONS)
}
