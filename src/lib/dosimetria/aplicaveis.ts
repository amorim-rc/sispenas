// Quais modificadores são oferecidos a um dado tipo penal.
//
// Três filtros, nesta ordem:
//   1. ESCOPO   — o modificador alcança este diploma/título/artigo?
//   2. CONDIÇÃO — o tipo satisfaz o pré-requisito (admite tentativa etc.)?
//   3. EMBUTIDA — a causa já é preceito próprio deste tipo? Então não se
//                 oferece de novo (evita dupla contagem de cenários).

import type {Crime} from '../types';
import type {Modificador} from './types';

/**
 * Títulos da Parte Especial do CP por faixa de artigos. Necessário porque o
 * catálogo guarda o artigo, não o título — e há modificadores cujo escopo é o
 * título inteiro (art. 226 alcança todo o Título VI).
 */
const TITULOS_CP: {titulo: string; de: number; ate: number}[] = [
  {titulo: 'I', de: 121, ate: 154},    // contra a pessoa
  {titulo: 'II', de: 155, ate: 183},   // contra o patrimônio
  {titulo: 'III', de: 184, ate: 196},  // propriedade imaterial
  {titulo: 'IV', de: 197, ate: 207},   // organização do trabalho
  {titulo: 'V', de: 208, ate: 212},    // sentimento religioso e mortos
  {titulo: 'VI', de: 213, ate: 234},   // dignidade sexual
  {titulo: 'VII', de: 235, ate: 249},  // família
  {titulo: 'VIII', de: 250, ate: 285}, // incolumidade pública
  {titulo: 'IX', de: 286, ate: 288},   // paz pública
  {titulo: 'X', de: 289, ate: 311},    // fé pública
  {titulo: 'XI', de: 312, ate: 359},   // administração pública
];

/** Número do artigo de um registro do catálogo ("Art. 121, §2º, I" → 121). */
export function numeroArtigo(artigo: string): number | null {
  const m = /Art\.?\s*(\d+)/i.exec(artigo);
  return m ? Number(m[1]) : null;
}

function tituloDoCrime(c: Crime): string | null {
  if (!c.lei.startsWith('CP')) return null;
  const n = numeroArtigo(c.artigo);
  if (n === null) return null;
  return TITULOS_CP.find((t) => n >= t.de && n <= t.ate)?.titulo ?? null;
}

function leiBase(lei: string): string {
  return lei.replace(/\s*\(atualiz\.?\)/, '').trim();
}

function noEscopo(m: Modificador, c: Crime): boolean {
  const esc = m.escopo;
  switch (esc.tipo) {
    case 'geral':
      return true;
    case 'lei':
      return leiBase(c.lei) === esc.valor;
    case 'titulo':
      return leiBase(c.lei) === esc.lei && tituloDoCrime(c) === esc.valor;
    case 'tipos_por_artigo':
      return leiBase(c.lei) === esc.lei &&
        esc.artigos.some((a) => c.artigo.startsWith(a));
    case 'tipos':
      return esc.ids.includes(c.id);
    case 'combinador':
      return false; // concurso não é toggle do tipo; tem tela própria
    default:
      return false;
  }
}

function satisfazCondicao(m: Modificador, c: Crime): boolean {
  switch (m.condicao) {
    case undefined:
      return true;
    case 'admite_tentativa':
      return c.tentativa === 'Sim';
    case 'sem_violencia_ou_grave_ameaca':
      return c.violencia !== 'Sim' && c.grave_ameaca !== 'Sim';
    case 'papel_participe':
      return true; // depende do papel escolhido, não do tipo
    case 'nao_qualificado_pelo_mesmo_motivo':
      return true; // decisão do usuário (evitar bis in idem), apenas sinalizada
    default:
      return true;
  }
}

/**
 * A causa já é preceito próprio deste tipo? As causas de aumento embutidas
 * (§4º/§6º/§7º) permanecem como LINHAS do catálogo, com a moldura já calculada;
 * oferecer o modificador equivalente contaria o mesmo aumento duas vezes.
 * Detecta pelo dispositivo: se o modificador comina no mesmo artigo do tipo,
 * ele já está embutido.
 */
function jaEmbutida(m: Modificador, c: Crime): boolean {
  const artMod = numeroArtigo(m.dispositivo);
  const artCrime = numeroArtigo(c.artigo);
  if (artMod === null || artCrime === null) return false;
  const mesmaLei = m.dispositivo.startsWith('CP') && leiBase(c.lei).startsWith('CP');
  return mesmaLei && artMod === artCrime;
}

/** Modificadores oferecidos a um tipo penal, já filtrados e ordenados por fase. */
export function modificadoresAplicaveis(
  todos: Modificador[],
  crime: Crime,
): Modificador[] {
  return todos
    .filter((m) => m.escopo.tipo !== 'combinador')
    .filter((m) => noEscopo(m, crime))
    .filter((m) => satisfazCondicao(m, crime))
    .filter((m) => !jaEmbutida(m, crime));
}

/** Agrupa por fase, preservando a ordem 1 → 2 → 3 (a ordem do art. 68). */
export function porFase(mods: Modificador[]): {fase: 1 | 2 | 3; itens: Modificador[]}[] {
  return ([1, 2, 3] as const).map((fase) => ({
    fase,
    itens: mods.filter((m) => m.fase === fase),
  }));
}
