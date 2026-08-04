# Revisão pendente — catálogo de tipos penais brasileiro

Duas listas, e a diferença entre elas importa:

- **O que está respondido e falta aplicar** — a segunda rodada de revisão
  (03/08/2026) decidiu, e a versão 1.9.0 não alcançou. Não há pergunta aqui: há
  trabalho, com a resposta ao lado. Ninguém precisa reabrir o mérito.
- **O que continua em aberto** — as perguntas. Esta parte é **autossuficiente**:
  traz o texto legal de cada caso, o que o catálogo publica hoje e o que se quer
  decidir. Quem responde não precisa abrir o repositório.

## O que é este catálogo

Um catálogo aberto de **tipos penais brasileiros vigentes**: 1.417 registros, um
por conduta com pena própria. Ele alimenta o cálculo de **benefícios penais**
(transação, ANPP, sursis, regime inicial, progressão, livramento, prescrição) e a
**dosimetria pelas três fases** do art. 68 do Código Penal.

Ao lado dele há um **catálogo de modificadores**: agravantes, atenuantes e causas
de aumento e de diminuição, cada uma com a fração que aplica e o alcance sobre
que tipos incide. Causa de aumento **não** é tipo penal e não entra no catálogo
de tipos — é aplicada sobre ele no cálculo.

As penas são conferidas semanalmente contra o texto compilado oficial do
`planalto.gov.br`, e **não há divergência de pena pendente**.

---

# Parte I — respondido, falta aplicar

## A. Desdobrar por inciso os artigos que cominam no *caput*

**Resposta dada (grau A).** Desdobrar, com critério — e o critério não é "o
artigo tem incisos", é **conduta com pena própria e autonomia típica**. Teste de
três perguntas: o inciso descreve conduta completa, com verbo nuclear e objeto?
Pode ser praticado isoladamente? A prática de dois deles gera concurso de crimes?
Três "sim", registro próprio.

O artigo permanece como **agregador não computável** — visível na busca, com a
pena para referência, marcado como não aplicável em dosimetria e ligado aos
incisos. Nenhum endereço público quebra, e nenhuma dupla contagem acontece.

| Dispositivo | Registros novos |
|---|---|
| Estatuto da Pessoa Idosa, art. 100, II a V | 4 |
| Código Eleitoral, art. 313, parágrafo único (sujeito ativo distinto) | 1 |
| Lei 8.245/91, art. 44, I a IV | 4 |
| Lei 9.504/97, art. 72, I a III | 3 |
| Lei 9.605/98, art. 33, parágrafo único, I a III | 3 |
| Lei 9.279/96, art. 184, I e II | 2 |
| Lei 9.605/98, art. 68, parágrafo único — modalidade **culposa** com moldura própria (3 meses a 1 ano) | 1 |

Dezessete registros sobre 1.417 — pouco mais de 1%. O custo de **não** desdobrar
já está acontecendo: quem busca "negar emprego a pessoa idosa por motivo de
idade" não encontra nada, porque só o inciso I do art. 100 está cadastrado.

**Efeito colateral a tratar junto:** o id 399 (Lei 8.137/90, art. 2º, *caput*) foi
aposentado na v1.8.0 em vez de virar agregador. Restaurá-lo ao mesmo dispositivo
não viola a regra do id append-only — que proíbe reatribuir a **outro**
dispositivo — e deixa a convenção uniforme.

## B. Estatuto da Pessoa Idosa — padronizar a nomenclatura

**Resposta dada (grau A).** Sim, e para todo o diploma. A Lei 14.423/2022 alterou
a denominação oficial: "Estatuto do Idoso" deixou de ser o nome da lei. O nome do
tipo, no catálogo, é **rótulo editorial, não transcrição legal** — todos já são
paráfrase —, então construí-lo com a nomenclatura vigente não falseia nada. A
linha que não se atravessa: o **texto legal transcrito** preserva a letra.

