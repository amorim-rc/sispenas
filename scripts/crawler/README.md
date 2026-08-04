# O conferidor

Toda segunda-feira, 05:00 de Brasília, o repositório se pergunta se o catálogo
ainda corresponde à lei. Baixa os textos compilados dos 63 diplomas de
`data/fontes.json`, estrutura cada dispositivo, lê as molduras penais, compara
com `static/data/crimes.json` e olha o DOU da semana em busca de lei penal nova.

O resultado sai em dois canais: **uma issue** com tudo que precisa de gente e,
quando há correção inequívoca, **um PR** aberto pelo próprio robô.

É determinístico de ponta a ponta — sem IA, sem inferência. Onde não há leitura
segura, o achado vira pergunta na issue em vez de virar dado.

## Os módulos

| Arquivo | O que faz |
|---|---|
| `baixar.py` | Fetch dos compilados. Detecta codificação (BOM → meta → UTF-8 → cp1252) e valida a **sentinela** de cada fonte: página sem ela reprova, em vez de deixar o differ comparar com texto velho. |
| `parsear.py` | HTML → dispositivos (caput, §§, pena, situação, anotação). Fatia o HTML cru: a árvore do Word malformado desloca as fronteiras de parágrafo. |
| `../pena_parser.py` | Lê a moldura. **Compartilhado com `transform_data.py`**, para que catálogo e conferidor leiam a mesma pena do mesmo jeito. |
| `conferir.py` | O differ. Classifica cada achado e escreve `crawler/relatorios/AAAA-MM-DD.md`. Sai com 3 quando há achados. |
| `vigencia.py` | Vacatio legis e produção de efeitos diferida: nunca propor mudança que ainda não vigora. |
| `revogacao.py` | Revogação total de diploma (banner no topo da página). |
| `corrigir.py` | Correção mecânica de linha existente: moldura e espécie de pena. |
| `criar.py` | Linha nova. **Não roda no automático** — ver "o que o robô não faz". |
| `propor.py` | Escolhe o diploma da rodada, aplica, escreve a entrada de changelog, sobe a versão e monta o corpo do PR. |
| `auditar.py` | Audita os campos que a conferência de penas não alcança: hediondez (contra `data/hediondos.json`), ação penal, causas de aumento ausentes e nomes — inclusive o nome que descreve MELHOR outro artigo do mesmo diploma, ponto cego da conferência de molduras. Repete também os títulos das perguntas de `REVISAO-PENDENTE.md`. |
| `dou_watcher.py` | Filtro semanal da Seção 1 do DOU, para achar lei penal **nova e autônoma**. Tria em três níveis pelo preceito secundário; o descartado sai nomeado, não some. |
| `excecoes.json` | O que já foi julgado e decidido na conferência de PENAS. Sem isso o relatório repetiria para sempre os mesmos achados. |
| `excecoes-auditoria.json` | O mesmo, para a auditoria de classificação. Arquivo próprio porque as chaves são outras: ora o id do registro, ora o dispositivo do compilado. |
| `../verificar_documentacao.py` | Saúde da prosa: documento vence por prazo ou porque algo de que ele fala mudou depois da última conferência. |
| `tempo.py` | A data de Brasília. O runner roda em UTC, e sem isso a rodada das 21h se datava de amanhã. |

## Rodar à mão

```bash
python scripts/crawler/baixar.py --todas          # ou --fonte cp
python scripts/crawler/conferir.py                # relatório de tudo
python scripts/crawler/conferir.py --carimbar     # + trilha em data/conferencia.json
python scripts/crawler/propor.py                  # o PR que sairia (não escreve)
python scripts/crawler/dou_watcher.py --dias 8
python -m pytest scripts/crawler/tests            # sem rede, contra fixtures
```

O workflow também roda sob demanda: aba **Actions** → "Conferidor semanal" →
**Run workflow**, com opção de não abrir PR e de incluir linhas novas.

## O que o robô faz e o que não faz

