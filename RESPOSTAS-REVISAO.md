> **ARQUIVO TEMPORÁRIO DE TRABALHO.** Respostas da revisão jurídica de 02/08/2026
> às perguntas que a conferência automática acumulou. Cada item traz um grau de
> confiança (A/M/B) — **B não vira dado publicado**. Ao aplicar tudo, exclua este
> arquivo; o registro permanente é o changelog e o `data/hediondos.json`.
>
> Estado da aplicação: **em curso**. Aplicado até agora: art. 112 da LEP (v1.7.1).

# Respostas à revisão pendente — catálogo de tipos penais brasileiro

Revisão dos cinco blocos de `REVISAO-PENDENTE.md`.
Data da revisão: 02/08/2026.

## Como ler este arquivo

Cada resposta traz um **grau de confiança**:

| Marca | Significado |
|---|---|
| **A** | Decidível pelo texto legal fornecido ou verificado. Pode ser aplicado ao catálogo após conferência de rotina. |
| **M** | Depende de leitura doutrinária defensável, ou de conferência contra o texto integral que não foi feita aqui. Aplicar com o fundamento registrado e a divergência anotada. |
| **B** | Questão aberta, sem resposta segura. **Não publicar como dado.** Registrar como pendência. |

Onde a resposta é **B**, digo exatamente o que falta ver.

---

## Achados que extrapolam as perguntas

Cinco coisas apareceram durante a revisão que não estavam sendo perguntadas e que
têm impacto maior que os blocos:

1. **A premissa "não há divergência de pena pendente" não se sustenta.** O caso 1.2
   (id 794, CE art. 313) publica reclusão de 2 a 6 anos para um artigo que comina
   apenas 90 a 120 dias-multa. A auditoria automática não pega isso porque confere
   a pena do registro contra o artigo que o **registro diz** ser — se o artigo de
   origem está trocado, a conferência valida o erro. Todo registro do Bloco 1 com
   nome incorreto precisa de reconferência de pena, e vale rodar a mesma suspeita
   sobre o catálogo inteiro.

2. **O § 3º do art. 232 do CPM foi declarado inconstitucional pelo STF** (ADI 7555,
   Rel. Min. Cármen Lúcia, Plenário, julgamento virtual encerrado em 29/08/2025,
   eficácia *ex nunc*). Não é caso de ajustar hediondez: o registro não deve constar
   como tipo vigente. Detalhes no Bloco 4.

3. **O § 3º do art. 2º da Lei 15.358/2026 foi vetado.** Tanto o art. 4º da própria
   lei quanto o novo inciso VIII do parágrafo único do art. 1º da Lei 8.072/1990
   declaram hediondos "o *caput* e os §§ 1º e 3º do art. 2º" — sendo que o § 3º
   não existe. Detalhes no Bloco 5.

4. **A Lei 15.358/2026 alterou o art. 112 da LEP** (percentuais de progressão:
   incisos V a VIII, com revogação do VI-A). Isso atinge o motor de progressão de
   regime do catálogo inteiro, não só os crimes novos. É a alteração de maior
   impacto sistêmico da lei.

5. **Oito dos dez dispositivos do CTB listados no Bloco 3 não são penais.** São
   infrações administrativas de trânsito. Detalhes no Bloco 3.

---

# Bloco 1 — O nome do tipo descreve este artigo?

`id | correto | nome proposto | fundamento`

### 1.1 — id 792 · CE art. 310 — **NÃO** — **A**

**Nome proposto:** Praticar, ou permitir membro da mesa receptora que se pratique,
irregularidade que determine a anulação de votação

**Fundamento:** o nome publicado ("Violar ou tentar violar o sigilo do voto") é a
conduta do art. 312 do Código Eleitoral, cuja pena é detenção até dois anos. O art.
310 pune conduta inteiramente diversa.

**Pena:** confere. Detenção até seis meses — coincide com o art. 310.

