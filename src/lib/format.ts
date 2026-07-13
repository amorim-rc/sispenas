// Utilidades de formatação de pena (valores em MESES).

export function formatPena(meses: number | null | undefined): string {
  if (meses === null || meses === undefined || Number.isNaN(meses)) return '—';
  if (meses <= 0) return '—';
  if (meses < 1) {
    const dias = Math.round(meses * 30);
    return `${dias} ${dias === 1 ? 'dia' : 'dias'}`;
  }
  const m = Math.round(meses);
  const anos = Math.floor(m / 12);
  const rem = m % 12;
  if (anos === 0) return `${rem} ${rem === 1 ? 'mês' : 'meses'}`;
  if (rem === 0) return `${anos} ${anos === 1 ? 'ano' : 'anos'}`;
  return `${anos} ${anos === 1 ? 'ano' : 'anos'} e ${rem} ${rem === 1 ? 'mês' : 'meses'}`;
}

export function formatPenaCurta(meses: number | null | undefined): string {
  if (meses === null || meses === undefined || Number.isNaN(meses)) return '—';
  if (meses <= 0) return '—';
  if (meses < 1) return `${Math.round(meses * 30)}d`;
  const m = Math.round(meses);
  const anos = Math.floor(m / 12);
  const rem = m % 12;
  if (anos === 0) return `${rem}m`;
  if (rem === 0) return `${anos}a`;
  return `${anos}a${rem}m`;
}

const FRACOES: Record<string, string> = {
  '0.167': '1/6',
  '0.200': '1/5',
  '0.250': '1/4',
  '0.333': '1/3',
  '0.400': '2/5',
  '0.500': '1/2',
  '0.600': '3/5',
  '0.667': '2/3',
  '0.700': '7/10',
};

export function formatFracao(f: number): string {
  return FRACOES[f.toFixed(3)] ?? `${(f * 100).toFixed(0)}%`;
}
