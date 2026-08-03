# Revisão pendente — o que a auditoria encontrou e não sabe decidir

> **ARQUIVO TEMPORÁRIO DE TRABALHO.** É o pacote de perguntas que a conferência
> automática acumulou e que só gente responde. Ao fechar todos os blocos,
> **exclua este arquivo** no mesmo PR — o registro permanente é o changelog.
>
> Gerado em 02/08/2026, a partir da rodada de `scripts/crawler/auditar.py` sobre
> o catálogo da v1.7.0 (1.412 tipos penais).

## Como usar isto

Cada bloco abaixo é uma **pergunta** com os dados já reunidos. A resposta se
aplica editando `data/crimes.json` (a fonte) ou `data/modificadores.json`, e
regenerando o derivado.

**Regras do projeto que valem sempre — leia antes de mexer:**

1. **Nada entra sem conferência contra o texto compilado** do `planalto.gov.br`.
   O link de cada diploma está em `data/fontes.json`, e a cópia já baixada em
   `crawler/snapshots/<id>/` (se não existir: `python scripts/crawler/baixar.py
   --fonte <id>`). Onde não houver certeza, **deixe como está e anote a dúvida** —
   dado errado publicado é pior que dado ausente.
2. **Uma sessão = uma release.** Acumule as entradas de changelog sob a mesma
   `version` (`src/data/changelog/entries/<ano>/<id>.ts`, texto puro, sem
   markdown) e suba `package.json` + `CITATION.cff` uma vez só, ao fechar.
   Correção de dado → `1.Y.Z`; campo novo nos dados abertos → `1.Y.0`.
3. **Verificação antes de concluir**, nesta ordem:
   ```
   python scripts/transform_data.py --estrito --max-contradicoes=0
   python scripts/validar_modificadores.py
   python -m pytest scripts/crawler/tests
   npm run typecheck && npm run verificar && npm run build
   ```
4. **Trabalhe em branch própria**; não faça push nem abra PR sem o mantenedor
   pedir.
5. `id` é **URL pública** e nunca é reatribuído. Registro retirado entra em
   `data/ids-aposentados.json`.
6. Convenções completas em `CONTRIBUTING.md` (C1 a C8) e `CLAUDE.md`.

**O que NÃO está aqui:** divergência de pena. A conferência semanal contra o
compilado está com **zero divergências** — pena, espécie, existência e situação
de cada dispositivo batem com a lei.

---

### 1. Nome do tipo que não conversa com o dispositivo (13)

**Pergunta:** o nome descreve a conduta DESTE artigo, ou foi copiado de outro?

