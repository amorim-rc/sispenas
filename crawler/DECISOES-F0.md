# F0 — Decisões do spike (29/07/2026)

Entregável da fase F0 do `PLANO-CRAWLER.md`. Experimentos executados ao vivo
contra o Planalto em 29/07/2026; evidências citadas abaixo.

## 1. Estratégia de fetch — **Playwright obrigatório** (decidido)

| Experimento | Resultado |
|---|---|
| `curl` sem User-Agent | **Recusado** (resposta vazia). |
| `curl` com UA de Chrome — CP, CPM, 9.605, 8.137 | Página **atual** (sentinelas 15.384/14.688/15.355/LC 224 presentes). |
| `curl` com UA — **Lei 11.340 (Maria da Penha)** | Página **ANTIGA, pré-2018** (sem art. 24-A, sem Lei 13.641), embora `Last-Modified: 02/07/2026`. |
| + `Cache-Control: no-cache`, `Pragma`, query cache-buster | **Mesmos bytes antigos.** |
| + cookie jar (TS01/f5_cspm do BIG-IP) + Referer | **Mesmos bytes antigos.** |
| Navegador real (mesmo instante, mesma URL) | Página **atual** (24-A, 14.994, 15.383 presentes). |

Conclusão: o CDN do Planalto (F5/BIG-IP) serve **variantes arcaicas por página**
a clientes não-navegador, por fingerprinting que UA/headers/cookies não
contornam — e o `Last-Modified` **mente**. O dano é silencioso e a página afetada
é imprevisível (4 de 5 vieram frescas; a 5ª veio de ~2017). Portanto:

- **Fetcher da F1 usa exclusivamente Playwright/Chromium** — sem caminho
  HTTP "otimizado" (o risco não compensa a economia de ~60 páginas/semana).
- **Sentinela por fonte continua obrigatória** (defesa em profundidade: pega
  regressão do próprio Planalto e cache velho em datacenter da CI).

## 2. Encoding — **windows-1252 por padrão** (decidido)

Todas as 6 páginas amostradas: **sem `<meta charset>`**, `Content-Type:
text/html` **sem charset**, e conteúdo que **não é UTF-8 válido**. Decodificar
`cp1252` por padrão; tentar UTF-8 primeiro e cair para cp1252 no
`UnicodeDecodeError` (páginas novas do Planalto podem vir em UTF-8).

## 3. Estrutura HTML (levantamento no CP compilado atual)

1. **Anotações são links estruturados** — ex.:
   `<a href="../_Ato2023-2026/2026/Lei/L15384.htm#art3">(Incluído pela Lei nº
   15.384, de 2026)</a>`. O `href` entrega a URL da lei alteradora **e a âncora
   do artigo** — insumo direto para o checador de vigência (5.6) sem resolver
   URL por conta própria.
2. **Artigo totalmente revogado tem o corpo REMOVIDO**: resta
   `Art. 217 - (Revogado pela Lei nº 11.106, de 2005)` (link). Detecção de
   `situacao=revogado`: anotação de revogação imediatamente após o cabeçalho do
   artigo, sem preceito/pena. Simplifica o parser.
3. **Dispositivo alterado mantém a redação antiga em texto plano** (sem
   riscado), seguida da nova com "(Redação dada…)". `<strike>` existe mas é
   raro/legado (6 ocorrências no CP inteiro, envolvendo cabeçalhos de capítulo
   revogado). Confirma a regra do plano (5.3-1): **a versão vigente é a de
   anotação mais recente** — nunca confiar em riscado.
4. Layout é HTML de Word (MSO): `<font>`, `&nbsp;` de indentação, `<p>` com
   estilos inline. Parsear por parágrafo extraindo texto + links; não esperar
   marcação semântica.

## 4. LexML — **descartado como verificação automática** (decidido)

- Página URN (`lexml.gov.br/urn/...lei:1989-07-11;7802`): 200 OK, mas **sem os
  metadados de revogação** no HTML estático (não cita a Lei 14.785).
- API SRU: respondida por **challenge anti-bot do Senado** ao curl.

A detecção de revogação total (armadilha dos agrotóxicos) fica com: (a) banner
no topo do snapshot; (b) **o watcher do DOU (5.11/F7)** — a lei revogadora nova
casa tanto a citação do diploma quanto o vocabulário penal, cobrindo o caso
dali em diante. O componente `revogacao.py` da F4 perde a perna LexML.

## 5. Ajustes decorrentes no plano

- F1: dependência única de fetch = `playwright` (sem modo HTTP).
- F4: critério de aceite passa a ser o caso 7.802 detectado **por banner** (e o
  caso futuro coberto pelo watcher da F7); some a menção a LexML.
- Fixture obrigatória da F2: o HTML **do navegador** da Lei 11.340 (o snapshot
  curl desta página é inútil — está pré-2018).