Sugestão a implementar junto: manter "Estatuto do Idoso" como **alias de busca**,
para que quem procure pelo nome antigo continue encontrando.

**Aplicado na v1.9.0:** só os dois registros que a revisão citou nominalmente
(arts. 100, I e 101). Falta o resto do diploma e o alias.

## C. Multa cominada em índice extinto

**Resposta dada (grau A).** Publicar a **unidade original com ressalva**. Não
converter — a OTN foi extinta em 1989, não há critério legal de conversão, e
qualquer índice escolhido seria dado criado pelo catálogo. Não omitir — a multa
integra a cominação.

Modelagem proposta: multa em texto literal ("multa de 50 a 100 Obrigações do
Tesouro Nacional — OTN") com sinalizador `indice_extinto` e nota curta. O motor
de benefícios não perde nada: o que ele consome é a pena privativa.

Alcança a Lei 7.643/87 (OTN) e as cominações em **réis** da LCP ("multa de
duzentos mil réis a dois contos de réis"), que aparecem em vários registros.

## D. Lei 7.643/87 (cetáceos) — vigente

**Resposta dada (grau M).** Não houve derrogação pelo art. 29 da Lei 9.605/98.
Não há revogação expressa; a relação é de especialidade e a especial é a anterior
(LINDB, art. 2º, §2º); há condenações fundadas nos arts. 1º e 2º, e acórdãos que
se referem à lei como "especial mais gravosa"; a doutrina registra a vigência.

A desproporção da moldura é argumento de **inconstitucionalidade por excesso**,
não de revogação — registrar como nota, não como reserva de vigência.

**Falta:** acrescentar a nota da crítica ao registro. A vigência e o campo
`artigo` já estão como a resposta pede.

## E. Rádio clandestina — art. 151, §1º, IV do CP

**Resposta dada (grau M).** Não excluir e não publicar como plenamente vigente.
Duas décadas de jurisprudência sobre rádio clandestina litigam art. 70 da Lei
4.117/62 contra art. 183 da Lei 9.472/97; o art. 151, §1º, IV **não aparece**.
Para um tipo penal, sumir do contencioso da matéria que ele regula é evidência
forte de superação.

Marcar como **vigência controvertida — aplicação residual**, com nota informando
que a conduta é hoje processada pelo art. 183 da Lei 9.472/97.

**Por que a nota importa mais que a classificação:** pelo art. 151, §1º, IV a pena
é detenção de um a seis meses ou multa — menor potencial ofensivo, JECrim,
transação, prescrição em três anos. Pelo art. 183, detenção de dois a quatro anos
e multa, sem transação, na Justiça Federal. Quem calcule benefícios pelo
dispositivo do CP chega a um resultado radicalmente favorável e errado.

**Falta:** a marcação. Hoje o registro consta como plenamente vigente. Note que
`vigencia_ate` não serve — o dispositivo não deixou de vigorar em data certa; é
outra categoria.

## F. Tráfico militar — equiparado a hediondo

**Resposta dada (grau M).** Sim. O Plenário do **Superior Tribunal Militar**,
acolhendo recurso do MPM, reconheceu que a conduta do art. 290 do CPM
caracterizada como tráfico é equiparada a crime hediondo nos termos do art. 2º da
Lei 8.072/90, e por isso negou indulto.

A distinção em relação à conclusão da rodada anterior é limpa: o inciso VI do
parágrafo único do art. 1º projeta sobre o CPM os crimes "previstos no art. 1º" —
remissão a **dispositivo**, e o tráfico não está lá. Já a CF, art. 5º, XLIII e o
art. 2º da Lei 8.072 equiparam "o tráfico ilícito de entorpecentes" — designação
**pela conduta**, sem remissão a dispositivo algum, e nada nelas restringe o
alcance à legislação penal comum.

**Modelagem proposta:** `hediondez_rol` (inciso e dispositivo) + `equiparacao`
(fundamento e precedente) + derivado `tratamento_hediondo`, que é o que o motor
consome. Onde os dois eixos divergem: o §5º do art. 112 da LEP exclui o tráfico
privilegiado da condição de equiparado, e precisa saber por qual eixo o registro
entrou; e a auditabilidade é diferente — "hediondo porque o art. 1º, IV arrola o
art. 159" se confere contra o texto, "equiparado porque a conduta é tráfico" é
juízo e precisa carregar o precedente junto.

**Falta tudo:** hoje o art. 290, §5º consta como não hediondo.

## G. Pena por remissão de moldura

**Resposta dada (grau M).** Não são duas exceções documentáveis em nota — são um
padrão com **três famílias**, e o catálogo já tem instâncias das três:

- **(a) remissão com acréscimo** — "aplica-se a pena cominada a outro crime,
  aumentada de X": CP, art. 258, 4ª hipótese; CPM, art. 277, 4ª hipótese;
- **(b) remissão pura** — a pena do tipo é, por inteiro, a de outro dispositivo:
  Lei 9.434/97, art. 23-B, que remete às sanções do art. 10, XXIII da Lei
  6.437/77 — e essas são **administrativas sanitárias**, não pena criminal;
- **(c) remissão de regime a outro capítulo** — **CP, art. 285**: "Aplica-se o
  disposto no art. 258 aos crimes previstos neste Capítulo, salvo quanto ao
  definido no art. 267". Confirmado no compilado.

**Modelagem proposta:** campo `pena_por_remissao` com `{dispositivo_fonte,
operador (nenhum | aumento | diminuição), fração}`.

**Quanto à natureza da 4ª hipótese:** é **tipo qualificado pelo resultado com
moldura por remissão**. Não é majorante, porque não há pena sobre a qual incidir
— a base do crime de perigo comum é abandonada, não modificada. Não é concurso,
porque há unidade de conduta e o resultado é preterdoloso. O "aumentada de um
terço" é, esse sim, majorante, mas incide sobre a moldura **importada**.

**Correção imediata que decorre disso:** o alcance registrado dos três
modificadores do art. 258 está **incompleto** — o art. 285 os estende aos crimes
contra a saúde pública (arts. 267 a 285), salvo o art. 267.

## H. Roubo com arma de uso restrito — art. 157, §2º-B

**Resposta dada (grau M).** É **causa de aumento**. Qualificadora *comina* pena
própria; majorante *opera sobre pena alheia*, e o §2º-B usa a segunda fórmula,
remetendo expressamente ao *caput* — enquanto o §3º do mesmo artigo, que é
qualificadora, comina moldura própria. Topograficamente, o §2º-B vem logo após o
§2º-A, cuja natureza de majorante é pacífica, e os dois formam uma escala.

**O argumento decisivo na prática:** só na leitura de majorante fica disponível o
**art. 68, parágrafo único** — no concurso de causas de aumento da Parte
Especial, o juiz pode limitar-se a um só aumento. Em matéria de dúvida
interpretativa penal, prevalece a leitura que preserva essa faculdade.

**E a hediondez continua visível**, por uma modelagem que resolve mais que este
caso. O inciso II do rol arrola o §2º, V; o §2º-A, I; o §2º-B; e o §3º —
**nenhum deles é tipo penal autônomo**. O inciso não torna hediondo um crime:
torna hediondo *o roubo praticado em certas circunstâncias*. Campo
`hediondez_condicionada` no registro do art. 157, com uma entrada por condição, e
o motor liga a marcação quando o modificador correspondente é aplicado. O mesmo
mecanismo serve ao art. 121 (inciso I), ao art. 155 (§4º-A), ao art. 148 (§1º,
IV) e ao art. 149-A.

---

# Parte II — o que continua em aberto

## 1. Reincidente em crime do Título XII: 20% pelo inciso III, ou 1/6 pelo *caput*?

**Contexto.** A Lei 15.402/2026 deu ao art. 112 da Lei de Execução Penal esta
redação:

> **Art. 112.** …quando o preso tiver cumprido ao menos 1/6 (um sexto) da pena no
> regime anterior e seu mérito indicar a progressão, **observadas as seguintes
> exceções**:
>
> **I** – se o apenado for primário e for condenado pela prática de crime mediante
> o exercício de violência ou grave ameaça, **salvo em relação aos crimes previstos
> no Título XII da Parte Especial** do Código Penal, deverão ser cumpridos ao menos
> 25% da pena;
>
> **II** – se o apenado for reincidente e for condenado pela prática de crime
> mediante o exercício de violência ou grave ameaça, salvo em relação aos crimes
> previstos no Título XII da Parte Especial do Código Penal, deverão ser cumpridos
> ao menos 30% da pena;
>
> **III** – se o apenado for **reincidente em crime diverso dos crimes referidos
> nos incisos I e II** do *caput* deste artigo, deverão ser cumpridos ao menos 20%
> da pena;

**O que já foi decidido e aplicado.** O *caput* voltou a ser regra geral. Para o
**primário** condenado por crime do Título XII (arts. 359-A a 359-T, contra o
Estado Democrático de Direito) sobra o *caput*, por exclusão expressa dos incisos
I e II — leitura literal, sem controvérsia.

**Pergunta.** E o **reincidente** em crime do Título XII? Duas leituras:

1. **Inciso III, 20%** — ele alcança o "reincidente em crime diverso dos crimes
   referidos nos incisos I e II"; os do Título XII estão expressamente **fora** do
   alcance de I e II, logo são "diversos" deles. É a leitura mais fiel à letra:
   "referidos" é o que o dispositivo diz.
2. ***Caput*, 1/6 ≈ 16,67%** — "crimes referidos nos incisos I e II" significaria
   crimes praticados com violência ou grave ameaça, categoria a que os do Título
   XII pertencem materialmente, ainda que ressalvados. Não sendo "diversos", não
   caem no III e restam no *caput*. É a leitura mais fiel à finalidade da reforma.

**O que o sistema faz hoje.** Devolve o resultado como **condicional**, com as
duas leituras escritas e o cálculo pelo *caput*, que é o mais favorável. Nenhuma
foi escolhida em silêncio.

**O que falta ver.** Decisões de varas e tribunais de execução posteriores a maio
de 2026 sobre reincidente em crime do Título XII. É o único insumo que fecha a
questão.

## 2. Há registros cujo nome não corresponde a artigo nenhum?

**Contexto.** Uma verificação automática compara o nome de cada registro com o
texto do seu artigo e com o dos demais artigos do mesmo diploma. Nos treze casos
examinados na segunda rodada, todos os rótulos errados tinham vindo de **algum**
artigo real — menos um.

O art. 26 da Lei das Contravenções Penais publicava o nome "abrir valas ou
escavações que ponham em perigo a vida, a integridade física ou o patrimônio de
outrem, sem as devidas sinalizações". Esse texto **não corresponde a nenhum
artigo da LCP** — nem ao 26 (violação de lugar ou objeto), nem ao 62
(embriaguez), nem aos arts. 29 a 31, que tratam de perigo em construções e
animais. O nome foi corrigido; a pergunta que ele levanta, não.

**Pergunta.** Um rótulo sem origem legal identificável sugere que aquele registro
não foi extraído, e sim **redigido**. Quantos outros registros estão nessa
situação?

**O teste proposto:** rodar a verificação de similaridade não contra os artigos do
mesmo diploma, mas contra **todo** o acervo, e listar os registros cujo nome não
tem correspondente forte em lugar nenhum. Se o caso for isolado, ótimo. Se não
for, o problema é de **método de povoamento**, e vale mais que os treze casos da
segunda rodada somados.

**O que falta ver.** Nada de direito. É uma varredura a escrever, e a pergunta
para o revisor é se o resultado dela — uma lista de nomes sem fonte — deve virar
correção em massa ou triagem caso a caso.

## 3. Quais causas de aumento truncadas têm o alcance dependente dos incisos?

**Contexto.** Cerca de trinta causas de aumento foram cadastradas a partir de
dispositivos cujo texto vem cortado no ponto em que começam os incisos —
"*Aumenta-se a pena de 1/3 até metade se o crime é cometido:*", e a lista fica de
fora. Isso não impediu classificar natureza, fração e alcance, que é o que o
cálculo exige.

**O critério, já estabelecido.** Os incisos **restringem** o alcance quando
descrevem a quais condutas ou a quais parágrafos a causa se aplica; **não
restringem** quando descrevem circunstâncias do fato, do agente ou da vítima.
Três padrões, reconhecíveis pela fórmula introdutória:

- **"se o crime é cometido: [circunstâncias]"** → alcança o artigo inteiro;
- **"na hipótese do §X, aumenta-se…"** → alcance restrito ao parágrafo citado (já
  identificado: CP, art. 154-A, §4º);
- **"nos crimes previstos nos arts. X e Y…"** → lista explícita (já identificados:
  Lei 10.826/03, arts. 19 e 20; Lei 9.605/98, art. 53; Lei 13.260/16, art. 7º).

Os oito exemplos examinados — CP 121-A §2º, 147-A §1º, 149 §2º, 154-A §5º, 232-A
§2º, CPM 206 §1º, ECA 240 §2º, CE 323 §2º — trazem todos a fórmula do primeiro
padrão, o que sugere que nenhum restringe o alcance. Mas isso é inferência a
partir da fórmula, não leitura do texto.

**Um deles já foi conferido e está resolvido:** o CPM, art. 206, §1º não herda o
problema do art. 121, §4º do CP. Os dois incisos dele — inobservância de regra
técnica e omissão de socorro — são ambos do homicídio **culposo** militar, que é
o próprio art. 206. Não há duas regras com alcances distintos, e não há
desdobramento a fazer.

**Pergunta.** Nos demais, o alcance depende mesmo dos incisos?

**O que falta ver.** Uma varredura por referência interna nos incisos truncados,
procurando "§", "parágrafo", "art.", "inciso", "*caput*", "desta Lei". Um inciso
que mencione dispositivo é candidato a restringir alcance; um que só descreva
circunstância não é. Isso separa em minutos os que exigem leitura integral dos
que não exigem, e provavelmente reduz trinta casos a menos de cinco.

## 4. Pares de artigos com pena idêntica no mesmo diploma

**Contexto.** Quando dois artigos do mesmo diploma cominam a **mesma** pena,
trocar os nomes entre eles não produz divergência nenhuma para a conferência de
molduras: ela confere a pena do registro contra o artigo que o registro **diz**
ser. É o ponto cego que já produziu, e a lista de pares conhecidos cresce a cada
rodada:

- Lei 9.605/98, arts. 33 e 34 — detenção de 1 a 3 anos, ou multa, ou ambas;
- Lei 9.605/98, arts. 68 e 69 — detenção de 1 a 3 anos e multa;
- Estatuto da Pessoa Idosa, arts. 96 e 100 — reclusão de 6 meses a 1 ano e multa;
- Lei 9.279/96, arts. 184 e 190 — detenção de 1 a 3 meses ou multa;
- LCP, arts. 26 e 62 — prisão simples de 15 dias a 3 meses ou multa;
- Código Eleitoral, arts. 303 e 304 — pagamento de 250 a 300 dias-multa.

**O que já existe.** Uma verificação de nome que compara cada registro com os
demais artigos do mesmo diploma e acusa quando o rótulo conversa mais com outro
— foi ela que achou os arts. 68 e 69 da Lei 9.605.

**Pergunta.** Vale gerar a lista completa de pares de pena idêntica e conferir
todos os registros neles, mesmo os que a verificação de nome não acusa? Nos pares
acima, um dos dois artigos estava errado em quatro casos de seis.

**O que falta ver.** Nada de direito — é decisão de prioridade. A varredura é
barata; a leitura de cada par, não.