| id | Diploma e artigo | Nome publicado | O que o artigo diz |
|---|---|---|---|
| 792 | `CE (Lei 4.737/65) Art. 310` | Violar ou tentar violar o sigilo do voto | Praticar, ou permitir membro da mesa receptora que seja praticada, qualquer irregularidade que determine a anulação de votação, salvo no caso do Art.  |
| 794 | `CE (Lei 4.737/65) Art. 313` | Falsificar no todo ou em parte documento público ou alterar documento  | Deixar o juiz e os membros da Junta de expedir o boletim de apuração imediatamente após a apuração de cada urna e antes de passar à subseqüente, sob q |
| 750 | `CP Art. 338` | Sonegação de contribuição previdenciária (suprimir/reduzir contribuiçã | Reingresso de estrangeiro expulso — Reingressar no território nacional o estrangeiro que dele foi expulso: |
| 474 | `Lei 10.741/03 Art. 100` | Obstar acesso de idoso a cargo público por motivo de idade | Constitui crime punível com reclusão de 6 (seis) meses a 1 (um) ano e multa: |
| 328 | `Lei 11.343/06 Art. 40` | Tráfico com majorantes (1/6 a 2/3): transnacional, transporte público, | As penas previstas nos arts. 33 a 37 desta Lei são aumentadas de um sexto a dois terços, se: |
| 411 | `Lei 7.492/86 Art. 10` | Empréstimo/adiantamento vedado ou em condições mais vantajosas que as  | Fazer inserir elemento falso ou omitir elemento exigido pela legislação, em demonstrativos contábeis de instituição financeira, seguradora ou institui |
| 917 | `Lei 7.643/87 Art. 2º` | Pesca ou molestamento intencional de cetáceo em águas jurisdicionais b | A infração ao disposto nesta lei será punida com a pena de 2 (dois) a 5 (cinco) anos de reclusão e multa de 50 (cinqüenta) a 100 (cem) Obrigações do T |
| 399 | `Lei 8.137/90 Art. 2º` | Sonegação fiscal formal (condutas que dificultam a fiscalização, sem e | Constitui crime da mesma natureza: (Vide Lei nº 9.964, de 10.4.2000) |
| 670 | `Lei 8.137/90 Art. 2º, I` | Fazer declaração falsa ou omitir declaração sobre rendas, bens ou fato | Constitui crime da mesma natureza: (Vide Lei nº 9.964, de 10.4.2000) |
| 671 | `Lei 8.137/90 Art. 2º, II` | Deixar de recolher no prazo legal tributo descontado ou cobrado na qua | Constitui crime da mesma natureza: (Vide Lei nº 9.964, de 10.4.2000) |
| 550 | `Lei 8.245/91 Art. 44` | Cobrar antecipadamente o aluguel (salvo nos casos do Art. 42) | Constitui crime de ação pública, punível com detenção de três meses a um ano, que poderá ser substituída pela prestação de serviços à comunidade: |
| 537 | `Lei 9.504/97 Art. 72` | Inserção de dados falsos no sistema eleitoral (inserir/alterar dados n | Constituem crimes, puníveis com reclusão, de cinco a dez anos: |
| 355 | `Lei 9.605/98 Art. 33` | Pesca em período ou local proibido | Provocar, pela emissão de efluentes ou carreamento de materiais, o perecimento de espécimes da fauna aquática existentes em rios, lagos, açudes, lagoa |

### 2. Ação penal com ressalva de hipótese (9)

**Pergunta:** este registro cai na hipótese da regra ou na da ressalva?

| id | Diploma e artigo | Ação publicada | Crime |
|---|---|---|---|
| 76 | `CP Art. 151` | Pública Incondicionada | Violação de correspondência |
| 1351 | `CP Art. 151, § 3º` | Pública Incondicionada | Violação de correspondência — Se o agente comete o crime, com abuso de |
| 77 | `CP Art. 151, §1º, I` | Pública Incondicionada | Sonegação ou destruição de correspondência |
| 78 | `CP Art. 151, §1º, II` | Pública Incondicionada | Violação de comunicação telegráfica, radioelétrica ou telefônica |
| 646 | `CP Art. 151, §1º, III` | Pública Incondicionada | Impedir a comunicação telegráfica, radioelétrica ou telefônica |
| 647 | `CP Art. 151, §1º, IV` | Pública Incondicionada | Instalar ou utilizar estação ou aparelho radioelétrico sem autorização |
| 79 | `CP Art. 153` | Ação Penal Privada | Divulgação de segredo |
| 80 | `CP Art. 153, §1º-A` | Pública Incondicionada | Divulgação de informações sigilosas da administração pública |
| 285 | `CP Art. 345` | Ação Penal Privada | Exercício arbitrário das próprias razões |

### 3. Causas de aumento e diminuição ausentes de `data/modificadores.json` (109)

**Pergunta por dispositivo:** (a) é causa de aumento/diminuição de pena? (b) qual a fração? (c) sobre QUAIS tipos incide — o artigo, o capítulo, o diploma?

<details><summary><strong>cp</strong> — 41 (<a href="https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm">texto compilado</a>)</summary>

- `Art. 121-A|§ 2º` — A pena do feminicídio é aumentada de 1/3 (um terço) até a metade se o crime é praticado: (Incluído pela Lei nº 14.994, de 2024)
- `Art. 121-B|parágrafo único` — A pena do vicaricídio é aumentada de 1/3 (um terço) até a metade se o crime for praticado: (Incluído pela Lei nº 15.384, de 2026)
- `Art. 121|§ 4º` — No homicídio culposo, a pena é aumentada de 1/3 (um terço), se o crime resulta de inobservância de regra técnica de profissão, arte ou ofíci
- `Art. 121|§ 6º` — A pena é aumentada de 1/3 (um terço) até a metade se o crime for praticado por milícia privada, sob o pretexto de prestação de serviço de se
- `Art. 122|§ 4º` — A pena é aumentada até o dobro se a conduta é realizada por meio da rede de computadores, de rede social ou transmitida em tempo real. (Incl
- `Art. 132|parágrafo único` — A pena é aumentada de um sexto a um terço se a exposição da vida ou da saúde de outrem a perigo decorre do transporte de pessoas para a pres
- `Art. 135-A|parágrafo único` — A pena é aumentada até o dobro se da negativa de atendimento resulta lesão corporal de natureza grave, e até o triplo se resulta a morte. (I
- `Art. 135|parágrafo único` — A pena é aumentada de metade, se da omissão resulta lesão corporal de natureza grave, e triplicada, se resulta a morte
- `Art. 136|§ 3º` — Aumenta-se a pena de um terço, se o crime é praticado contra pessoa menor de 14 (catorze) anos. (Incluído pela Lei nº 8.069, de 1990)
- `Art. 147-A|§ 1º` — A pena é aumentada de metade se o crime é cometido: (Incluído pela Lei nº 14.132, de 2021)
- `Art. 147-B|parágrafo único` — A pena é aumentada de metade se o crime é cometido mediante uso de inteligência artificial ou de qualquer outro recurso tecnológico que alte
- `Art. 149-A|§ 1º` — A pena é aumentada de um terço até a metade se: (Incluído pela Lei nº 13.344, de 2016) (Vigência)
- `Art. 149-A|§ 2º` — A pena é reduzida de um a dois terços se o agente for primário e não integrar organização criminosa. (Incluído pela Lei nº 13.344, de 2016) 
- `Art. 149|§ 2º` — A pena é aumentada de metade, se o crime é cometido: (Incluído pela Lei nº 10.803, de 11.12.2003)
- `Art. 154-A|§ 2º` — Aumenta-se a pena de 1/3 (um terço) a 2/3 (dois terços) se da invasão resulta prejuízo econômico. (Redação dada pela Lei nº 14.155, de 2021)
- `Art. 154-A|§ 4º` — Na hipótese do § 3 o , aumenta-se a pena de um a dois terços se houver divulgação, comercialização ou transmissão a terceiro, a qualquer tít
- `Art. 154-A|§ 5º` — Aumenta-se a pena de um terço à metade se o crime for praticado contra: (Incluído pela Lei nº 12.737, de 2012) Vigência
- `Art. 157|§ 2º-B` — Se a violência ou grave ameaça é exercida com emprego de arma de fogo de uso restrito ou proibido, aplica-se em dobro a pena prevista no cap
- `Art. 168|§ 1º` — A pena é aumentada de um terço, quando o agente recebeu a coisa:
- `Art. 203|§ 2º` — A pena é aumentada de um sexto a um terço se a vítima é menor de dezoito anos, idosa, gestante, indígena ou portadora de deficiência física 
- `Art. 207|§ 2º` — A pena é aumentada de um sexto a um terço se a vítima é menor de dezoito anos, idosa, gestante, indígena ou portadora de deficiência física 
- `Art. 208|parágrafo único` — Se há emprego de violência, a pena é aumentada de um terço, sem prejuízo da correspondente à violência
- `Art. 209|parágrafo único` — Se há emprego de violência, a pena é aumentada de um terço, sem prejuízo da correspondente à violência
- `Art. 216-A|§ 2º` — A pena é aumentada em até um terço se a vítima é menor de 18 (dezoito) anos. (Incluído pela Lei nº 12.015, de 2009)
- `Art. 218-C|§ 1º` — A pena é aumentada de 1/3 (um terço) a 2/3 (dois terços) se o crime é praticado por agente que mantém ou tenha mantido relação íntima de afe
- `Art. 232-A|§ 2º` — A pena é aumentada de 1/6 (um sexto) a 1/3 (um terço) se: Incluído pela Lei nº 13.445, de 2017 Vigência
- `Art. 258|caput` — Se do crime doloso de perigo comum resulta lesão corporal de natureza grave, a pena privativa de liberdade é aumentada de metade; se resulta
- `Art. 268|parágrafo único` — A pena é aumentada de um terço, se o agente é funcionário da saúde pública ou exerce a profissão de médico, farmacêutico, dentista ou enferm
- `Art. 311-A|§ 3º` — Aumenta-se a pena de 1/3 (um terço) se o fato é cometido por funcionário público. (Incluído pela Lei 12.550. de 2011)
- `Art. 311|§ 1º` — Se o agente comete o crime no exercício da função pública ou em razão dela, a pena é aumentada de um terço. (Incluído pela Lei nº 9.426, de 
- `Art. 317|§ 1º` — A pena é aumentada de um terço, se, em conseqüência da vantagem ou promessa, o funcionário retarda ou deixa de praticar qualquer ato de ofíc
- `Art. 332|parágrafo único` — A pena é aumentada da metade, se o agente alega ou insinua que a vantagem é também destinada ao funcionário. (Redação dada pela Lei nº 9.127
- `Art. 333|parágrafo único` — A pena é aumentada de um terço, se, em razão da vantagem ou promessa, o funcionário retarda ou omite ato de ofício, ou o pratica infringindo
- `Art. 334-A|§ 3º` — A pena aplica-se em dobro se o crime de contrabando é praticado em transporte aéreo, marítimo ou fluvial. (Incluído pela Lei nº 13.008, de 2
- `Art. 334|§ 3º` — A pena aplica-se em dobro se o crime de descaminho é praticado em transporte aéreo, marítimo ou fluvial. (Redação dada pela Lei nº 13.008, d
- `Art. 337-B|parágrafo único` — A pena é aumentada de 1/3 (um terço), se, em razão da vantagem ou promessa, o funcionário público estrangeiro retarda ou omite o ato de ofíc
- `Art. 337-C|parágrafo único` — A pena é aumentada da metade, se o agente alega ou insinua que a vantagem é também destinada a funcionário estrangeiro. (Incluído pela Lei n
- `Art. 337-O|§ 2º` — Se o crime é praticado com o fim de obter benefício, direto ou indireto, próprio ou de outrem, aplica-se em dobro a pena prevista no caput d
- `Art. 339|§ 2º` — A pena é diminuída de metade, se a imputação é de prática de contravenção
- `Art. 359-I|§ 1º` — Aumenta-se a pena de metade até o dobro, se declarada guerra em decorrência das condutas previstas no caput deste artigo. (Incluído pela Lei
- `Art. 359-M|caput` — B. Quando os crimes previstos neste Capítulo forem praticados em contexto de multidão, a pena será reduzida de 1/3 (um terço) a 2/3 (dois te

</details>

<details><summary><strong>cpm</strong> — 18 (<a href="https://www.planalto.gov.br/ccivil_03/decreto-lei/del1001compilado.htm">texto compilado</a>)</summary>

- `Art. 160|parágrafo único` — Se o fato é praticado contra o comandante da unidade a que pertence o agente, oficial-general, oficial de dia, de serviço ou de quarto, a pe
- `Art. 162|parágrafo único` — A pena é aumentada da metade, se o fato é praticado diante da tropa, ou em público
- `Art. 190|§ 3º` — A pena é aumentada de um terço, se se tratar de sargento, subtenente ou suboficial, e de metade, se oficial. (Redação dada pela Lei nº 9.764
- `Art. 196|§ 2º` — Se o agente exercia função de comando, a pena é aumentada de metade
- `Art. 206|§ 1º` — A pena é aumentada de 1/3 (um terço): (Incluído pela Lei nº 14.688, de 2023)
- `Art. 206|§ 2º` — Se, em conseqüência de uma só ação ou omissão culposa, ocorre morte de mais de uma pessoa ou também lesões corporais em outras pessoas, a pe
- `Art. 207|§ 3º` — Se o suicídio é apenas tentado, e da tentativa resulta lesão grave, a pena é reduzida de um a dois terços
- `Art. 210|§ 1º` — A pena é aumentada de 1/3 (um terço) se o crime resulta da inobservância de regra técnica de profissão, arte ou ofício, ou se o agente deixa
- `Art. 210|§ 2º` — Se, em conseqüência de uma só ação ou omissão culposa, ocorrem lesões em várias pessoas, a pena é aumentada de um sexto até metade
- `Art. 213|§ 3º` — A pena é aumentada de 1/3 (um terço) se o crime é praticado contra pessoa menor de 14 (quatorze) anos, maior de 60 (sessenta) anos ou com de
- `Art. 226|§ 2º` — A pena é aumentada de 1/3 (um terço) se o fato é cometido por militar em serviço ou por servidor público, fora dos casos legais, ou com inob
- `Art. 241|parágrafo único` — A pena é aumentada de metade se a coisa usada é veículo motorizado, embarcação, aeronave ou arma, e de 1/3 (um terço) se é animal de sela ou
- `Art. 263|§ 1º` — Se resulta lesão grave, a pena correspondente é aumentada da metade; se resulta a morte, é aplicada em dôbro
- `Art. 267|§ 2º` — A pena é aumentada de 1/3 (um terço) se o crime é cometido por superior, por militar ou por servidor público, em razão da função. (Redação d
- `Art. 277|caput` — Se do crime doloso de perigo comum resulta, além da vontade do agente, lesão grave, a pena é aumentada de metade; se resulta morte, é aplica
- `Art. 290|§ 4º` — A pena é aumentada de metade se as condutas descritas no caput deste artigo são cometidas por militar em serviço. (Incluído pela Lei nº 14.6
- `Art. 308|§ 1º` — A pena é aumentada de um terço, se, em conseqüência da vantagem ou promessa, o agente retarda ou deixa de praticar qualquer ato de ofício ou
- `Art. 336|parágrafo único` — A pena é aumentada de metade se o agente alega ou insinua que a vantagem é também destinada ao militar ou ao servidor público. (Redação dada

</details>

<details><summary><strong>ctb</strong> — 10 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l9503compilado.htm">texto compilado</a>)</summary>

- `Art. 165-A|parágrafo único` — Aplica-se em dobro a multa prevista no caput em caso de reincidência no período de até 12 (doze) meses (Incluído pela Lei nº 13.281, de 2016
- `Art. 165|parágrafo único` — Aplica-se em dobro a multa prevista no caput em caso de reincidência no período de até 12 (doze) meses. (Redação dada pela Lei nº 12.760, de
- `Art. 173|parágrafo único` — Aplica-se em dobro a multa prevista no caput em caso de reincidência no período de 12 (doze) meses da infração anterior. (Incluído pela Lei 
- `Art. 174|§ 2º` — Aplica-se em dobro a multa prevista no caput em caso de reincidência no período de 12 (doze) meses da infração anterior. Incluído pela Lei n
- `Art. 175|parágrafo único` — Aplica-se em dobro a multa prevista no caput em caso de reincidência no período de 12 (doze) meses da infração anterior. (Incluído pela Lei 
- `Art. 191|parágrafo único` — Aplica-se em dobro a multa prevista no caput em caso de reincidência no período de até 12 (doze) meses da infração anterior. (Incluído pela 
- `Art. 203|parágrafo único` — Aplica-se em dobro a multa prevista no caput em caso de reincidência no período de até 12 (doze) meses da infração anterior. (Incluído pela 
- `Art. 253-A|§ 2º` — Aplica-se em dobro a multa em caso de reincidência no período de 12 (doze) meses. (Incluído pela Lei nº 13.281, de 2016)
- `Art. 302|§ 1º` — No homicídio culposo cometido na direção de veículo automotor, a pena é aumentada de 1/3 (um terço) à metade, se o agente: (Incluído pela Le
- `Art. 303|§ 1º` — Aumenta-se a pena de 1/3 (um terço) à metade, se ocorrer qualquer das hipóteses do § 1 o do art. 302. (Renumerado do parágrafo único pela Le

</details>

<details><summary><strong>ambiental-9605</strong> — 10 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l9605.htm">texto compilado</a>)</summary>

- `Art. 29|§ 4º` — A pena é aumentada de metade, se o crime é praticado:
- `Art. 29|§ 5º` — A pena é aumentada até o triplo, se o crime decorre do exercício de caça profissional
- `Art. 32|§ 2º` — A pena é aumentada de um sexto a um terço, se ocorre morte do animal. (Vide ADPF 640)
- `Art. 38-A|parágrafo único` — Se o crime for culposo, a pena será reduzida à metade. (Incluído pela Lei nº 11.428, de 2006)
- `Art. 38|parágrafo único` — Se o crime for culposo, a pena será reduzida à metade
- `Art. 40-A|§ 3º` — Se o crime for culposo, a pena será reduzida à metade. (Incluído pela Lei nº 9.985, de 2000)
- `Art. 40|§ 3º` — Se o crime for culposo, a pena será reduzida à metade
- `Art. 53|caput` — Nos crimes previstos nesta Seção, a pena é aumentada de um sexto a um terço se:
- `Art. 56|§ 2º` — Se o produto ou a substância for nuclear ou radioativa, a pena é aumentada de um sexto a um terço
- `Art. 69-A|§ 2º` — A pena é aumentada de 1/3 (um terço) a 2/3 (dois terços), se há dano significativo ao meio ambiente, em decorrência do uso da informação fal

</details>

<details><summary><strong>lcp</strong> — 4 (<a href="https://www.planalto.gov.br/ccivil_03/decreto-lei/del3688.htm">texto compilado</a>)</summary>

- `Art. 19|§ 1º` — A pena é aumentada de um terço até metade, se o agente já foi condenado, em sentença irrecorrivel, por violência contra pessoa
- `Art. 21|parágrafo único` — Aumenta-se a pena de 1/3 (um terço) até a metade se a vítima é maior de 60 (sessenta) anos. (Incluído pela Lei nº 10.741, de 2003)
- `Art. 21|§ 1º` — Aumenta-se a pena de 1/3 (um terço) até a metade se a vítima é maior de 60 (sessenta) anos. (Renumerado do parágrafo único pela Lei nº 14.99
- `Art. 50|§ 1º` — A pena é aumentada de um terço, se existe entre os empregados ou participa do jogo pessoa menor de dezoito anos

</details>

<details><summary><strong>ce</strong> — 3 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l4737compilado.htm">texto compilado</a>)</summary>

- `Art. 323|§ 2º` — Aumenta-se a pena de 1/3 (um terço) até metade se o crime: (Incluído pela Lei nº 14.192, de 2021)
- `Art. 326-A|§ 2º` — A pena é diminuída de metade, se a imputação é de prática de contravenção. (Incluído pela Lei nº13.834, de 2019)
- `Art. 326-B|parágrafo único` — Aumenta-se a pena em 1/3 (um terço), se o crime é cometido contra mulher: (Incluído pela Lei nº 14.192, de 2021)

</details>

<details><summary><strong>eca</strong> — 3 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l8069compilado.htm">texto compilado</a>)</summary>

- `Art. 240|§ 2º` — Aumenta-se a pena de 1/3 (um terço) se o agente comete o crime: (Redação dada pela Lei nº 11.829, de 2008)
- `Art. 241-B|§ 1º` — A pena é diminuída de 1 (um) a 2/3 (dois terços) se de pequena quantidade o material a que se refere o caput deste artigo. (Incluído pela Le
- `Art. 243|parágrafo único` — A pena será aumentada de 1/3 (um terço) até a metade se a criança ou o adolescente utilizar ou consumir o produto. (Incluído pela Lei nº 15.

</details>

<details><summary><strong>pcd-13146</strong> — 3 (<a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm">texto compilado</a>)</summary>

- `Art. 88|§ 1º` — Aumenta-se a pena em 1/3 (um terço) se a vítima encontrar-se sob cuidado e responsabilidade do agente
- `Art. 89|parágrafo único` — Aumenta-se a pena em 1/3 (um terço) se o crime é cometido:
- `Art. 91|parágrafo único` — Aumenta-se a pena em 1/3 (um terço) se o crime é cometido por tutor ou curador

</details>

<details><summary><strong>idoso-10741</strong> — 2 (<a href="https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm">texto compilado</a>)</summary>

- `Art. 96|§ 2º` — A pena será aumentada de 1/3 (um terço) se a vítima se encontrar sob os cuidados ou responsabilidade do agente
- `Art. 97|parágrafo único` — A pena é aumentada de metade, se da omissão resulta lesão corporal de natureza grave, e triplicada, se resulta a morte

</details>

<details><summary><strong>desarmamento-10826</strong> — 2 (<a href="https://www.planalto.gov.br/ccivil_03/leis/2003/l10.826compilado.htm">texto compilado</a>)</summary>

- `Art. 19|caput` — Nos crimes previstos nos arts. 17 e 18, a pena é aumentada da metade se a arma de fogo, acessório ou munição forem de uso proibido ou restri
- `Art. 20|caput` — Nos crimes previstos nos arts. 14, 15, 16, 17 e 18, a pena é aumentada da metade se: (Redação dada pela Lei nº 13.964, de 2019)

</details>

<details><summary><strong>esporte-14597</strong> — 2 (<a href="https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14597.htm">texto compilado</a>)</summary>

- `Art. 167|parágrafo único` — A pena será aumentada de 1/3 (um terço) até a metade se o agente for servidor público, dirigente ou funcionário de organização esportiva que
- `Art. 201|§ 6º` — A pena prevista neste artigo será aumentada de 1/3 (um terço) até a metade para aquele que organiza ou prepara o tumulto ou incita a sua prá

</details>

<details><summary><strong>falencias-11101</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/lei/l11101.htm">texto compilado</a>)</summary>

- `Art. 168|§ 2º` — A pena é aumentada de 1/3 (um terço) até metade se o devedor manteve ou movimentou recursos ou valores paralelamente à contabilidade exigida

</details>

<details><summary><strong>orgcrim-12850</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12850.htm">texto compilado</a>)</summary>

- `Art. 2|§ 4º` — A pena é aumentada de 1/6 (um sexto) a 2/3 (dois terços):

</details>

<details><summary><strong>terrorismo-13260</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/lei/l13260.htm">texto compilado</a>)</summary>

- `Art. 7|caput` — Salvo quando for elementar da prática de qualquer crime previsto nesta Lei, se de algum deles resultar lesão corporal grave, aumenta-se a pe

</details>

<details><summary><strong>genocidio-2889</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l2889.htm">texto compilado</a>)</summary>

- `Art. 3|§ 2º` — A pena será aumentada de 1/3 (um terço), quando a incitação for cometida pela imprensa

</details>

<details><summary><strong>cvm-6385</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l6385.htm">texto compilado</a>)</summary>

- `Art. 27-D|§ 2º` — A pena é aumentada em 1/3 (um terço) se o agente comete o crime previsto no caput deste artigo valendo-se de informação relevante de que ten

</details>

<details><summary><strong>sfn-7492</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l7492.htm">texto compilado</a>)</summary>

- `Art. 19|parágrafo único` — A pena é aumentada de 1/3 (um terço) se o crime é cometido em detrimento de instituição financeira oficial ou por ela credenciada para o rep

</details>

<details><summary><strong>racismo-7716</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l7716.htm">texto compilado</a>)</summary>

- `Art. 2|parágrafo único` — A pena é aumentada de metade se o crime for cometido mediante concurso de 2 (duas) ou mais pessoas. (Incluído pela Lei nº 14.532, de 2023)

</details>

<details><summary><strong>planejamento-familiar-9263</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l9263.htm">texto compilado</a>)</summary>

- `Art. 15|parágrafo único` — A pena é aumentada de um terço se a esterilização for praticada:

</details>

<details><summary><strong>interceptacao-9296</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l9296.htm">texto compilado</a>)</summary>

- `Art. 10-A|§ 2º` — A pena será aplicada em dobro ao funcionário público que descumprir determinação de sigilo das investigações que envolvam a captação ambient

</details>

<details><summary><strong>tortura-9455</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l9455.htm">texto compilado</a>)</summary>

- `Art. 1|§ 4º` — Aumenta-se a pena de um sexto até um terço:

</details>

<details><summary><strong>lavagem-9613</strong> — 1 (<a href="https://www.planalto.gov.br/ccivil_03/leis/l9613.htm">texto compilado</a>)</summary>

- `Art. 1|§ 4º` — A pena será aumentada de 1/3 (um terço) a 2/3 (dois terços) se os crimes definidos nesta Lei forem cometidos de forma reiterada, por intermé

</details>

---

## 4. Hediondez dos crimes do Código Penal Militar (7 registros)

**Pergunta:** cada um destes tipos militares apresenta "identidade" com algum
crime do rol do art. 1º da Lei 8.072/1990?

O inciso VI do parágrafo único (incluído pela Lei 14.688/2023) declara hediondos
"os crimes previstos no Decreto-Lei nº 1.001, de 1969 (Código Penal Militar), que
apresentem **identidade** com os crimes previstos no art. 1º desta Lei".
Identidade é juízo de correspondência entre tipos, não remissão a dispositivo —
por isso o CPM está declarado `fora_de_alcance` em `data/hediondos.json`, e estes
sete registros estão marcados como hediondos sem que a máquina possa confirmar.

| id | Artigo | Crime | Correspondente provável no rol |
|---|---|---|---|
| 701 | Art. 205, §2º | Homicídio qualificado | art. 1º, I (homicídio qualificado) |
| 720 | Art. 232, caput | Estupro | art. 1º, V (estupro) |
| 1114 | Art. 232, §1º | Estupro com lesão grave | art. 1º, V |
| 1115 | Art. 232, §2º | Estupro com resultado morte | art. 1º, V |
| 1116 | Art. 232, §3º | Estupro de vulnerável | art. 1º, VI (estupro de vulnerável) |
| 1126 | Art. 244, caput | Extorsão mediante sequestro | art. 1º, IV |
| 1345 | Art. 290, §5º | Tráfico de drogas em lugar sujeito à administração militar | equiparado (CF, art. 5º, XLIII) |

**Ao responder:** se a identidade se confirma, o registro fica como está e a
justificativa entra numa tabela própria em `data/hediondos.json` (bloco
`pendentes`), para que a auditoria pare de tratar o CPM como fora de alcance. Se
não se confirma, o campo vira `Não`. Falta ainda decidir se os **demais** crimes
militares com correspondência (roubo, extorsão, lesão gravíssima) deveriam estar
marcados e não estão.

## 5. Domínio social estruturado (Lei 15.358/2026)

**Pergunta:** qual diploma é o "marco legal do combate ao crime organizado" a que
o inciso VIII do parágrafo único do art. 1º da Lei 8.072 se refere, e o catálogo
já registra seus arts. 2º e 3º?

O inciso, incluído pela Lei 15.358/2026, declara hediondos "os crimes de domínio
social estruturado e de favorecimento ao domínio social estruturado, previstos no
caput e nos §§ 1º e 3º do art. 2º e no art. 3º da lei que institui o marco legal
do combate ao crime organizado no Brasil". A remissão é por **nome**, não por
número — é preciso identificar o diploma.

**Ao responder:** se o diploma existe e tem tipo penal, ele entra em
`data/fontes.json` (o conferidor passa a vigiá-lo toda semana) e os tipos entram
no catálogo; a regra correspondente entra em `data/hediondos.json`.

---
