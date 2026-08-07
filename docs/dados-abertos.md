---
id: dados-abertos
title: Dados abertos
sidebar_position: 4
---

# Dados abertos

O catálogo completo é publicado como dado aberto em formato JSON:

- **Arquivo:** [`/data/crimes.json`](pathname:///sispenas/data/crimes.json)
- **Licença:** MIT com atribuição — cite como **"Equipe SISPENAS"**.

## Esquema de cada registro

```json
{
  "id": 1,
  "lei": "CP",
  "artigo": "Art. 121, caput",
  "crime": "Homicídio simples",
  "pena_min": 72,
  "pena_max": 240,
  "tipo_pena": "Reclusão",
  "acao": "Pública Incondicionada",
  "hediondo": "Não",
  "hediondo_condicao": null,
  "elemento": "Doloso",
  "tentativa": "Sim",
  "violencia": "Sim",
  "grave_ameaca": "Não",
  "obs": "Matar alguém. 6-20 anos reclusão",

  "pena_privativa": "Reclusão",
  "tem_multa": false,
  "multa_regime": "nenhuma",
  "derivado_auto": true,
  "pena_min_meses": 72,
  "pena_max_meses": 240,
  "pena_min_rotulo": "6 anos",
  "pena_max_rotulo": "20 anos",
  "pena_faixa_rotulo": "6 a 20 anos",
  "infracao_menor_potencial": false,

  "tem_pena_privativa": true,
  "sancoes_nao_privativas": [],
  "pena_por_remissao": null,
  "resultado_morte": true,
  "resultado_morte_derivado": true,
  "perdao_judicial_previsto": false,
  "chave_dispositivo": "cp|art. 121, caput",
  "duplicata": false,
  "duplicata_divergente": false,
  "duplicata_ids": []
}
```

Penas (`pena_min`, `pena_max`, `pena_*_meses`) estão em **meses** — o mês do art. 11 do
Código Penal tem 30 dias, então 0,5 são 15 dias. O primeiro bloco é a fonte redigida à
mão; os demais são calculados por `scripts/transform_data.py` a cada build.

## Para que serve cada campo

Nem todo campo tem o mesmo peso: alguns definem o que o sistema responde, outros
apenas descrevem. A tabela abaixo diz **onde cada um é usado**, para quem for reaproveitar
os dados saber o que pode mudar sem quebrar uma conta.

### Fonte — redigida à mão, é a autoridade

| Campo | Onde é usado |
|---|---|
| `id` | Endereço público do tipo (`/pesquisa/tipos?tipo=N`), citado em pareceres e trabalhos. **Nunca é reatribuído**: um id aposentado não volta a ser usado por outro crime. A numeração foi reiniciada duas vezes — v1.4.0 e v2.0.0 —, e é por isso que essas versões são MAIORES: quem tenha guardado um endereço anterior precisa refazê-lo. |
| `lei`, `artigo` | Identificam o dispositivo. Juntos formam a `chave_dispositivo`, que detecta registro repetido, e ligam a linha ao texto oficial conferido toda semana pelo conferidor. |
| `crime` | Nome exibido na busca. Também é dele — **e não do `obs`** — que se deduz o `resultado_morte`. |
| `pena_min`, `pena_max` | **A moldura.** Alimentam toda a dosimetria e todos os benefícios com limiar de pena (transação penal, ANPP, sursis, regime inicial, prescrição). Desde a v1.2.17 são a autoridade; antes disso a moldura era extraída do texto do `obs`, e uma frase secundária podia mudar a pena publicada. |
| `tipo_pena` | Reclusão, detenção, prisão simples, multa, morte (só nos crimes militares de tempo de guerra), "Outras penas" ou nenhuma. Define o regime inicial e distingue o tipo sem pena privativa. |
| `pena_por_remissao` | Opcional. O tipo **não comina moldura própria**: importa a de outro dispositivo, e este campo diz qual (`dispositivo_fonte`) e o que se faz com ela (`operador`: nenhum, aumento ou diminuicao; `fracao`). É o caso do art. 304 do CP — "a pena cominada à falsificação" — e do art. 315 do CPM. Quem o declara tem `pena_min` e `pena_max` zerados **de propósito**, e fica fora das estatísticas de alcance: a moldura depende de qual dispositivo-fonte incide no caso, e o catálogo não a inventa. |
| `acao` | Espécie de ação penal. Condiciona os institutos que dependem de representação ou de queixa. |
| `hediondo` | Fecha indulto, graça e comutação, e endurece as frações de progressão e livramento condicional. |
| `elemento` | Doloso, culposo ou preterdoloso. Crime culposo admite substituição por pena restritiva qualquer que seja a pena, e não admite tentativa. |
| `tentativa` | Habilita a redução do art. 14, II na terceira fase da dosimetria. |
| `violencia`, `grave_ameaca` | Vedam substituição por restritivas de direitos, ANPP e arrependimento posterior. |
| `vigencia_ate`, `vigencia_nota` | Opcionais. Data em que o dispositivo deixou de vigorar e o que houve — declaração de inconstitucionalidade com eficácia *ex nunc*, revogação —, com o dispositivo que passa a reger a conduta. O registro **não sai do catálogo**: fato anterior continua regido por ele, e uma consulta a 2024 precisa da lei de 2024. |
| `obs` | **Descritivo.** Observação de leitura humana — origem da redação, formas do artigo, remissões. Não define a pena; o que dele ainda se extrai é a presença e o regime da multa. |

### Derivados — recalculados a cada build, não edite

| Campo | Para que existe |
|---|---|
| `pena_min_meses`, `pena_max_meses` | Moldura canônica para cálculo. |
| `pena_min_rotulo`, `pena_max_rotulo`, `pena_faixa_rotulo` | Exibição na unidade natural: "15 dias a 3 meses", "2 a 5 anos", "até 5 anos". |
| `pena_privativa`, `tem_pena_privativa`, `sancoes_nao_privativas` | Separam o tipo com pena de prisão daquele cuja sanção é outra (art. 28 da Lei 11.343/06). |
| `tem_multa`, `multa_regime` | Multa cumulativa, alternativa ou isolada, lida do `obs`. |
| `infracao_menor_potencial` | Pena máxima até dois anos — porta de entrada da Lei 9.099/95. |
| `resultado_morte`, `resultado_morte_derivado` | Marcam o tipo com morte como resultado; o segundo avisa que veio de heurística sobre o **nome** do crime, sem revisão manual. |
| `perdao_judicial_previsto` | Só é `true` nas hipóteses expressamente previstas em lei — não há perdão judicial genérico. |
| `chave_dispositivo`, `duplicata`, `duplicata_divergente`, `duplicata_ids` | Detecção de registro repetido. `duplicata_divergente` marcaria o mesmo dispositivo com penas conflitantes; **hoje não há nenhum**. |
| `derivado_auto` | Marca o registro cujos campos passaram por preenchimento automático. |
| `hediondo_condicional`, `acao_condicional` | A classificação depende de circunstância do CASO, não do tipo: o texto da condição está em `hediondo_condicao` e `acao_condicao`, na fonte. Nesses registros o campo fica no padrão seguro, e a interface mostra a hipótese. |
| `vigente` | `false` quando o registro declara `vigencia_ate`. Deriva da presença do campo, não de uma comparação com a data de hoje: o arquivo derivado é publicado e conferido pela CI, e um campo que virasse sozinho num dia qualquer quebraria o build sem ninguém ter tocado em nada. |
| `fonte` | A página do texto compilado contra a qual este registro é conferido. |
| `conferido_em` | Data da última conferência deste registro contra a lei (AAAA-MM-DD). |
| `conferido_resultado` | `conferido` (a moldura bate), `sem_moldura_na_lei` (o dispositivo não traz moldura própria: pena por referência ou sanção não privativa), `divergente` (virou achado) ou `dispensado` (exceção já julgada). |

## De onde vem cada registro, e como ele é revisado

Um dado errado publicado é pior que um dado ausente. Esta seção explica, sem pressupor
conhecimento técnico, como um tipo penal chega ao catálogo e o que acontece com ele depois
— porque quem cita o dado precisa saber o que foi conferido, por quem, e o que não foi.

### A fonte é o texto compilado, não a lei publicada no dia

Uma lei penal quase nunca nasce sozinha: ela altera outra. O Código Penal de hoje é o
decreto-lei de 1940 mais oitenta anos de emendas. Por isso a fonte do catálogo não é o
texto original de cada lei, e sim o **texto compilado** do `planalto.gov.br`: a versão que
o próprio governo mantém atualizada, com a redação em vigor no corpo do artigo e, ao lado
de cada dispositivo, uma nota dizendo quem o incluiu, alterou ou revogou — "(Redação dada
pela Lei nº 14.994, de 2024)".

