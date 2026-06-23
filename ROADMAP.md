# Roadmap — algo-pen

## v2 (atual) — GitHub Pages
Site estático com catálogo interativo e calculadora dosimétrica.

- [x] Catálogo de 1.061 tipos penais em JSON
- [x] Interface de busca e filtros combinados
- [x] Calculadora de dosimetria trifásica (Art. 68 CP)
- [x] Estatísticas do catálogo
- [x] Responsivo (mobile-first)
- [x] Zero dependências externas
- [ ] Expandir catálogo para ~1.688 tipos (cobertura SISPENAS completa)
- [ ] Calculadora de progressão de regime (Art. 112 LEP)
- [ ] Calculadora de prescrição (Arts. 109-119 CP)
- [ ] Concurso de crimes (material, formal, continuado)
- [ ] Geração de texto jurídico fundamentado (minutas)

---

## v2.5 — Automação e Governança

Crawler automatizado + IA para manter o catálogo atualizado com segurança jurídica.

- [ ] Crawler do Diário Oficial da União (DOU) — execução semanal via GitHub Actions
- [ ] Agente IA (Claude/GPT) que identifica alterações na legislação penal
- [ ] Atualizações propostas via Pull Request (nunca diretamente no main)
- [ ] Esteira de CI com validação:
  - Penas dentro de intervalos razoáveis
  - Referências cruzadas consistentes
  - Sem duplicatas
  - Classificação de hediondos conforme Lei 8.072/90
- [ ] Revisão obrigatória por pessoa com competência jurídica + técnica
- [ ] Geração automática de changelog

---

## v3 — Sistema web completo

API REST pública + frontend avançado.

- [ ] Backend (Node.js ou Python/FastAPI) com API REST pública
- [ ] Autenticação (OAuth2) para funcionalidades avançadas
- [ ] Banco de dados relacional (PostgreSQL)
- [ ] Histórico de alterações legislativas (quando cada tipo penal mudou, foi criado ou revogado)
- [ ] Busca avançada com NLP (linguagem natural: "qual a pena para quem rouba com arma de fogo?")
- [ ] Versionamento temporal (visualizar o estado da legislação em qualquer data passada)
- [ ] API de consulta para integração com outros sistemas jurídicos
- [ ] Documentação OpenAPI (Swagger)

---

## v4 — Plataforma integrada

Ferramenta completa para prática forense e pesquisa de políticas públicas.

- [ ] Simulação de alteração legislativa (ex: "o que acontece se aumentar a pena do furto em 2 anos?")
- [ ] Cruzamento exaustivo de tipos penais com benefícios (12 benefícios SISPENAS)
- [ ] Dashboards analíticos:
  - Distribuição de penas por gravidade
  - Evolução temporal do endurecimento/abrandamento penal
  - Proporção hediondos/não-hediondos por década
- [ ] Dados abertos para pesquisa acadêmica (CSV, JSON, GraphQL)
- [ ] Módulo de prática forense:
  - Gerador de petições (dosimetria fundamentada)
  - Cálculo de detração e remição
  - Simulação de progressão de regime
  - Alertas de prescrição
- [ ] Integração com bases públicas (DATAJUS, CNJ)
- [ ] Colaboração multiusuário (propostas de correção pela comunidade jurídica)

---

## Contribuição

Contribuições são bem-vindas! Veja o README para instruções. Priorize:
1. Expansão do catálogo (novos tipos penais)
2. Correção de dados (penas incorretas, classificações erradas)
3. Novas calculadoras (progressão, prescrição, concurso)
