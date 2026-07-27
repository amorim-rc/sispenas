// Contrato de uma entrada do changelog.
//
// O formato foi desenhado para que um backend futuro produza EXATAMENTE o mesmo
// JSON (um array de ChangelogEntry) sem que o frontend precise mudar. Por isso:
//   - `body` é texto puro (sem markdown, sem backticks); cada string é um
//     parágrafo, renderizado as-is.
//   - não há lista central: cada entrada é um arquivo próprio em
//     entries/<ano>/<id>.ts, e index.ts agrega tudo por require.context.
//
// Adaptado da abordagem do EBANX à realidade do SISPENAS: no lugar de
// status/domain/countries/paymentMethods, os dois eixos que definimos —
// `tipo` (a natureza da mudança) e `areas` (a parte do sistema).

/** A natureza da mudança. Espelha o versionamento semântico do projeto. */
export type ChangelogTipo =
  | 'novidade' // funcionalidade nova (1.Y.0)
  | 'melhoria' // aprimoramento sem mudar dado
  | 'correcao' // correção de dado ou norma (1.1.Z)
  | 'estrutural'; // quebra de contrato de dados/URLs (X.0.0)

/** A parte do sistema afetada. */
export type ChangelogArea =
  | 'Tipos penais'
  | 'Benefícios'
  | 'Dosimetria'
  | 'Acervo histórico'
  | 'Interface'
  | 'Documentação';

/** "Onde a mudança aparece" — o link para o local exato. */
export interface ChangelogLink {
  label: string;
  href: string;
}

export interface ChangelogEntry {
  /** YYYY-MM-DD-<slug>, idêntico ao nome do arquivo (sem extensão). */
  id: string;
  /** Data ISO, YYYY-MM-DD. */
  date: string;
  title: string;
  /** Um parágrafo de resumo. */
  summary: string;
  /** Parágrafos em texto puro, renderizados as-is (sem markdown). */
  body: string[];
  tipo: ChangelogTipo;
  areas: ChangelogArea[];
  /** Ex.: "v1.2.0". Ausente em entradas não atreladas a uma versão. */
  version?: string;
  links?: ChangelogLink[];
}
