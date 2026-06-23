# E-mail para as autoras do SISPENAS

**Assunto:** Evolução prática do conceito SISPENAS — convite ao diálogo

---

Prezadas Professoras Maíra e Marta,

Meu nome é [nome]. Sou filósofo de formação pela UFPE, atualmente estudante de Direito, e trabalho no ecossistema de tecnologia há três anos. Escrevo para apresentar um projeto que nasceu diretamente inspirado pelo SISPENAS, publicado na Revista Jurídica da Presidência (v. 10, n. 90, 2008), e para explorar possibilidades de diálogo e colaboração.

**O problema que me motivou é o mesmo que motivou vocês em 2007**: a inacessibilidade do sistema de penas e alternativas no ordenamento brasileiro. Como estudante de Direito que veio da tecnologia, a primeira coisa que me ocorreu ao estudar dosimetria penal foi: "por que isso não está sistematizado numa ferramenta funcional?"

Ao pesquisar, encontrei o artigo do SISPENAS — e constatei que vocês já haviam diagnosticado e atacado esse problema com rigor acadêmico notável. Contudo, o sistema aparentemente nunca foi disponibilizado ao público. Não o encontrei online para testar.

**O que construí até agora:**

Uma ferramenta funcional de dosimetria penal e consulta legislativa, já operacional, com dupla vocação — prática forense (para advogados criminalistas) e pesquisa de políticas públicas (para acadêmicos e legisladores):

- **Catálogo unitário de 529 tipos penais** de 53 diplomas legislativos, cada um com: pena mín/máx, tipo de pena, ação penal, classificação de hediondo, elemento subjetivo (doloso/culposo/preterdoloso), admissibilidade de tentativa, qualificadoras/majorantes/minorantes, e observações com jurisprudência relevante
- **Catálogo granularizado de 822 variantes de tipos penais** de 62 diplomas, seguindo a metodologia SISPENAS — cada variante (simples, qualificado, privilegiado, culposo, com aumento, etc.) é um registro autônomo com intervalo de pena próprio. Inclui o Código Penal Militar, campos de violência e grave ameaça como elementares, e cruzamento automático com 3 benefícios penais (ANPP, sursis processual, sursis da pena). Cobertura: 79 hediondos, 182 com violência, 89 com grave ameaça
- **Dosimetria trifásica completa** (Art. 68 CP): 8 circunstâncias judiciais do Art. 59 com cálculo automático, agravantes/atenuantes (Arts. 61-66), e causas de aumento/diminuição com frações editáveis
- **Progressão de regime** atualizada pelo Pacote Anticrime (2019): todas as frações do Art. 112 LEP (16% a 70%), com cálculo de datas estimadas
- **Prescrição** (Arts. 109-119 CP): abstrata, retroativa, com marcos interruptivos e redução do Art. 115
- **Concurso de crimes** (Arts. 69-71 CP): material, formal, continuado — com comparação automática do mais favorável ao réu
- **Detração e remição**, prazos processuais, multa, ANPP (Art. 28-A CPP), sursis processual e da pena
- **Geração automática de textos fundamentados**: petições de progressão, livramento condicional, alegação de prescrição, excesso de prazo — todos com citação de artigos e cálculos preenchidos automaticamente

**Por que escrevo para vocês:**

1. **Reconhecimento**: o SISPENAS é o trabalho seminal neste campo no Brasil. O meu projeto é, conscientemente, uma evolução prática do conceito que vocês conceberam.

2. **Complementaridade**: o SISPENAS foi desenhado para formuladores de políticas públicas e pesquisadores; meu sistema começou voltado para advogados criminalistas. Estou agora reorientando o projeto para servir a ambos os públicos — prática forense *e* pesquisa de políticas públicas. O cruzamento automático de tipos penais com benefícios que vocês implementaram é exatamente o tipo de funcionalidade que estou expandindo (atualmente 3 benefícios; objetivo de alcançar os 12 que vocês mapearam).

3. **Roadmap**:
   - **v1 (atual)**: Ferramenta funcional com dois catálogos (unitário e granularizado), dosimetria completa, progressão, prescrição e geração de textos jurídicos
   - **v2**: Site público (GitHub Pages) servindo dados curados, com crawler automatizado do Diário Oficial da União integrado com inteligência artificial para identificar alterações na legislação penal e propor atualizações automaticamente, com esteira de CI/CD monitorada por pessoa com competência jurídica e técnica — um MVP web com governança robusta
   - **v3**: Sistema web completo com API pública e interface acessível
   - **v4**: Plataforma integrada de prática forense e pesquisa de políticas públicas — com simulação de alteração legislativa, cruzamento exaustivo de tipos com benefícios, e dados abertos para pesquisa acadêmica

4. **Perguntas que gostaria de fazer**:
   - Qual é o estado atual do SISPENAS? O banco de dados (1.529 tipos à época) ainda existe em alguma forma acessível?
   - O código-fonte entregue à SAL/MJ chegou a ser implantado em algum momento?
   - Há interesse em colaboração para que a pesquisa de 2008 encontre, enfim, aplicação pública e permanente?
   - Conhecem iniciativas similares em andamento no Brasil ou no exterior que eu deveria conhecer?

Terei prazer em apresentar o sistema em funcionamento e discutir como podemos fazer esse trabalho avançar — seja como colaboração acadêmica, como projeto de extensão, ou como proposta para um edital do "Pensando o Direito", que entendo continuar ativo.

Agradeço imensamente pelo trabalho pioneiro que realizaram. Espero que este contato seja o início de um diálogo produtivo.

Cordialmente,