Ler o compilado é o que permite responder "qual é a pena **hoje**" sem reconstruir a
história da norma emenda por emenda.

### O ciclo semanal, em quatro passos

Toda segunda-feira, de madrugada, o repositório repete sozinho o mesmo procedimento:

1. **Baixar.** Busca a página compilada dos 63 diplomas que têm tipo penal no catálogo.
   Cada diploma tem uma **sentinela**: um trecho que comprovadamente existe na versão
   atual da página (em geral a emenda mais recente já incorporada). Se a sentinela não
   aparecer, a rodada falha em vez de continuar — é a proteção contra comparar o catálogo
   com uma cópia velha servida por engano.
2. **Ler.** Cada página é decomposta em dispositivos: artigo, parágrafo, o texto da
   conduta, a linha "Pena" e a situação (em vigor, revogado, vetado). Quando o mesmo
   dispositivo aparece em duas redações — o compilado costuma manter a antiga logo acima
   da nova —, vale a de nota mais recente.
3. **Comparar.** A pena lida na lei é confrontada com a publicada no catálogo, dispositivo
   a dispositivo. Divergiu, faltou, foi revogado: vira achado.
4. **Reportar.** Os achados viram uma **issue** no repositório, aberta ao público. Quando
   a divergência é de leitura direta — a moldura ou a espécie de pena de um registro que já
   existe não corresponde ao que a lei comina —, o sistema também abre um **pull request**
   com a correção proposta, citando o trecho da lei ao lado de cada mudança.