**Ressalva de completude:** a cominação do art. 310 é alternativa ("detenção até
seis meses **ou** pagamento de 90 a 120 dias-multa"). Se o campo *espécie de pena*
registra apenas detenção, a alternativa de multa isolada está sendo perdida, e ela
importa para transação penal e substituição.

### 1.2 — id 794 · CE art. 313 — **NÃO** (nome **e** pena) — **A**

**Nome proposto:** Deixar o juiz ou os membros da Junta de expedir o boletim de
apuração imediatamente após a apuração de cada urna

**Fundamento:** o nome publicado é a conduta do art. 348 do Código Eleitoral
(falsificação de documento público para fins eleitorais), cuja pena é reclusão de
2 a 6 anos e pagamento de 15 a 30 dias-multa. A pena publicada no registro é
exatamente essa. O art. 313 comina **apenas** pagamento de 90 a 120 dias-multa.

**Pena correta:** 90 a 120 dias-multa, sem pena privativa de liberdade.

**Consequência para o catálogo:** este é o registro mais grave do bloco. Um crime
apenado só com multa muda tudo a jusante — não há regime, não há progressão, não há
livramento, a prescrição corre pelo art. 114, I do CP, e a transação penal é
cabível de plano. Enquanto o registro publicar 2 a 6 anos de reclusão, todo cálculo
de benefício derivado dele está errado.

**Nota de granularização:** o parágrafo único estende a mesma pena ao presidente e
aos mesários, nas seções em que a contagem é feita pela mesa receptora. É sujeito
ativo distinto com pena própria — merece registro autônomo pela metodologia do
catálogo.

### 1.3 — id 750 · CP art. 338 — **NÃO** — **A**

**Nome proposto:** Reingresso de estrangeiro expulso

**Fundamento:** o próprio arquivo já registra a epígrafe oficial. O nome publicado
descreve o art. 337-A do CP (sonegação de contribuição previdenciária), cuja pena
é reclusão de 2 a 5 anos.

**Pena:** confere. Reclusão de 1 a 4 anos.

**Nota:** a Lei de Migração (Lei 13.445/2017) não revogou o art. 338 do CP. O tipo
segue vigente, com a ressalva legal de nova expulsão após o cumprimento da pena.

### 1.4 — id 474 · Lei 10.741/03 art. 100, I — **SIM** (falso alarme) — **A**

O nome publicado reproduz fielmente o inciso I. O alarme veio de o *caput* ser
norma de cominação ("Constitui crime punível com...") e as condutas estarem nos
incisos: o verificador comparou o nome contra o *caput*.

**Pena:** confere. Reclusão de 6 meses a 1 ano e multa.

**Duas observações de modelagem:**

- Se o registro é do inciso I, o campo *artigo* deveria ser `Art. 100, I` e não
  `Art. 100`. Hoje o registro ocupa o artigo genérico, o que vai colidir quando os
  incisos II a V forem cadastrados — e eles devem ser, porque cada um é conduta
  autônoma sob a mesma pena.
- O diploma foi renomeado para **Estatuto da Pessoa Idosa** pela Lei 14.423/2022.
  O próprio inciso III já usa "pessoa idosa". Vale padronizar a nomenclatura no
  campo *diploma* e nos nomes de tipo dessa lei.

### 1.5 — id 328 · Lei 11.343/06 art. 40 — **nome sim, modelagem não** — **A**

O nome descreve o dispositivo. O problema é outro: **o art. 40 não é tipo penal.**
É causa de aumento, e portanto pertence ao Bloco 3, não ao catálogo de tipos.

**Pena publicada (5 anos e 10 meses a 25 anos):** é uma pena calculada — 5 anos
+ 1/6, e 15 anos + 2/3. O cálculo embute a premissa de que a majorante incide só
sobre o art. 33, quando o *caput* diz "arts. 33 a 37". Publicada como pena de tipo,
ela aparece na busca como se existisse um crime com essa moldura, o que não existe.

**Recomendação:** mover para o catálogo de modificadores — fração 1/6 a 2/3,
alcance arts. 33 a 37 da Lei 11.343/06 — e remover a pena calculada.

**Novidade a cadastrar junto:** a Lei 15.358/2026 (art. 36) inseriu o **art. 40-A**
na Lei 11.343/06, aplicando as penas dos arts. 33 a 37 **em dobro** quando o crime
for praticado por integrante de organização criminosa ultraviolenta, grupo
paramilitar ou milícia privada, no contexto do art. 2º daquela lei. É outro
modificador, com fração fixa.

### 1.6 — id 411 · Lei 7.492/86 art. 10 — **NÃO** — **A**

**Nome proposto:** Inserir elemento falso ou omitir elemento exigido em
demonstrativos contábeis de instituição financeira, seguradora ou integrante do
sistema de distribuição de valores mobiliários

**Fundamento:** o nome publicado descreve o art. 17 da Lei 7.492/86 (empréstimo ou
adiantamento vedado a controlador, administrador etc.), cuja pena é reclusão de
2 a 6 anos e multa.

**Pena:** confere. Reclusão de 1 a 5 anos e multa — é a do art. 10.

### 1.7 — id 917 · Lei 7.643/87 art. 2º — **questão de modelagem** — **M**

Não é erro de conteúdo. A Lei 7.643/87 separa proibição e sanção: o **art. 1º**
proíbe a pesca e o molestamento intencional de cetáceos em águas jurisdicionais
brasileiras; o **art. 2º** é a norma sancionadora ("a infração ao disposto nesta
lei será punida com..."). O nome descreve a conduta, que está no art. 1º; a pena
está no art. 2º.

**Recomendação:** registrar o artigo como `Art. 1º c/c Art. 2º`, que é o que a
doutrina faz, em vez de atribuir a conduta ao artigo que só comina.

**Dois pontos abertos — B:**

- A multa está expressa em OTN, extinta. O catálogo precisa decidir como exibir
  cominações pecuniárias em índices revogados. Não é questão jurídica, é de
  apresentação, mas afeta o campo *espécie de pena*.
- Há corrente sustentando que o art. 29 da Lei 9.605/98 derrogou a Lei 7.643/87
  nesse ponto, e corrente sustentando a especialidade da lei anterior. Não afirmo
  vigência nem revogação sem levantamento de jurisprudência. **Registrar como
  pendência de vigência**, não como resposta.

### 1.8 — id 399 · Lei 8.137/90 art. 2º (*caput*) — **problema estrutural** — **A**

O *caput* do art. 2º não descreve conduta — diz apenas "Constitui crime da mesma
natureza:" e comina a pena. As condutas estão nos incisos I a V. Um registro
`art. 2º, caput` sem inciso **não corresponde a nenhuma conduta punível autônoma**,
e como os incisos I e II já estão cadastrados (ids 670 e 671), este id é uma
duplicata estrutural que soma pena ao catálogo sem tipo por trás.

O nome publicado ("Sonegação fiscal formal — condutas que dificultam a
fiscalização, sem exigir resultado") é uma descrição doutrinária do conjunto do
artigo, e a rigor é imprecisa: o inciso I exige fraude para eximir-se do
pagamento, o que não é conduta meramente formal.

**Recomendação — uma das duas:**

- converter o id 399 em registro guarda-chuva, não computável na dosimetria; ou
- desdobrá-lo nos incisos **III, IV e V**, que faltam e são condutas autônomas com
  a mesma pena.

A segunda é mais coerente com a metodologia do catálogo.

### 1.9 — id 670 · Lei 8.137/90 art. 2º, I — **SIM** — **A**

Nome fiel ao inciso. Pena confere (detenção de 6 meses a 2 anos e multa).

### 1.10 — id 671 · Lei 8.137/90 art. 2º, II — **SIM** — **A**

Nome fiel ao inciso. Pena confere.

**Nota jurisprudencial (M):** o STF, no RHC 163.334/SC, fixou que o contribuinte
que deixa de recolher ICMS próprio declarado, de forma contumaz e com dolo de
apropriação, incide neste inciso. Se o catálogo tiver campo de notas, é a
informação mais consultada sobre este tipo.

### 1.11 — id 550 · Lei 8.245/91 art. 44 — **NÃO** — **A**

**Fundamento:** "cobrar antecipadamente o aluguel" é conduta do **art. 43, III** da
Lei do Inquilinato — que é **contravenção penal**, punida com prisão simples de
cinco dias a seis meses ou multa. O art. 44 é crime de ação pública com detenção de
três meses a um ano, e seus quatro incisos tratam de outras condutas.

**Pena:** confere com o art. 44 (detenção de 3 meses a 1 ano). Aqui só o nome está
errado — mas note que o nome errado vem de um dispositivo de **espécie diversa**
(contravenção, prisão simples), o que é sinal de que a origem do registro foi
outro artigo.

**Nome proposto:** o ideal é desdobrar em quatro registros (incisos I a IV), já que
cada inciso é conduta autônoma sob a mesma pena. Se mantido registro único:
"Crimes contra a locação — condutas do art. 44 da Lei 8.245/91".

**Nota:** o art. 44 traz substituição por prestação de serviços à comunidade já na
própria cominação — se o catálogo modela substituição, é dado a capturar.

### 1.12 — id 537 · Lei 9.504/97 art. 72 — **NÃO** — **A**

**Fundamento:** o art. 72 não trata do Cadastro Nacional de Eleitores. Trata de
(I) obter acesso a sistema de tratamento automático de dados do serviço eleitoral
para alterar apuração ou contagem; (II) desenvolver ou introduzir comando ou
programa capaz de destruir, alterar ou transmitir dados; (III) causar dano físico
ao equipamento de votação ou totalização.

**Pena:** confere. Reclusão de 5 a 10 anos.

**Nome proposto:** "Crimes contra o sistema eletrônico de votação e apuração" —
ou, preferencialmente, desdobrar nos três incisos.

**Sobre a origem do nome errado (M):** o rótulo lembra a descrição do art. 313-A do
CP (inserção de dados falsos em sistema de informações da Administração), mas não
afirmo a origem sem conferir. O que é seguro é que o nome não descreve o art. 72.

### 1.13 — id 355 · Lei 9.605/98 art. 33 — **NÃO** — **A**

**Nome proposto:** Provocar o perecimento de espécimes da fauna aquática por emissão
de efluentes ou carreamento de materiais

**Fundamento:** "pesca em período ou local proibido" é o **art. 34** da Lei
9.605/98.

**Pena:** confere — **e é justamente esse o problema.** Os arts. 33 e 34 têm penas
*idênticas* (detenção de um a três anos, ou multa, ou ambas cumulativamente). A
auditoria de pena é estruturalmente cega a essa troca. Se houver outros pares de
artigos com cominação idêntica no mesmo diploma, eles são o ponto cego da
auditoria e merecem varredura dirigida.

**Nota:** o parágrafo único traz três condutas equiparadas (incisos I a III) com a
mesma pena — condutas autônomas, candidatas a registro próprio.

---

## Resumo do Bloco 1

| id | artigo | nome correto? | pena correta? |
|---|---|---|---|
| 792 | CE 310 | não | sim (espécie incompleta) |
| 794 | CE 313 | **não** | **não** |
| 750 | CP 338 | não | sim |
| 474 | Idoso 100, I | sim | sim |
| 328 | 11.343 art. 40 | sim, mas não é tipo | pena calculada, remover |
| 411 | 7.492 art. 10 | não | sim |
| 917 | 7.643 art. 2º | modelagem | sim |
| 399 | 8.137 art. 2º | duplicata estrutural | sim |
| 670 | 8.137 art. 2º, I | sim | sim |
| 671 | 8.137 art. 2º, II | sim | sim |
| 550 | 8.245 art. 44 | não | sim |
| 537 | 9.504 art. 72 | não | sim |
| 355 | 9.605 art. 33 | não | sim |

Nove nomes a corrigir, uma pena a corrigir, dois registros a reclassificar.

---

# Bloco 2 — Espécie de ação penal

## Art. 151 do CP — a regra

O § 4º é exaustivo: *"Somente se procede mediante representação, salvo nos casos do
§ 1º, IV, e do § 3º."* Logo a representação é a regra do artigo, e a
incondicionalidade é exceção nominada em duas hipóteses. Tudo o que não está na
ressalva é condicionado.

| id | dispositivo | espécie | publicado hoje | status |
|---|---|---|---|---|
| 76 | CP 151, *caput* | **pública condicionada a representação** | incondicionada | corrigir |
| 1351 | CP 151, § 3º | **pública incondicionada** | incondicionada | manter |
| 77 | CP 151, § 1º, I | **pública condicionada a representação** | incondicionada | corrigir |
| 78 | CP 151, § 1º, II | **pública condicionada a representação** | incondicionada | corrigir |
| 646 | CP 151, § 1º, III | **pública condicionada a representação** | incondicionada | corrigir |
| 647 | CP 151, § 1º, IV | **pública incondicionada** | incondicionada | manter |

**Fundamento de todas:** art. 151, § 4º do CP, a contrario e conforme a ressalva.
Confiança **A** — a leitura é literal e não comporta divergência.

Quatro dos seis registros estão errados hoje, e todos erram no mesmo sentido:
publicam incondicionada onde a lei exige representação. Isso tem efeito prático
direto — em crime de ação condicionada, a decadência do direito de representação
(seis meses, art. 38 do CPP) extingue a punibilidade, e o catálogo hoje não sinaliza
esse prazo.

### Ponto aberto sobre o id 647 — **B**

Há corrente relevante sustentando que o art. 151, § 1º, IV do CP foi **tacitamente
revogado** pelo art. 183 da Lei 9.472/97, que pune o desenvolvimento clandestino de
atividades de telecomunicação com detenção de dois a quatro anos. Se acolhida, o
registro deveria ser marcado como revogado, e não apenas ter sua ação penal
ajustada. Não decido isso aqui: exige levantamento da jurisprudência atual do STJ
sobre rádio clandestina, que não fiz. **Registrar como pendência de vigência.**

## Art. 153 do CP

### 2.7 — id 79 · CP art. 153, *caput* — **pública condicionada a representação** — **A**

Publicado hoje como **ação penal privada** — está errado. O § 1º (antigo parágrafo
único, renumerado pela Lei 9.983/2000) diz expressamente "somente se procede
mediante representação". Representação é ação pública condicionada; queixa é ação
privada. São institutos distintos, com prazos e titularidade diferentes.

### 2.8 — id 80 · CP art. 153, § 1º-A — **DEPENDE** — **M**

**Condição a registrar:** pública incondicionada quando resultar prejuízo para a
Administração Pública; nos demais casos, pública condicionada a representação.

**Fundamento:** § 2º do art. 153, inserido pela Lei 9.983/2000 junto com o § 1º-A.

**Por que "depende" e não "incondicionada":** o § 2º só tem sentido útil se, na
ausência de prejuízo, a ação não for incondicionada. Ler o § 1º-A como sempre
incondicionado esvazia o § 2º, o que viola o cânone de que a lei não contém
palavras inúteis.

**Divergência a registrar junto:** há corrente sustentando que o § 1º-A é sempre
pública incondicionada, porque o bem jurídico é a Administração e não haveria
ofendido individualizado apto a representar. O argumento é forte na prática, mas
não vence a literalidade do § 2º. Como o catálogo sabe guardar classificação
circunstanciada, este é exatamente o caso de guardar a condição em texto em vez de
afirmar uma espécie.

### 2.9 — id 285 · CP art. 345 — **DEPENDE** — **A**

**Condição a registrar:** se **não** há emprego de violência, ação penal privada
(queixa); **se há** emprego de violência, ação pública incondicionada.

**Fundamento:** parágrafo único do art. 345 do CP, a contrario.

O registro atual ("privada") descreve só metade do artigo. E a hipótese com
violência é a que mais aparece na prática, além de acumular a pena correspondente à
violência — o que também importa para o concurso.

---

# Bloco 3 — Causas de aumento e diminuição (109 dispositivos)

## Notas gerais que valem para todo o bloco

**Sobre alcance.** Salvo indicação em contrário, a causa incide sobre as condutas
do **próprio artigo** em que está inserida. Marquei explicitamente os casos em que o
alcance é o capítulo, a seção, a lei inteira ou uma lista de artigos — que são a
minoria, mas são justamente os que a máquina não conseguiria inferir.

**Sobre frações abertas.** Três formulações não têm mínimo determinado: "até o
dobro", "até o triplo", "em até um terço". Registrei a fração máxima e marquei o
mínimo como aberto. O catálogo precisa decidir se representa isso como `0 → x` ou
como fração de teto — a escolha muda o cálculo do piso da pena majorada, e hoje não
há resposta legal para o mínimo (a doutrina resolve pela menor fração compatível
com a individualização).

**Sobre dispositivos truncados.** Cerca de trinta entradas vieram cortadas no ponto
em que começam os incisos ("se o crime é cometido:"). Isso não impede classificar
natureza, fração e alcance — que é o que o bloco pede — mas impede descrever as
hipóteses. Onde a hipótese importa para o alcance, marquei **B**.

### 3.cp — Código Penal (41)

| Dispositivo | Natureza | Fração | Alcance | Nota |
|---|---|---|---|---|
| 121-A, § 2º | aumento | 1/3 a 1/2 | art. 121-A | incisos truncados |
| 121-B, p.ú. | aumento | 1/3 a 1/2 | art. 121-B | incisos truncados |
| 121, § 4º | aumento | 1/3 | **duas regras distintas** | ver abaixo |
| 121, § 6º | aumento | 1/3 a 1/2 | art. 121, todas as formas | milícia ou grupo de extermínio |
| 122, § 4º | aumento | até o dobro (mín. aberto) | art. 122 | hipótese do inciso X do rol de hediondos |
| 132, p.ú. | aumento | 1/6 a 1/3 | art. 132 | transporte de trabalhadores |
| 135, p.ú. | aumento | **metade** (lesão grave) / **triplo** (morte) | art. 135 | frações fixas; desdobrar em dois |
| 135-A, p.ú. | aumento | **até o dobro** (lesão grave) / **até o triplo** (morte) | art. 135-A | frações de teto; desdobrar em dois |
| 136, § 3º | aumento | 1/3 | art. 136, *caput* e §§ 1º e 2º | vítima menor de 14 |
| 147-A, § 1º | aumento | metade | art. 147-A | incisos truncados |
| 147-B, p.ú. | aumento | metade | art. 147-B | uso de IA ou recurso que altere imagem/som |
| 149, § 2º | aumento | metade | art. 149 | incisos truncados |
| 149-A, § 1º | aumento | 1/3 a 1/2 | art. 149-A | incisos truncados |
| 149-A, § 2º | **diminuição** | 1/3 a 2/3 | art. 149-A | agente primário sem vínculo com orgcrim |
| 154-A, § 2º | aumento | 1/3 a 2/3 | art. 154-A, *caput* | prejuízo econômico |
| 154-A, § 4º | aumento | 1/3 a 2/3 | **só a hipótese do § 3º** | alcance restrito, não o artigo todo |
| 154-A, § 5º | aumento | 1/3 a 1/2 | art. 154-A | incisos truncados (qualidade da vítima) |
| 157, § 2º-B | aumento (controverso) | **dobro** | art. 157, *caput* | ver abaixo |
| 168, § 1º | aumento | 1/3 | art. 168, *caput* | incisos truncados |
| 203, § 2º | aumento | 1/6 a 1/3 | art. 203, *caput* e § 1º | |
| 207, § 2º | aumento | 1/6 a 1/3 | art. 207, *caput* e § 1º | |
| 208, p.ú. | aumento | 1/3 | art. 208 | cumulativa com a pena da violência |
| 209, p.ú. | aumento | 1/3 | art. 209 | cumulativa com a pena da violência |
| 216-A, § 2º | aumento | **em até 1/3** (mín. aberto) | art. 216-A | |
| 218-C, § 1º | aumento | 1/3 a 2/3 | art. 218-C | |
| 232-A, § 2º | aumento | 1/6 a 1/3 | art. 232-A | incisos truncados |
| 258 | **misto** | ver abaixo | **arts. 250 a 259 (Cap. I do Tít. VIII)** | alcance de capítulo |
| 268, p.ú. | aumento | 1/3 | art. 268 | qualidade do agente |
| 311, § 1º | aumento | 1/3 | art. 311 | |
| 311-A, § 3º | aumento | 1/3 | art. 311-A | agente funcionário público |
| 317, § 1º | aumento | 1/3 | art. 317, *caput* | |
| 332, p.ú. | aumento | metade | art. 332 | |
| 333, p.ú. | aumento | 1/3 | art. 333 | |
| 334, § 3º | aumento | dobro | art. 334 | transporte aéreo, marítimo ou fluvial |
| 334-A, § 3º | aumento | dobro | art. 334-A | idem |
| 337-B, p.ú. | aumento | 1/3 | art. 337-B | |
| 337-C, p.ú. | aumento | metade | art. 337-C | |
| 337-O, § 2º | aumento | dobro | art. 337-O, *caput* | |
| 339, § 2º | **diminuição** | metade | art. 339 | imputação de contravenção |
| 359-I, § 1º | aumento | metade **até o dobro** | art. 359-I, *caput* | |
| 359-M ("B.") | **diminuição** | 1/3 a 2/3 | **todos os crimes do Capítulo** | ver abaixo — **B** |

**Art. 121, § 4º — desdobrar em dois registros.** O parágrafo comporta duas causas
distintas, com alcances diferentes: (a) **homicídio culposo** — aumento de 1/3 por
inobservância de regra técnica, omissão de socorro ou fuga, alcance art. 121, § 3º;
(b) **homicídio doloso** — aumento de 1/3 se praticado contra pessoa menor de 14
anos ou maior de 60, alcance art. 121, *caput* e § 2º. Um registro único faz o motor
de dosimetria aplicar a majorante culposa a homicídio doloso e vice-versa.

**Art. 157, § 2º-B — classificação controversa (M).** Literalmente, manda aplicar
em dobro a pena do *caput*, o que é operação de terceira fase. Parte da doutrina o
trata como qualificadora, porque o efeito prático é criar moldura própria. Sugiro
registrar como **aumento de fração fixa (dobro) sobre o art. 157, *caput***, e
anotar a divergência, porque a diferença só aparece na ordem de aplicação com
outras causas. É hediondo pelo art. 1º, II, "b" da Lei 8.072/90.

**Art. 258 — não é uma causa só (M).** Comporta quatro hipóteses, e a quarta não é
majoração:

1. crime doloso de perigo comum + lesão grave → aumento de metade;
2. crime doloso + morte → pena em dobro;
3. crime culposo + lesão corporal → aumento de metade;
4. crime culposo + morte → **aplica-se a pena do homicídio culposo aumentada de
   1/3** — isto é substituição da moldura, não majoração da pena do tipo.

Recomendo três registros de aumento e um registro de natureza "outro — substituição
de moldura". Alcance de todas: os crimes de perigo comum do Capítulo I do Título
VIII (arts. 250 a 259).

**Art. 359-M — o identificador está quebrado (B).** O texto vem como
`Art. 359-M — B. Quando os crimes previstos neste Capítulo...`. Esse "B." isolado
no início do conteúdo é forte indício de que o dispositivo real é o
**art. 359-M-B**, e que o extrator quebrou o identificador ao separar a letra do
número. Não aplicar sem conferir a designação no compilado. O conteúdo — diminuição
de 1/3 a 2/3 em contexto de multidão, desde que o agente não tenha financiado nem
liderado — está claro; o rótulo do dispositivo, não.

### 3.cpm — Código Penal Militar (18)

| Dispositivo | Natureza | Fração | Alcance | Nota |
|---|---|---|---|---|
| 160, p.ú. | aumento | metade | art. 160 | vítima qualificada |
| 162, p.ú. | aumento | metade | art. 162 | fato diante da tropa ou em público |
| 190, § 3º | aumento | **1/3** (sargento, subtenente, suboficial) / **metade** (oficial) | art. 190 | duas frações fixas por posto; desdobrar |
| 196, § 2º | aumento | metade | art. 196 | agente em função de comando |
| 206, § 1º | aumento | 1/3 | art. 206 | incisos truncados |
| 206, § 2º | aumento | 1/6 a 1/2 | art. 206 | pluralidade de vítimas |
| 207, § 3º | **diminuição** | 1/3 a 2/3 | art. 207 | tentativa com lesão grave |
| 210, § 1º | aumento | 1/3 | art. 210 | |
| 210, § 2º | aumento | 1/6 a 1/2 | art. 210 | pluralidade de vítimas |
| 213, § 3º | aumento | 1/3 | art. 213 | vítima menor de 14, maior de 60 ou com deficiência |
| 226, § 2º | aumento | 1/3 | art. 226 | |
| 241, p.ú. | aumento | **metade** (veículo, embarcação, aeronave, arma) / **1/3** (animal de sela ou tiro) | art. 241 | duas frações fixas; desdobrar |
| 263, § 1º | aumento | metade (lesão grave) / dobro (morte) | **os crimes de dano do capítulo** — **B** | ver abaixo |
| 267, § 2º | aumento | 1/3 | art. 267 | agente superior ou servidor público |
| 277 | **misto** | mesma estrutura do art. 258 do CP | crimes de perigo comum do CPM — **B** | ver abaixo |
| 290, § 4º | aumento | metade | art. 290, *caput* | militar em serviço |
| 308, § 1º | aumento | 1/3 | art. 308 | |
| 336, p.ú. | aumento | metade | art. 336 | |

**Arts. 263, § 1º e 277 (B).** Ambos usam a fórmula "a pena correspondente é
aumentada", que remete a um conjunto de artigos anteriores sem nomeá-los. Determinar
o alcance exige ver a estrutura do capítulo no texto integral do CPM, que não
conferi. A natureza (aumento pelo resultado) e as frações são seguras; o alcance
não. O art. 277 tem a mesma quarta hipótese do art. 258 do CP — substituição de
moldura pela pena do homicídio culposo aumentada de 1/3, que não é majoração.

### 3.ctb — Código de Trânsito Brasileiro (10)

**Oito destes dez não pertencem a este catálogo — A.**

| Dispositivo | Natureza | Nota |
|---|---|---|
| 165, p.ú. | **não é causa de aumento penal** | multa administrativa em dobro por reincidência |
| 165-A, p.ú. | **não é causa de aumento penal** | idem |
| 173, p.ú. | **não é causa de aumento penal** | idem |
| 174, § 2º | **não é causa de aumento penal** | idem |
| 175, p.ú. | **não é causa de aumento penal** | idem |
| 191, p.ú. | **não é causa de aumento penal** | idem |
| 203, p.ú. | **não é causa de aumento penal** | idem |
| 253-A, § 2º | **não é causa de aumento penal** | idem |
| 302, § 1º | aumento — 1/3 a 1/2 — art. 302, *caput* | incisos truncados |
| 303, § 1º | aumento — 1/3 a 1/2 — art. 303, *caput* | por remissão às hipóteses do art. 302, § 1º |

Os oito primeiros estão no capítulo de **infrações administrativas de trânsito**,
não no capítulo dos crimes de trânsito. "Aplica-se em dobro a multa prevista no
*caput*" refere-se à multa administrativa, cobrada pelo órgão de trânsito, e a
"reincidência no período de 12 meses" é reincidência administrativa — conceito que
não guarda relação com a reincidência penal do art. 63 do CP. Nada disso entra na
terceira fase da dosimetria do art. 68.

**Como isso entrou:** provavelmente porque o extrator buscou o padrão "aplica-se em
dobro a multa" sem distinguir multa penal de multa administrativa. Vale checar se
outros diplomas com parte administrativa (Lei 9.605/98, Estatuto da Pessoa Idosa,
Lei 13.146/15) trouxeram o mesmo falso positivo.

**Nota sobre o art. 302 (M):** o § 3º do art. 302 (condução sob influência de álcool
ou substância psicoativa) tem **pena própria** — reclusão de 5 a 8 anos — e é figura
qualificada, não majorante. Conferir se o catálogo já a registra como tipo autônomo;
se estiver como causa de aumento, está errada.

### 3.ambiental-9605 — Lei 9.605/98 (10)

| Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|
| 29, § 4º | aumento | metade | art. 29, *caput* e § 1º — incisos truncados |
| 29, § 5º | aumento | **até o triplo** (mín. aberto) | art. 29 — caça profissional |
| 32, § 2º | aumento | 1/6 a 1/3 | art. 32, *caput* e § 1º-A |
| 53 | aumento | 1/6 a 1/3 | **todos os crimes da Seção (crimes contra a flora)** — incisos truncados |
| 56, § 2º | aumento | 1/6 a 1/3 | art. 56, *caput* e § 1º |
| 69-A, § 2º | aumento | 1/3 a 2/3 | art. 69-A, *caput* |
| 38, p.ú. | **não é causa de diminuição** | — | ver abaixo |
| 38-A, p.ú. | **não é causa de diminuição** | — | ver abaixo |
| 40, § 3º | **não é causa de diminuição** | — | ver abaixo |
| 40-A, § 3º | **não é causa de diminuição** | — | ver abaixo |

**Os quatro dispositivos "se o crime for culposo, a pena será reduzida à metade"
(M).** Tecnicamente não são causas de diminuição de terceira fase: a culpa é
**elemento do tipo**, não circunstância do fato. O que a lei faz é criar modalidade
culposa derivada com moldura própria (metade da dolosa). Como o catálogo já tem
campo *elemento (doloso/culposo)* e a metodologia é registrar cada conduta com pena
própria, o modelo correto é **tipo culposo autônomo** com pena = metade da dolosa,
não modificador. Registrar como diminuição faria o motor aplicar a redução depois
das demais causas, quando na verdade ela define a moldura de partida.

O mesmo raciocínio vale, fora deste bloco, para qualquer "se culposo, reduz-se"
em outros diplomas.

### 3.lcp — Lei das Contravenções Penais (4)

| Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|
| 19, § 1º | aumento | 1/3 até metade | art. 19 — **ver ressalva de vigência** |
| 21, p.ú. | aumento | 1/3 até metade | art. 21 — **duplicata** |
| 21, § 1º | aumento | 1/3 até metade | art. 21 — **duplicata** |
| 50, § 1º | aumento | 1/3 | art. 50 — jogo de azar |

**Art. 19 — ressalva de vigência (M).** O art. 19 da LCP (porte de arma) está
tacitamente revogado quanto a **arma de fogo** pela Lei 10.826/2003, subsistindo
apenas para armas brancas e outros instrumentos. Se o catálogo publica o art. 19
como vigente sem essa qualificação, o registro está incompleto — e o § 1º herda o
problema.

**Art. 21 — duplicata (A).** As duas entradas têm texto rigorosamente idêntico. É
artefato de renumeração no compilado: o antigo parágrafo único foi convertido em
§ 1º, e o extrator capturou as duas redações empilhadas. Manter **um só** registro,
com a designação vigente.

### 3.ce — Código Eleitoral (3)

| Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|
| 323, § 2º | aumento | 1/3 até metade | art. 323 — incisos truncados |
| 326-A, § 2º | **diminuição** | metade | art. 326-A — imputação de contravenção |
| 326-B, p.ú. | aumento | 1/3 | art. 326-B — incisos truncados |

O art. 326-A, § 2º é o espelho eleitoral do art. 339, § 2º do CP. Mesma estrutura,
mesma fração.

### 3.eca — Estatuto da Criança e do Adolescente (3)

| Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|
| 240, § 2º | aumento | 1/3 | art. 240, *caput* e § 1º — incisos truncados |
| 241-B, § 1º | **diminuição** | **1/3 a 2/3** | art. 241-B, *caput* — ver nota |
| 243, p.ú. | aumento | 1/3 até metade | art. 243 |

**Art. 241-B, § 1º — nota de redação (A).** O compilado traz "diminuída de 1 (um) a
2/3 (dois terços)", o que lido literalmente seria "reduzida em 100% a 66%" —
absurdo, porque zeraria a pena. É defeito de redação conhecido: lê-se "de um
[terço] a dois terços". Registrar **1/3 a 2/3** e anotar a divergência entre a letra
e a leitura corrente, para que a auditoria automática não "corrija" de volta.

### 3.pcd-13146 — Lei Brasileira de Inclusão (3)

| Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|
| 88, § 1º | aumento | 1/3 | art. 88, *caput* |
| 89, p.ú. | aumento | 1/3 | art. 89, *caput* — incisos truncados |
| 91, p.ú. | aumento | 1/3 | art. 91, *caput* |

### 3.idoso-10741 — Estatuto da Pessoa Idosa (2)

| Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|
| 96, § 2º | aumento | 1/3 | art. 96, *caput* e § 1º |
| 97, p.ú. | aumento | **metade** (lesão grave) / **triplo** (morte) | art. 97 — desdobrar em dois |

O art. 97, p.ú. é cópia estrutural do art. 135, p.ú. do CP — frações fixas, não de
teto.

### 3.desarmamento-10826 — Estatuto do Desarmamento (2)

| Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|
| 19 | aumento | metade | **lista explícita: arts. 17 e 18** |
| 20 | aumento | metade | **lista explícita: arts. 14, 15, 16, 17 e 18** — incisos truncados |

Estes dois são os casos mais claros de alcance por lista explícita do bloco inteiro.

**A cadastrar junto:** a Lei 15.358/2026 (art. 37) inseriu o **art. 21-A** na Lei
10.826/2003 — aumento de **2/3** nos crimes dos arts. 12, 14 e 16, se praticados em
concurso com crime da Lei 11.343/06, se ligados ao comércio ilícito de
entorpecentes, ou se o artefato foi usado para assegurar a mercancia. Alcance por
lista explícita.

### 3.esporte-14597 — Lei Geral do Esporte (2)

| Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|
| 167, p.ú. | aumento | 1/3 até metade | art. 167, *caput* — qualidade do agente |
| 201, § 6º | aumento | 1/3 até metade | art. 201, *caput* e § 1º — organizador ou incitador |

### Diplomas com um dispositivo cada (11)

| Diploma | Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|---|
| Lei 11.101/05 | 168, § 2º | aumento | 1/3 até metade | art. 168, *caput* |
| Lei 12.850/13 | 2º, § 4º | aumento | 1/6 a 2/3 | art. 2º, *caput* e § 1º — incisos truncados |
| Lei 13.260/16 | 7º | aumento | **1/3** (lesão grave) / **metade** (morte) | **todos os crimes da Lei**, salvo quando o resultado for elementar |
| Lei 2.889/56 | 3º, § 2º | aumento | 1/3 | art. 3º — incitação pela imprensa |
| Lei 6.385/76 | 27-D, § 2º | aumento | 1/3 | art. 27-D, *caput* |
| Lei 7.492/86 | 19, p.ú. | aumento | 1/3 | art. 19, *caput* |
| Lei 7.716/89 | "2º, p.ú." | aumento | metade | **ver ressalva — B** |
| Lei 9.263/96 | 15, p.ú. | aumento | 1/3 | art. 15, *caput* — incisos truncados |
| Lei 9.296/96 | 10-A, § 2º | aumento | dobro | art. 10-A, *caput* — agente funcionário público |
| Lei 9.455/97 | 1º, § 4º | aumento | 1/6 a 1/3 | art. 1º, *caput* e §§ 1º e 2º — incisos truncados |
| Lei 9.613/98 | 1º, § 4º | aumento | 1/3 a 2/3 | art. 1º, *caput* e §§ 1º e 2º |

**Lei 7.716/89 — identificador provavelmente errado (B).** O dispositivo listado
como "Art. 2, parágrafo único" quase certamente é o **parágrafo único do art. 2º-A**,
que tipifica a injúria racial (incluído pela Lei 14.532/2023) e traz exatamente essa
majorante de metade por concurso de duas ou mais pessoas. O art. 2º da Lei 7.716/89,
na redação original, não comporta parágrafo único com esse conteúdo. **Não aplicar
sem conferir o compilado** — se confirmado, é erro de identificador que vai
propagar para o catálogo de modificadores.

**Lei 13.260/16, art. 7º — alcance de lei inteira (A).** É um dos poucos casos em
que a causa incide sobre todos os crimes do diploma, com a ressalva expressa de não
incidir quando o resultado for elementar do tipo — cláusula anti-*bis in idem* que o
motor de dosimetria precisa respeitar.

**Lei 9.613/98, art. 1º, § 4º — atualizar (A).** O texto no arquivo já contempla a
redação com "ativo virtual". Confirmado.

---

## Resumo do Bloco 3

- **97** dispositivos confirmados como causa de aumento ou diminuição.
- **8** não pertencem ao catálogo penal (CTB administrativo).
- **4** devem ser modelados como tipos culposos derivados, não como diminuição
  (Lei 9.605/98).
- **1** é duplicata (LCP art. 21).
- **9** precisam ser desdobrados em dois registros por conterem duas frações ou
  dois alcances (CP 121 § 4º, 135 p.ú., 135-A p.ú., 258, CPM 190 § 3º, 241 p.ú.,
  263 § 1º, 277, Idoso 97 p.ú., 13.260 art. 7º).
- **3** têm identificador suspeito e não devem ser aplicados sem conferência
  (CP 359-M, Lei 7.716 art. 2º, CPM 263/277 quanto ao alcance).
- **4** têm fração de teto sem mínimo legal (CP 122 § 4º, 135-A p.ú., 216-A § 2º,
  9.605 art. 29 § 5º) — exigem decisão de modelagem.

---

# Bloco 4 — Crimes militares hediondos por identidade

## Pergunta 3, primeiro: o que é "identidade"?

Respondo esta antes das outras porque a resposta determina as demais.

**Identidade exige correspondência de conduta e bem jurídico com a hipótese
específica listada no art. 1º — não basta o *nomen juris*.** Confiança **M**: é
posição defensável e a que considero correta, mas não há jurisprudência consolidada
do STF ou do STJ sobre o alcance do inciso VI, que é de 2023.

Três razões:

1. **A hediondez é consequência gravosa**, e sua imposição por analogia ou por
   leitura extensiva é vedada. Interpretar por *nomen juris* ampliaria o alcance da
   Lei 8.072/90 sem base típica, em prejuízo do réu.

2. **O rol do art. 1º é taxativo e identifica crimes por dispositivo, não por
   nome** — e, mais que isso, frequentemente por **hipótese dentro do dispositivo**.
   O roubo não é hediondo: são hediondas apenas as formas do art. 157, § 2º, V,
   § 2º-A, I, § 2º-B e § 3º. Se bastasse o nome, todo roubo militar seria hediondo,
   o que inverteria a lógica do próprio rol que o inciso VI manda espelhar.

3. **O inciso VI é o único do rol que não remete a dispositivo.** Justamente por
   isso deve ser lido do modo mais estrito possível: ele não cria hipóteses, apenas
   projeta as existentes sobre o CPM.

**Consequência prática para o catálogo:** a comparação deve ser feita *hipótese a
hipótese*, não *artigo a artigo*. Um artigo do CPM pode ter parágrafos com
identidade e parágrafos sem.

## Pergunta 1: os sete tipos hoje marcados

`artigo do CPM | há identidade | inciso do rol | fundamento`

### CPM art. 205, § 2º — **SIM** — inciso I — **M**

Corresponde ao homicídio qualificado do art. 121, § 2º do CP. A pena publicada
(12 a 30 anos) confere com a moldura do § 2º.

**Duas ressalvas:**

- O nome no catálogo ("Homicídio simples — Se o homicídio é cometido") é artefato de
  truncamento: o § 2º é a forma qualificada, e o rótulo está colando a epígrafe do
  *caput* ao início do § 2º. Corrigir para "Homicídio qualificado".
- A identidade deve ser conferida **inciso a inciso** do § 2º. Os incisos clássicos
  (motivo fútil, torpe, meio cruel, recurso que dificulte a defesa, conexão com
  outro crime) têm correspondente direto no art. 121, § 2º do CP. Se houver inciso
  próprio do CPM sem correspondente — e o índice de alterações do diploma sugere um
  inciso VII acrescentado — esse inciso **não** gera identidade. Não conferi o texto
  integral do § 2º; **B** quanto aos incisos individualmente.
- A primeira parte do inciso I do rol (homicídio simples em atividade típica de
  grupo de extermínio) não tem figura correspondente no CPM. Essa parte não projeta.

### CPM art. 232, *caput* — **SIM** — inciso V — **A**

Estupro na redação unificada dada pela Lei 14.688/2023 (constranger alguém, mediante
violência ou grave ameaça, a conjunção carnal ou outro ato libidinoso), reclusão de
6 a 10 anos. Conduta e bem jurídico idênticos ao art. 213, *caput* do CP, que o
inciso V arrola expressamente.

### CPM art. 232, § 1º — **SIM** — inciso V — **A**

Lesão grave ou vítima menor de 18 e maior de 14. Corresponde ao art. 213, § 1º do
CP, abrangido pelo inciso V ("*caput* e §§ 1º e 2º").

### CPM art. 232, § 2º — **SIM** — inciso V — **A**

Resultado morte. Corresponde ao art. 213, § 2º do CP, abrangido pelo inciso V.

### CPM art. 232, § 3º — **PREJUDICADA — dispositivo inconstitucional** — **A**

Este é o achado de maior impacto do bloco, e não é sobre hediondez.

O STF, na **ADI 7555** (Rel. Min. Cármen Lúcia, Plenário, julgamento virtual
encerrado em 29/08/2025), julgou procedente o pedido para:

- **declarar a inconstitucionalidade do § 3º do art. 232 do CPM**, incluído pela
  Lei 14.688/2023, com eficácia ***ex nunc*** a contar da publicação da ata de
  julgamento;
- declarar a **não recepção dos incisos I a III do art. 236 do CPM** (presunção
  relativa de violência);
- determinar que, ao estupro de vulnerável praticado por militar no exercício da
  função ou em lugar sujeito à administração militar, aplique-se **toda a disciplina
  do art. 217-A do CP, inclusive os §§ 1º a 5º**, por força do art. 9º, II do CPM
  (na ausência de previsão legal na legislação militar, aplica-se a lei penal comum
  em tempo de paz).

O fundamento foi proteção deficiente: o § 3º cominava 8 a 15 anos para o estupro de
vulnerável militar e não previa agravamento por lesão grave ou morte, enquanto o CP
comina 10 a 20 e 12 a 30 anos nessas hipóteses.

**O que fazer no catálogo:** não ajustar a hediondez. **Marcar o registro como
inconstitucional**, com a data de eficácia, e apontar o art. 217-A do CP como
dispositivo aplicável. Como a eficácia é *ex nunc*, o registro precisa continuar
consultável para fatos anteriores — o que é exatamente o tipo de caso em que um
campo de vigência com data importa mais que a exclusão do registro. Vale também
conferir se o catálogo registra o art. 236 do CPM e seus incisos I a III.

### CPM art. 244, *caput* — **SIM** — inciso IV — **A**

Extorsão mediante sequestro. O inciso IV do rol abrange o art. 159 do CP em todas as
formas (*caput* e §§ 1º, 2º e 3º), de modo que a figura simples do CPM tem
correspondente na figura simples arrolada.

**Ponto de vigilância (M):** a pena do CPM é de 6 a 15 anos, contra 8 a 15 do art.
159 do CP. É exatamente a assimetria de proteção deficiente que fundamentou a ADI
7555 quanto ao art. 232, § 3º. Não afirmo inconstitucionalidade — não há ação
julgada sobre este artigo — mas o registro merece marcação de risco de alteração.

### CPM art. 290, § 5º — **NÃO** — **A**

**Não há identidade possível.** Tráfico de drogas **não está no art. 1º da Lei
8.072/90**. É crime **equiparado** a hediondo, por força do art. 5º, XLIII da
Constituição e do art. 2º da Lei 8.072/90 — que é dispositivo diverso.

O inciso VI projeta sobre o CPM apenas os crimes "previstos no art. 1º desta Lei".
Como o tráfico não está lá, nenhum tipo militar de tráfico pode ser hediondo *por
identidade*.

**O que fazer:** remover a marcação de hediondez por identidade. Se a intenção do
catálogo é sinalizar o tratamento mais severo aplicável ao tráfico militar, isso é
**equiparação**, com fundamento próprio, e deve ocupar campo distinto — porque as
consequências não são idênticas às da hediondez por rol.

## Pergunta 2: falta algum?

**Confiança B para todo este item.** Respondo com candidatos, não com conclusões,
porque não conferi o texto integral do CPM.

**Candidato forte — roubo qualificado pelo resultado.** O inciso II, "c" do rol
arrola o art. 157, § 3º do CP (roubo qualificado por lesão grave ou morte). O CPM
tem figura correspondente no capítulo do roubo. Se ela existe com essa estrutura, a
identidade é defensável e o registro está faltando. **Conferir o art. 242 e
parágrafos do CPM.**

**Candidato — extorsão qualificada pelo resultado.** Inciso III do rol (art. 158,
§ 3º do CP). Conferir se o CPM tem figura correspondente.

**Candidato — sequestro ou cárcere privado contra menor de 18.** Inciso XI do rol
(art. 148, § 1º, IV do CP). Conferir a figura correspondente no CPM.

**Respostas negativas seguras (A):**

- **Lesão gravíssima: não.** Lesão corporal gravíssima não é hedionda no CP. Sem
  hipótese no rol, não há o que projetar.
- **Tráfico: não**, pela razão já dada.
- **Genocídio: não.** Está no parágrafo único, inciso I, que remete à Lei 2.889/56 —
  e o inciso VI só alcança crimes "previstos no art. 1º".
- **Roubo simples: não.** O rol não torna hediondo o roubo simples; só as formas
  circunstanciadas e qualificadas nomeadas.

**Sobre as demais hipóteses do rol** (epidemia com resultado morte, favorecimento da
prostituição de vulnerável, furto com explosivo, induzimento a suicídio por rede,
tráfico de pessoas contra criança): não afirmo ausência de correspondente no CPM
sem ler o texto integral. É levantamento que exige varredura artigo a artigo do
Livro II do CPM, e recomendo fazê-lo de uma vez, registrando o resultado — inclusive
os "não há correspondente", que são tão úteis quanto os positivos.

## O que registrar como critério

Sugiro que o catálogo grave, junto aos registros militares, o critério adotado em
texto curto, por exemplo:

> Hediondez por identidade (Lei 8.072/90, art. 1º, par. ún., VI, incluído pela Lei
> 14.688/2023). Critério adotado: correspondência de conduta e bem jurídico com
> hipótese específica arrolada no art. 1º, não bastando identidade de *nomen juris*.
> Matéria sem jurisprudência consolidada do STF/STJ.

Isso torna o dado auditável e sinaliza ao usuário que é classificação argumentativa,
não fato assentado.

---

# Bloco 5 — Que lei é o "marco legal do combate ao crime organizado"?

## 1. Qual diploma

**Lei nº 15.358, de 24 de março de 2026** — publicada no DOU de 25/03/2026, em vigor
na data da publicação (art. 44). Denominação legal: **Lei Raul Jungmann**;
conhecida como Lei Antifacção. Origem: PL 5.582/2025.

**Ementa:** institui o Marco Legal do Combate ao Crime Organizado no Brasil;
tipifica os crimes de domínio social estruturado e de favorecimento ao domínio
social estruturado; e altera o Código Penal, o Código de Processo Penal, a Lei
8.072/90, a Lei de Execução Penal, a Lei 11.343/06, a Lei 10.826/03, a Lei 9.613/98,
o Código Eleitoral, a Lei 13.756/18 e a Lei 14.790/23.

Confiança **A** — texto conferido no compilado do Planalto.

## 2. Tipifica os crimes? Onde e com que penas?

Sim.

**Art. 2º — Domínio social estruturado.** Dez condutas (incisos I a X), praticadas
por integrante de organização criminosa ultraviolenta, grupo paramilitar ou milícia
privada — entre elas o uso de violência ou grave ameaça para impor controle
territorial, a criação de barricadas para obstruir a ação policial, ataques a
instituições prisionais, apoderamento de meios de transporte e sabotagem de
serviços essenciais.

> **Pena — reclusão, de 20 a 40 anos**, sem prejuízo das sanções correspondentes à
> ameaça, à violência ou a outros crimes previstos na legislação penal.

**Art. 3º — Favorecimento ao domínio social estruturado.** Seis condutas (incisos I
a VI): promover, fundar ou aderir à organização; distribuir material de incitação;
prover material explosivo ou arma; ceder local; fornecer informações; e alegar
falsamente pertencer à organização para obter vantagem ou intimidar.

> **Pena — reclusão, de 12 a 20 anos, e multa.**

**Modificadores a cadastrar:**

| Dispositivo | Natureza | Fração | Alcance |
|---|---|---|---|
| art. 2º, § 1º | aumento | **2/3 ao dobro** | art. 2º, *caput* (11 incisos: liderança, financiamento, vítima qualificada, conexão entre facções, concurso de funcionário público, infiltração no setor público, arma de uso restrito, recrutamento de criança ou adolescente, transnacionalidade, extração ilegal de minerais, uso de drones e contrainteligência) |
| art. 2º, § 5º | diminuição | **1/3 a 1/2** | atos preparatórios com propósito inequívoco, punidos com a pena do crime consumado reduzida |

**Regras que atingem diretamente o motor de benefícios (art. 2º, § 4º, estendidas ao
art. 3º pelo parágrafo único deste):** os crimes são insuscetíveis de **anistia,
graça e indulto**, de **fiança** e de **livramento condicional**. Somam-se: vedação
de auxílio-reclusão (§ 6º), cumprimento obrigatório em estabelecimento penal federal
de segurança máxima para lideranças (§ 7º), competência das Varas Criminais
Colegiadas para homicídios conexos (§ 8º) e prisão preventiva por causa suficiente
(§ 9º).

## 3. Coincidem com a organização criminosa da Lei 12.850/2013?

**Não — são autônomos, com relação de especialidade.** Três diferenças estruturais:

- **Número de agentes:** a facção do art. 2º, § 2º exige **3 ou mais** pessoas; a
  organização criminosa da Lei 12.850/13 exige **4 ou mais**.
- **Núcleo típico:** a Lei 12.850/13 pune a associação estável voltada à obtenção de
  vantagem; a Lei 15.358/26 pune o **exercício de poder estruturado** — controle
  territorial, social ou econômico mediante violência ou grave ameaça.
- **Relação declarada:** o art. 4º, parágrafo único diz que as condutas desta Lei e
  o art. 288-A do CP constituem **formas especiais de organização criminosa**,
  aplicando-se, no que couber, as disposições materiais da Lei 12.850/13. Ou seja,
  não há revogação nem absorção: há especialidade com aplicação subsidiária.

## 4. O problema do § 3º — leia antes de aplicar

**O § 3º do art. 2º foi VETADO** (Mensagem de veto VEP-216/26). Ele não existe no
texto sancionado.

Isso contamina duas remissões:

- o **art. 4º** da própria Lei 15.358/26, que declara hediondos "os crimes previstos
  no *caput* e nos §§ 1º e 3º do art. 2º e no art. 3º";
- o **inciso VIII** do parágrafo único do art. 1º da Lei 8.072/90, inserido pelo art.
  34 da mesma lei, com redação idêntica.

Ambos remetem a dispositivo inexistente. É defeito clássico de veto parcial: o
Executivo vetou o parágrafo e não houve ajuste das remissões cruzadas.

**Como registrar:** hediondos são o **art. 2º, *caput***, o **art. 2º, § 1º** e o
**art. 3º**. A remissão ao § 3º é inócua e deve ser anotada como tal, não como
pendência de cadastro — senão a auditoria vai procurar indefinidamente um
dispositivo que não existe.

**Segunda estranheza, esta de técnica legislativa (M):** o § 1º do art. 2º é **causa
de aumento**, não tipo penal. Declarar hediondo um dispositivo que só majora pena é
redundante — se o *caput* já é hediondo, a forma majorada também é. Registrar a
hediondez no *caput* e tratar o § 1º como modificador resolve sem perda.

## 5. O impacto real no catálogo é muito maior que dois tipos

Esta é a parte que a pergunta não previa. A Lei 15.358/26 é reforma de sistema, não
lei de dois crimes. Levantamento do que ela cria e altera:

**Novos tipos e figuras no Código Penal (art. 33 da Lei):**

| Dispositivo | Conteúdo | Pena |
|---|---|---|
| CP 121, § 2º-D | homicídio doloso por integrante de facção, no contexto do art. 2º | reclusão, 20 a 40 anos |
| CP 129, § 3º-A | lesão seguida de morte no contexto do art. 2º | reclusão, 20 a 40 anos |
| CP 147-C | ameaça no contexto do art. 2º | reclusão, 1 a 3 anos |
| CP 148, § 3º | sequestro ou cárcere privado por integrante de facção | reclusão, 12 a 20 anos |
| CP 155, § 9º | furto por integrante de facção | reclusão, 4 a 10 anos, e multa |
| CP 157, § 5º | roubo do § 3º, II, por integrante de facção, com resultado morte | reclusão, 20 a 40 anos, e multa |

**Novos modificadores:**

| Dispositivo | Natureza | Fração |
|---|---|---|
| CP 129, § 8º-A | aumento | 2/3 |
| CP 157, § 4º | aumento | **triplo**, desprezadas as demais causas de aumento |
| CP 158, § 4º | aumento | triplo |
| CP 159, § 5º | aumento | 2/3 |
| CP 180, § 8º | aumento | 2/3 |
| Lei 11.343/06, art. 40-A | aumento | dobro (+ concurso material se houver arma de fogo) |
| Lei 10.826/03, art. 21-A | aumento | 2/3 |

**Revogação:** o § 5º do art. 180 do CP foi revogado.

**Alteração de maior alcance — art. 112 da LEP:** os percentuais de progressão foram
reescritos (inciso V: 70% para hediondo primário; VI: 75%, com nova alínea "b" para
comando de organização criminosa ultraviolenta, vedado o livramento condicional, e
alínea "d" para feminicídio primário, também vedado o livramento; VII: 80%; VIII:
85% para reincidente em hediondo com resultado morte, vedado o livramento), e o
inciso VI-A foi revogado.

**Isso atinge o cálculo de progressão de todo o catálogo, não apenas dos crimes
novos.** Se o motor de progressão do SISPENAS ainda usa a tabela anterior, todos os
resultados de progressão para crimes hediondos estão desatualizados desde
25/03/2026. Na minha leitura é a pendência mais urgente deste arquivo inteiro —
mais que qualquer nome de tipo do Bloco 1.

**Outras alterações relevantes:** CPP arts. 3º-B, 78, I, 310 e 313, V; CP arts. 91,
91-A, § 5º e 92; Lei 9.613/98 arts. 4º-A e 7º; Código Eleitoral arts. 5º, IV e 71,
VI (suspensão de direitos políticos de presos provisórios).

---

# Apêndice — o que ficou como pendência

Itens que **não** devem virar dado publicado sem conferência adicional:

| Item | O que falta ver |
|---|---|
| 1.7 — Lei 7.643/87 | vigência frente ao art. 29 da Lei 9.605/98; jurisprudência |
| 1.12 — origem do nome errado do art. 72 da Lei 9.504/97 | de qual artigo o rótulo foi importado |
| 2.6 — CP 151, § 1º, IV | revogação tácita pelo art. 183 da Lei 9.472/97; jurisprudência do STJ |
| 2.8 — CP 153, § 1º-A | escolha entre as duas leituras; sugiro registrar como condicionada com a divergência anotada |
| 3 — CP art. 359-M | designação correta do dispositivo no compilado (provável 359-M-B) |
| 3 — Lei 7.716/89 "art. 2º, p.ú." | confirmar se é o parágrafo único do art. 2º-A |
| 3 — CPM arts. 263, § 1º e 277 | alcance: quais artigos do capítulo |
| 3 — ~30 dispositivos truncados | incisos, onde a hipótese importa para o alcance |
| 4 — CPM art. 205, § 2º | identidade inciso a inciso, incluindo eventual inciso VII |
| 4 — o que falta no rol militar | varredura do Livro II do CPM contra os doze incisos do art. 1º |

E três varreduras dirigidas que este trabalho sugere:

1. **Pares de artigos com pena idêntica no mesmo diploma** — são o ponto cego da
   auditoria automática (caso 1.13).
2. **Registros cujo nome veio de outro artigo** — reconferir a pena de todos, porque
   a auditoria não os pega (caso 1.2).
3. **Dispositivos administrativos capturados como penais** em diplomas que têm as
   duas naturezas: CTB (já identificado), Lei 9.605/98, Estatuto da Pessoa Idosa,
   Lei 13.146/15.
