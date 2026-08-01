# A segunda-feira do SISPENAS

Documento interno de operação — não é publicado no site. Responde a uma pergunta:
**o que chega para mim toda semana, e o que cada coisa exige.**

A rodada automática acontece **toda segunda-feira, 05:00 de Brasília**
(`.github/workflows/conferidor.yml`), e também sob demanda em Actions ▸ *Conferidor
semanal* ▸ **Run workflow**. Ela produz, no máximo, **três coisas**: um commit, uma issue
e um pull request.

## 1. Um commit que chega sozinho — nada a fazer

`chore(catalogo): carimbo da conferência semanal`

É a trilha de auditoria: `data/conferencia.json` mais o derivado, registrando **quando
cada tipo penal foi confrontado com a lei** e com que resultado. Vai direto para a `main`
porque não muda dado nenhum — só anota o que a máquina fez. Se este commit **não** aparecer
numa semana, a rodada falhou: vale abrir o log em Actions.

## 2. Uma issue — leitura, não ação imediata

Título: `Conferidor: achados de AAAA-MM-DD`, rótulo `conferidor`.

Ela só nasce quando há o que dizer, e reúne quatro blocos:

| Bloco | O que é | O que costuma exigir |
|---|---|---|
| **Achados de pena** | Moldura ou espécie de pena divergindo do compilado; dispositivo revogado; dispositivo com pena própria ausente do catálogo | Ler o artigo no Planalto. O que for mecânico já veio em PR (item 3); o resto é decisão de modelagem |
| **Cobertura** | Quantos registros foram conferidos, quantos não têm moldura própria, quantos não foram localizados | Nada, em regra. Se "não localizado" subir, é sinal de rótulo errado no catálogo ou de mudança na página |
| **Auditoria de classificação** | Hediondez, ação penal, causas de aumento ausentes e nomes suspeitos | Juízo jurídico. Hediondez e ação penal já vêm propostas em PR; aumentos e nomes ficam só aqui |
| **DOU da semana** | Atos normativos da Seção 1 que citam diploma monitorado ou trazem vocabulário penal | Ler a ementa. Se criar crime em diploma novo, o PR da semana já traz a entrada de `data/fontes.json` para conferir |

**Fechar a issue significa "triado"** — não "resolvido". O que virar tarefa vira commit ou
PR próprio.

## 3. Um pull request — é aqui que você decide

Um por rodada, um aberto por vez, autor `sispenas-automacao[bot]`, rótulo `conferidor`.
Ele **fecha uma versão**: sobe `package.json`, `CITATION.cff` e escreve a entrada de
changelog. Mergear publica a release.

Dois tipos, nesta ordem de prioridade:

**a) PR de pena** — `fix(catalogo): N correção(ões) em <diploma>`

Moldura ou espécie de pena de registro que já existe, divergindo do texto compilado. Um
diploma por PR. Cada mudança traz o trecho da lei ao lado. **É leitura de texto, não
juízo**: a revisão aqui é conferir se o trecho citado sustenta o número.

**b) PR de classificação** — `fix(catalogo): N ajuste(s) de hediondez e ação penal`

Só sai quando não há PR de pena pendente. **Este exige juízo jurídico**, e por isso vem
como proposta com o fundamento ao lado:

- **hediondez** — comparação com o rol do art. 1º da Lei 8.072/1990, transcrito em
  `data/hediondos.json`. Onde a lei condiciona a hediondez a circunstância do caso
  (grupo de extermínio, vítima criança, organização direcionada a crime hediondo), **nada
  é proposto** — a lei não decide pelo tipo;
- **ação penal** — fórmulas do próprio artigo ("somente se procede mediante
  representação"). Regra de ação penal que more em artigo de encerramento de capítulo ou
  em outro diploma não é alcançada;
- **fontes novas** — quando o DOU trouxe lei que parece criar tipo penal, a entrada
  proposta para `data/fontes.json` vem junto, para você corrigir em vez de escrever.

## O que a máquina NUNCA faz sozinha

- criar registro de tipo penal (a leva automática da v1.3.0 trouxe 29 que não eram crime);
- remover registro (decidir o destino do `id`, que é URL pública);
- transformar dispositivo em modificador, ou o contrário;
- mergear qualquer PR.

## O que fica esperando decisão sua, hoje

Registrado aqui para não se perder entre uma semana e outra. Ao resolver, tire da lista.

| Pendência | Onde | Por que depende de você |
|---|---|---|
| Hediondez dos crimes do **CPM** | `data/hediondos.json`, campo `fora_de_alcance` | O inciso VI do § único da Lei 8.072 declara hediondos os crimes militares "que apresentem identidade" com os do rol. Identidade é juízo de correspondência entre tipos; a tabela não resolve, e o catálogo hoje marca 7 tipos militares como hediondos |
| **Domínio social estruturado** (Lei 15.358/2026) | `data/hediondos.json`, campo `pendentes` | O inciso VIII remete ao "marco legal do combate ao crime organizado". Falta identificar o diploma, ver se o catálogo o registra e acrescentá-lo a `data/fontes.json` |
| **109 causas de aumento** presentes na lei e ausentes de `modificadores.json` | relatório de auditoria | Modelar exige decidir o escopo — sobre quais tipos o aumento incide —, e isso não se lê do dispositivo isolado |
| **13 nomes suspeitos** | relatório de auditoria | A heurística compara palavras; a decisão de renomear é de conteúdo. Pelo menos seis parecem erro real (o art. 338 do CP está com o nome da sonegação previdenciária, que é o art. 337-A) |
| Auditoria de **`tentativa`, `violencia` e `grave_ameaca`** | ainda não existe | Não há fonte textual que os declare: são qualificações doutrinárias do tipo. Precisaria de tabela curada, como a da hediondez |

## Quando algo falha

| Sintoma | Provável causa | O que fazer |
|---|---|---|
| A rodada falha em "Baixar os textos compilados" | Sentinela ausente: a página veio truncada ou de cache velho | Reexecutar. Se persistir, abrir a URL da fonte no navegador e conferir se o texto mudou de forma |
| A issue vem com muitos "não localizado" | Rótulo do catálogo apontando para dispositivo que não existe, ou mudança na numeração da lei | Conferir os ids listados contra o compilado |
| `ROL-ALTERADO` na auditoria de hediondez | O art. 1º da Lei 8.072 mudou | Reler o artigo, ajustar `data/hediondos.json` e regravar `impressao_do_texto` com o valor que o relatório informa |
| Nenhum PR, mesmo com achados | Não havia correção mecânica, ou já existe PR aberto do robô | Normal. Ver a issue |