Nada disso usa inteligência artificial. É comparação de texto: as mesmas regras, aplicadas
do mesmo jeito, toda semana — e por isso qualquer pessoa pode repetir a rodada e obter o
mesmo resultado.

### O que a máquina decide e o que fica para uma pessoa

A máquina **nunca** publica sozinha. O pull request é uma proposta e depende de aprovação
humana, e o alcance dela é deliberadamente estreito: corrigir a pena de um registro
existente. Criar um registro novo, remover um registro ou reclassificar um dispositivo
continua sendo decisão de gente, porque exige julgamento jurídico — o mesmo texto pode ser
um crime autônomo, uma causa de aumento da pena de outro crime, ou nem uma coisa nem
outra. Quando a leitura automática não é segura, o achado vira pergunta na triagem da
semana, não dado publicado.

### O segundo olho: o Diário Oficial

Reler todas as semanas as leis que já conhecemos tem um ponto cego óbvio: uma **lei penal
inteiramente nova**, que ainda não está em nenhuma página vigiada. Para cobri-lo, a mesma
rodada semanal percorre os atos normativos da Seção 1 do Diário Oficial da União dos
últimos oito dias — leis, leis complementares, medidas provisórias — e separa os que citam
algum diploma do catálogo ou trazem vocabulário penal ("reclusão", "detenção", "pena de",
"revoga").

São cerca de cinco atos por semana, contra as centenas de portarias e despachos que o
Diário publica por dia e que não podem criar crime. O resultado é uma lista para ler, não
uma decisão: aparecer nela só significa que vale a pena abrir o texto. O filtro é
deliberadamente largo, porque um alarme falso custa dez segundos de leitura e uma lei nova
que passe despercebida custa meses de catálogo desatualizado.

### Cada registro diz quando foi conferido

Saber que existe conferência semanal não basta para quem cita um dado: é preciso saber
**deste** registro. Por isso cada tipo penal carrega três campos de auditoria — `fonte` (a
página oficial contra a qual ele é conferido), `conferido_em` (a data) e
`conferido_resultado` (se a moldura bateu, se o dispositivo não tem moldura própria, ou se
virou achado).

A trilha é produzida pela rodada semanal e vive em
[`/data/conferencia.json`](pathname:///sispenas/data/conferencia.json), fora do catálogo
editado à mão. Registro recém-criado, ainda não alcançado por uma rodada, tem os três
campos nulos — o que também é uma informação.

### O que ainda não é conferido automaticamente

Honestidade sobre o alcance, para quem for citar:

- a conferência automática cobre **pena, espécie de pena, existência e situação** do
  dispositivo;
- **hediondez** é comparada com o rol do art. 1º da Lei 8.072/1990, e **ação penal** com as
  fórmulas escritas no próprio artigo — mas onde a lei condiciona a classificação a
  circunstância do caso (homicídio por grupo de extermínio, organização direcionada a
  crime hediondo), a máquina não decide nem propõe;
- **causas de aumento** e **nome do tipo** só geram lista para leitura humana: modelar um
  aumento exige decidir sobre quais tipos ele incide, e comparar nomes é heurística;
- **tentativa, violência e grave ameaça** não têm fonte textual que os declare — são
  qualificações do tipo, revisadas à mão;
- o [relatório de qualidade](#relatório-de-qualidade) publica, a cada build, as
  contradições conhecidas e os `id` envolvidos.

## Relatório de qualidade

Cada regeneração emite [`/data/qualidade.json`](pathname:///sispenas/data/qualidade.json)
com o estado do catálogo — contagens, lacunas conhecidas e a lista completa das
contradições, com os `id` envolvidos. Use-o para saber o que é confiável antes de citar.

## Reprodutibilidade

Os campos derivados são gerados por `scripts/transform_data.py` a partir de
`data/crimes.json` (fonte), escrevendo o catálogo enriquecido em
`static/data/crimes.json`. O processo é determinístico: a mesma fonte produz sempre o
mesmo derivado, e a CI falha se o derivado commitado divergir da fonte.

## Estabilidade e versionamento

Os dados abertos são **API pública** para efeito de versionamento semântico: acrescentar
campo é MENOR, remover ou ressignificar campo é MAIOR. Ver
[Roadmap](/docs/roadmap#como-este-roadmap-usa-o-versionamento-semântico).

## Como citar

> Equipe SISPENAS. *SISPENAS — Sistema de Pesquisa de Tipos Penais e Benefícios*.
> Disponível em: https://github.com/amorim-rc/sispenas. Acesso em: [data].