**Faz**, sozinho, direto na `main`: carimba a trilha de auditoria
(`data/conferencia.json` → `fonte`, `conferido_em` e `conferido_resultado` no derivado).
É registro do que a máquina fez, não proposta de mudança de dado.

**Faz**, sozinho, em PR: corrigir moldura ou espécie de pena de linha que já
existe, quando o compilado diz outra coisa. Um diploma por rodada, um PR aberto
por vez, evidência por mudança, e o PR fecha uma versão (sobe `package.json` e
`CITATION.cff`, e escreve a entrada do changelog).

**Faz**, em PR que PEDE JUÍZO: as mudanças de hediondez e ação penal, com o fundamento ao lado, e a entrada de `data/fontes.json` para lei nova que pareça criar tipo penal. Só sai quando não há correção de pena pendente — uma coisa por rodada.

**Não faz**: criar nem remover linha. Criar exige decidir se o dispositivo é
crime autônomo, causa de aumento ou nada; remover exige decidir o destino da URL
pública. `criar.py` existe e é útil, mas rodado por gente — a primeira leva
automática dele (v1.3.0) trouxe 29 registros que não eram tipos penais vigentes,
e foi preciso retirá-los na v1.4.0.

## As armadilhas que já custaram caro

Cada uma tem teste e fixture; nenhuma volta em silêncio.

1. **Texto citado.** O compilado transcreve, embaixo do artigo alterador, a
   redação dada à lei alterada — e congelada na data da alteração. A Lei 8.137
   "contém" o art. 172 do CP; a Lei 12.850 "contém" o art. 288. Duas formas de
   detectar: o texto do caput ("passa a vigorar…") e o número fora de sequência
   ("Art. 24, Art. 288, Art. 25").
2. **Espécie que não é pena.** Preceito que começa por "Pena - multa" é multa,
   mesmo que fale em suspensão ou fechamento depois do ponto e vírgula.
3. **Revogação que mantém o texto.** A LCP não apaga o corpo do artigo revogado:
   anota a revogação ao lado.
4. **Espécie alternativa.** "reclusão ou detenção, de um a três anos" é uma
   moldura com duas espécies, não duas molduras.
5. **Rótulo pela lei criadora.** Artigos do CP aparecem com `lei="Lei 14.811/24"`.
   O vínculo diploma → rótulos vem de `fontes.json`, nunca do campo `lei` cru.
6. **Comparar com o DERIVADO.** A moldura que a aplicação usa é
   `pena_*_meses`, do derivado — os campos crus da fonte podem estar velhos.
7. **Codificação.** O acervo do Planalto mistura cp1252 e UTF-16 com BOM.
   "Página parece desatualizada" quase sempre é erro de decodificação.
8. **`Art . 190`**, com espaço antes do ponto, é como a Lei 6.766 escreve do
   art. 37 em diante.
9. **Sufixo de letra.** Vem colado ao número, pode repetir-se (`359-M-B`) e pode
   vir depois do ordinal (`2º-A`). Sem as duas formas, o `2º-A` da Lei 7.716
   (injúria racial) virava corpo do art. 2º, que está vetado, e o `359-M-B` do
   CP virava corpo do golpe de Estado. Em contrapartida, `Art. 13 - O resultado`
   **não** tem sufixo: ali o hífen é pontuação e o `O` é artigo definido — foi
   assim que nasceram artigos inexistentes como `Art. 13-O` e `Art. 100-A`. A
   regra que separa os dois casos é o espaço em volta do hífen, e ela precisa
   valer igual em `parsear.py` e na `chave()` de `conferir.py`: os dois lados
   têm de reduzir ao MESMO identificador, senão o registro existe e não é
   conferido.

## Acrescentar um diploma

Uma entrada em `data/fontes.json` (`id`, `rotulos`, `url` do compilado,
`sentinela` — uma string que prova que a página está fresca). O conferidor passa
a vigiá-lo na rodada seguinte, e o watcher do DOU passa a reconhecer citações a
ele. Todo rótulo distinto de `data/crimes.json` precisa constar de exatamente um
diploma.
