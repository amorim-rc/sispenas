# algo-pen

**Catálogo exaustivo de tipos penais brasileiros e calculadora de dosimetria penal.**

Ferramenta de dupla vocação: **prática forense** (advogados criminalistas) e **pesquisa de políticas públicas** (acadêmicos, legisladores, organizações de direitos humanos).

---

## Cobertura atual

| Métrica | Valor |
|---------|-------|
| Tipos penais granularizados | 1.061 |
| Diplomas legislativos | 65 |
| Crimes hediondos | 104 |
| Com violência | 233 |
| Com grave ameaça | 106 |

Inclui: Código Penal, Código Penal Militar, Lei de Drogas, Estatuto do Desarmamento, CTB, ECA, Lei Maria da Penha, Crimes Ambientais, Lei de Tortura, Organização Criminosa, Lavagem de Dinheiro, Crimes contra a Ordem Tributária, Código Eleitoral, Lei de Licitações, Estatuto do Idoso, Estatuto da PcD, Lei de Transplantes, Lei de Terrorismo, e mais 47 diplomas.

Legislação atualizada até junho/2026 (feminicídio autônomo, fraude eletrônica, criptoativos, injúria racial, Lei Henry Borel, golpe de Estado, stalking, bullying/cyberbullying, Lei Sansão).

---

## Funcionalidades

### Catálogo
- Busca por nome do crime, artigo ou diploma
- Filtros combinados: lei, hediondo, elemento subjetivo, violência/grave ameaça, tipo de pena
- Ordenação por qualquer coluna
- Paginação
- Destaque visual: rosa = hediondo, amarelo = violência

### Dosimetria Trifásica (Art. 68 CP)
- Seleção do tipo penal com busca
- 1ª Fase: circunstâncias judiciais (Art. 59)
- 2ª Fase: agravantes e atenuantes
- 3ª Fase: causas de aumento e diminuição
- Resultado: pena definitiva, regime inicial, cabimento de substituição/sursis/ANPP

### Estatísticas
- Cards de resumo (total, hediondos, violência, etc.)
- Distribuição por lei

---

## Tecnologia

| Componente | Escolha | Justificativa |
|---|---|---|
| Hosting | GitHub Pages | Gratuito, CI integrado, versionamento |
| Banco de dados | JSON estático (`data/crimes.json`) | Rápido, versionável, sem servidor |
| Frontend | HTML + CSS + JavaScript vanilla | Zero dependências, leve, universal |
| Responsividade | CSS Grid + Flexbox + media queries | Mobile-first |

**Zero dependências externas.** Nenhum framework, CDN, ou build step necessário.

---

## Estrutura

```
algo-pen/
├── index.html          # Interface principal (SPA com 3 abas)
├── data/
│   └── crimes.json     # Catálogo — fonte de verdade (530 KB)
├── js/
│   └── app.js          # Lógica completa (~300 linhas)
├── css/
│   └── style.css       # Estilos responsivos
├── README.md
├── LICENSE
└── ROADMAP.md
```

---

## Como usar

### Online (GitHub Pages)
Acesse: `https://amorim-rc.github.io/algo-pen/` *(após ativar Pages)*

### Localmente
```bash
git clone https://github.com/amorim-rc/algo-pen.git
cd algo-pen
# Qualquer servidor HTTP estático serve:
python3 -m http.server 8000
# Abra http://localhost:8000
```

---

## Ativar GitHub Pages

1. Vá em **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / **(root)**
4. Clique **Save**
5. Em ~1 minuto, o site estará em `https://amorim-rc.github.io/algo-pen/`

---

## Metodologia

Inspirado no SISPENAS (Machado & Machado, 2008). Cada "tipo penal" é definido como uma conduta com cominação de pena própria — incluindo formas simples, qualificadas, privilegiadas, culposas, e cada inciso/alínea que gere pena autônoma.

**Fontes**: textos legislativos oficiais (planalto.gov.br), jurisprudência consolidada (STF/STJ), doutrina majoritária.

---

## Inspiração e Créditos

- SISPENAS — Machado, M. R. de A.; Machado, M. R. (2008). *Sistema Integrado de Penas*. Revista Jurídica, Brasília, v. 10, n. 90.
- Código Penal Brasileiro (Decreto-Lei nº 2.848/1940)
- Código Penal Militar (Decreto-Lei nº 1.001/1969)
- Lei de Execução Penal (Lei nº 7.210/1984)

---

## Licença

MIT — veja [LICENSE](LICENSE).
