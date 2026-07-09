# Agenda de Pesquisa — Direito Penal & Tecnologia

**Objetivo:** transformar 12 intuições em linhas de pesquisa/teses/artigos com densidade dogmática, legal, factual e tecnológica. Para cada tópico: pergunta de pesquisa, núcleo dogmático, âncoras normativas/jurisprudenciais, dimensão tecnológica e um **ângulo argumentativo defensável** (a tese que renderia um artigo forte). Ao final, refino/reagrupo e proponho tópicos novos.

> **Nota de método:** as âncoras legais e casos citados servem de ponto de partida — antes de publicar, valide texto vigente de cada dispositivo e a jurisprudência atualizada (leis penais/processuais mudam e teses caem). Este documento é mapa, não peça final.

---

## Eixo A — Bem jurídico, tipicidade e o objeto material digital

### 1. Coisa móvel, dados e a (in)subtração no furto digital

**Pergunta:** o dado puro (arquivo, registro de banco de dados, criptoativo) pode ser "coisa alheia móvel" para fins do art. 155 CP? A *cópia* não-destrutiva — em que o titular não perde o acesso — é subtração ou algo atípico como furto?

**Núcleo dogmático:**
- Furto exige *coisa* (corpórea, tradicionalmente) + *alheia* + *móvel* + *subtração* (=inversão da posse com desapossamento do dono). A cópia rompe justamente o elemento "desapossamento": o dado permanece com a vítima. Isso desloca a conduta para outros tipos (interceptação, invasão de dispositivo, violação de segredo, apropriação) ou revela lacuna.
- Distinguir três objetos: (a) **dado como informação** (incorpóreo — resiste à ideia de "coisa móvel"); (b) **criptoativo** (tem valor econômico e transferência com desapossamento efetivo — aqui *há* subtração real, aproxima-se de coisa/valor); (c) **conteúdo de banco de dados** copiado (sem desapossamento — atipicidade quanto ao furto).
- Confronto com a energia elétrica (art. 155, §3º equipara "energia... com valor econômico" a coisa móvel): argumento analógico *a favor* de equiparar o dado — mas esbarra na **vedação de analogia in malam partem**. Ponto nevrálgico do artigo.

**Âncoras:** art. 155 e §3º CP; Lei 12.737/2012 (art. 154-A — invasão de dispositivo); Lei 14.155/2021 (furto mediante fraude por meio eletrônico — §4º-B, e estelionato eletrônico art. 171 §2º-A); crimes contra a propriedade imaterial. Direito comparado: *theft of information* (common law) e a resistência histórica em enquadrar informação como *property*.

**Dimensão tecnológica:** natureza não-rival da informação (copiável sem perda para a origem) vs. natureza rival do criptoativo (UTXO/saldo: transferir = perder). Isso é *o* dado técnico que decide a subsunção.

**Ângulo defensável:** *a cópia de dados sem desapossamento é atípica como furto e o recurso à equiparação da "energia" é analogia in malam partem vedada — o legislador (12.737 e 14.155) reconheceu isso ao criar tipos próprios; criptoativo, ao contrário, admite furto porque há desapossamento efetivo.* Tese com forte apelo garantista.

### 3. Invasão de dispositivo físico conectado (IoT)

**Pergunta:** o art. 154-A CP ("dispositivo informático") alcança geladeira, fechadura, marca-passo, câmera, carro conectado? O bem jurídico protegido (intimidade/dados) é suficiente quando a invasão de um IoT gera risco à **integridade física** ou à **segurança**?

**Núcleo dogmático:**
- 154-A tutela primordialmente **privacidade/segurança de dados**. IoT desloca o resultado para o **mundo físico** (abrir fechadura, desativar freio, alterar dosagem de bomba de insulina). Surge a questão do **concurso** (154-A + lesão/homicídio/dano/perigo) e da eventual **subsidiariedade**.
- Discussão de **crime de perigo** vs. dano; dolo de invadir vs. dolo do resultado físico; se o 154-A vira crime-meio absorvido (consunção) quando o fim é lesão corporal, ou se há concurso material.
- "Dispositivo informático" como conceito — interpretação teleológica: todo objeto com capacidade de processamento e conectividade. Risco de tipicidade aberta.

**Âncoras:** art. 154-A e §§ (com redação da Lei 14.155/2021, que ampliou pena e abrangência); arts. 129, 132 (perigo), 163 (dano); Marco Civil (Lei 12.965/2014); regulação de segurança de produtos.

**Dimensão tecnológica:** superfície de ataque de IoT (firmware desatualizado, protocolos inseguros, ausência de update), *lateral movement* de um dispositivo a outro, e a diferença entre invadir o dado e comandar o atuador físico.

**Ângulo defensável:** *quando a invasão de IoT tem por fim ou resultado a ofensa à integridade física/segurança, o 154-A é crime-meio e a proteção penal deve migrar para o tipo do resultado — sob pena de subproteção do bem jurídico realmente atingido.*

---

## Eixo B — Autoria, imputação e a máquina que "decide"

### 2. Autoria e imputação em sistemas autônomos (IA/algoritmos)

**Pergunta:** quando um sistema autônomo causa um resultado lesivo (atropelamento por veículo autônomo, dano por decisão algorítmica, discriminação automatizada), a quem se imputa? Programador, fabricante, operador, "treinador" dos dados, usuário? Há espaço para responsabilidade penal da pessoa jurídica ou é sempre pessoa física?

**Núcleo dogmático:**
- Direito penal exige **conduta humana** dolosa ou culposa e **nexo de imputação**. A máquina não é sujeito de culpabilidade. O problema real é a **dispersão da autoria** e o **"responsibility gap"**: muitas mãos, nenhuma com domínio do fato no instante do resultado.
- Ferramental: **crimes culposos** (violação de dever de cuidado no design/teste/deploy), **imputação objetiva** (criação de risco proibido, fim de proteção da norma), **autoria mediata** (o operador que usa o sistema como instrumento?), **posição de garante** (fabricante/desenvolvedor com dever de vigilância e recall) e **culpa consciente vs. dolo eventual** em quem faz deploy sabendo do viés.
- Recusar antropomorfismo ("IA culpada") e evitar responsabilidade objetiva penal (vedada). O eixo é *dever de cuidado* distribuído e sua violação identificável.

**Âncoras:** arts. 13 (nexo/omissão imprópria), 18 (dolo/culpa) CP; teoria da imputação objetiva (Roxin); debates da Resolução do Parlamento Europeu sobre robótica; AI Act (UE) — categorização de risco; discussões de *Verbandsstrafrecht* (responsabilidade penal empresarial).

**Dimensão tecnológica:** opacidade de modelos (black box), aprendizado contínuo pós-deploy (o sistema muda depois de sair das mãos do dev), papel dos dados de treino na produção do viés, rastreabilidade/logging como prova do dever de cuidado.

**Ângulo defensável:** *não há vácuo de responsabilidade: a autonomia técnica não dissolve a autoria, apenas a antecipa para o momento do design/teste/deploy; o critério decisivo é a violação de um dever de cuidado documentável (ausência de teste de viés, de logging, de mecanismo de intervenção humana), imputável a título de culpa — e, quando há ciência do risco e indiferença, de dolo eventual.*

### 10 + 11 + 12. Reconhecimento facial, policiamento preditivo e escores de risco (COMPAS)

*(agrupei os três — formam um bloco coerente sobre "decisão penal por proxy". Ver Eixo D.)*

---

## Eixo C — Território, jurisdição e soberania do dado

### 4. Ubiquidade em xeque: conduta e resultado dispersos (crimes cibernéticos plurilocais)

**Pergunta:** a teoria da ubiquidade (art. 6º CP — lugar do crime é onde ocorreu a ação **ou** o resultado) ainda opera quando conduta, servidor, dado e vítima estão em jurisdições diferentes e simultâneas? Onde se fixa a competência interna (art. 70 CPP) e a jurisdição internacional?

**Núcleo dogmático:**
- Ubiquidade foi pensada para o crime à distância "linear" (tiro na fronteira). No ciber, há **multiplicidade** de loci: local do agente, do servidor de origem, do de trânsito, do de armazenamento, do resultado, da vítima. Isso gera **conflitos positivos** (vários Estados competentes) e risco de *forum shopping*.
- Distinguir **lugar do crime** (art. 6º, direito penal) de **competência processual** (art. 70 CPP, resultado consumado) — o artigo pode explorar a tensão entre os dois.
- Propor critérios de racionalização: **efeito substancial** (onde o dano se concretiza), **direcionamento** (targeting) da conduta, nacionalidade da vítima, localização do dado — inspirados no debate de jurisdição extraterritorial.

**Âncoras:** arts. 5º e 6º CP (territorialidade + ubiquidade), 7º (extraterritorialidade), art. 70 CPP; Convenção de Budapeste (cibercrime) — que o Brasil aderiu (Decreto 11.491/2023); precedentes de conflito de competência no STJ em crimes pela internet.

**Dimensão tecnológica:** CDNs, *sharding* de dados, replicação multirregião, anonimização por VPN/Tor/proxy que embaralha o "local da conduta", e o fato de o dado não ter um único lugar físico.

**Ângulo defensável:** *a ubiquidade clássica é insuficiente e produz sobreposição de jurisdições; propõe-se um critério de conexão substancial (efeito + direcionamento) para conter o forum shopping e compatibilizar a soberania penal com a arquitetura distribuída da rede.*

### 5. Soberania e custódia em nuvem: a urgência probatória vs. a lentidão dos MLATs

**Pergunta:** diante da necessidade urgente de prova armazenada no exterior, o Estado pode exigir dados diretamente do provedor com base/operação no Brasil, contornando o tratado de assistência mútua (MLAT)? Como conciliar soberania estrangeira, devido processo e eficiência?

**Núcleo dogmático:**
- Tensão entre **soberania** (a prova está em servidor sob outra jurisdição) e **efetividade da persecução**. MLATs são lentos (meses/anos); o dado é volátil.
- O caso brasileiro paradigmático: exigências a provedores globais (WhatsApp/Facebook/Google) e a discussão sobre se a **presença econômica no Brasil** basta para obrigar a entrega, mesmo com dado armazenado fora. Debate sobre o **CLOUD Act** (EUA) e o modelo europeu de *e-evidence*.
- Legalidade da coleta como condição de **admissibilidade da prova** (prova obtida por via que viola soberania alheia = risco de ilicitude, art. 157 CPP).

**Âncoras:** Marco Civil arts. 10-11 (guarda e fornecimento de registros; aplicação da lei brasileira a quem oferta serviço no país), art. 157 CPP (prova ilícita); Convenção de Budapeste e seu 2º Protocolo (cooperação direta com provedores); ADCs/ADPKs no STF sobre fornecimento de dados; CLOUD Act e *Microsoft Ireland*.

**Dimensão tecnológica:** localização física vs. lógica do dado, criptografia em repouso, jurisdição do *data center* vs. da controladora, e por que "onde está o dado" é uma pergunta cada vez menos respondível.

**Ângulo defensável:** *a presença econômica sujeita o provedor à ordem brasileira, mas a coleta que ignora a soberania do Estado de armazenamento sem base cooperativa contamina a prova; a saída é fortalecer cooperação direta provedor-Estado (modelo Budapeste II) e não a autotutela probatória extraterritorial.*

---

## Eixo D — Prova penal, integridade e decisão algorítmica

### 6. Cadeia de custódia e hash: integridade matemática como blindagem contra nulidade

**Pergunta:** o hash criptográfico (SHA-256 etc.) é suficiente para garantir a integridade da prova digital e afastar a nulidade? Que falhas na cadeia (arts. 158-A a 158-F CPP) o hash **não** cobre?

**Núcleo dogmático:**
- A Lei 13.964/2019 (Pacote Anticrime) positivou a **cadeia de custódia** (158-A a 158-F CPP), com etapas de coleta, acondicionamento, transporte, análise. Prova digital exige adaptação: **imagem forense** + **hash** na coleta + documentação de cada acesso.
- O hash prova **integridade** (o arquivo não mudou) mas **não prova licitude da origem nem autenticidade da autoria** ("o dado é íntegro, mas foi coletado legalmente? é mesmo do acusado?"). Distinguir integridade × autenticidade × licitude.
- Consequência da quebra: discussão entre **nulidade/inadmissibilidade** (prova ilícita/imprestável) vs. **valoração** (mera mácula que afeta o peso). O artigo pode defender uma teoria da "quebra da cadeia" para o digital.

**Âncoras:** arts. 158-A a 158-F, 157 CPP; jurisprudência do STJ sobre quebra de cadeia de custódia (tendência a reconhecer ilicitude/imprestabilidade conforme a gravidade); normas de perícia digital (ISO/IEC 27037).

**Dimensão tecnológica:** *write-blocker*, imagem bit-a-bit, hashing e re-hashing, *timestamping*, logs de acesso, e o problema da prova em nuvem/live forensics (dado volátil que não permite imagem estática).

**Ângulo defensável:** *o hash é condição necessária mas não suficiente; a integridade matemática não sana vícios de licitude e autenticidade, e a quebra documentada da cadeia no ambiente digital deve conduzir à imprestabilidade da prova, não à mera redução de peso — sob pena de esvaziar os arts. 158-A e ss.*

### 7. Senha do dispositivo apreendido vs. nemo tenetur se detegere

**Pergunta:** o Estado pode compelir o acusado a fornecer a senha/biometria de desbloqueio de dispositivo apreendido, ou isso viola o direito de não produzir prova contra si mesmo? Há diferença entre **senha** (conhecimento) e **biometria** (corpo)?

**Núcleo dogmático:**
- **Nemo tenetur se detegere** protege contra a autoincriminação **ativa** (declarar, colaborar produzindo prova). A jurisprudência distingue: o acusado não pode ser obrigado a *fazer* algo que o incrimine (fornecer senha = ato de fala/conhecimento, protegido), mas pode tolerar intervenções *passivas* sobre seu corpo (coleta de material).
- **Senha × biometria:** senha é conteúdo da mente → tende à proteção (é "testemunhal"). Biometria (digital, face) é dado corporal → argumento de que é intervenção passiva não protegida — mas isso permite ao Estado desbloquear pelo dedo o que não pode pela boca, o que é uma **contradição valorativa** a ser explorada.
- Alternativas do Estado: quebra técnica (exploits, cooperação do fabricante — caso *Apple v. FBI*), que desloca a questão do réu para o provedor.

**Âncoras:** art. 5º, LXIII CF; art. 8º Pacto de San José; jurisprudência do STF/STJ sobre nemo tenetur (recusa a bafômetro, a fornecer material grafotécnico); direito comparado (5ª Emenda EUA — *foregone conclusion doctrine*; casos sobre compelir senha).

**Dimensão tecnológica:** *full-disk encryption*, enclaves seguros (Secure Enclave/TEE), diferença entre desbloquear (senha) e decriptar, e por que sem a senha muitas vezes o dado é matematicamente inacessível.

**Ângulo defensável:** *compelir o fornecimento de senha viola o nemo tenetur porque exige colaboração testemunhal ativa; e a distinção senha/biometria é insustentável quando ambas destravam o mesmo conteúdo — a proteção deve alcançar também o desbloqueio biométrico compelido, sob pena de fraude à garantia.*

### 12. Escores de risco (COMPAS) na prisão preventiva e fiança — punindo o proxy

**Pergunta:** pode um sistema de escore de risco fundamentar (ou influenciar) decisão sobre prisão preventiva/fiança? Ao usar *proxies* (endereço, renda, histórico do bairro), o sistema pune vulnerabilidade social sob o disfarce de "probabilidade estatística"?

**Núcleo dogmático:**
- Preventiva exige **fundamentação concreta** (art. 312 CPP: garantia da ordem pública, instrução, aplicação da lei + periculum) e é medida **cautelar individual**, não atuarial. Escore estatístico é **prognose de grupo** aplicada ao indivíduo → colide com **individualização** e **presunção de inocência**.
- **Proxies discriminatórios:** variáveis correlacionadas a raça/classe reintroduzem viés vedado por via "neutra". Viola isonomia e o **direito penal do fato** (pune-se o que a pessoa *é*/onde vive, não o que fez → resvala em direito penal do autor).
- **Fundamentação e contraditório:** decisão baseada em caixa-preta é infundamentada (viola art. 93, IX CF) e impede o contraditório (não se pode refutar um escore cujo cálculo é opaco/segredo comercial).

**Âncoras:** arts. 312-315 CPP (fundamentação da cautelar), art. 93, IX CF (motivação), presunção de inocência (art. 5º, LVII CF); caso *State v. Loomis* (Wisconsin/COMPAS); estudo ProPublica sobre viés racial do COMPAS; LGPD art. 20 (revisão de decisão automatizada) e sua (in)aplicação ao processo penal.

**Dimensão tecnológica:** o que é um escore de recidiva, por que a "acurácia global" mascara **desigualdade de taxas de erro entre grupos** (falsos positivos concentrados em negros/pobres), e o problema do *proxy* e da **impossibilidade de fairness simultânea** (impossibility theorems: não dá para satisfazer todos os critérios de justiça ao mesmo tempo).

**Ângulo defensável:** *escore atuarial é incompatível com a cautelar penal: converte prognose de grupo em prisão individual, reintroduz viés por proxy e produz decisão infundamentada e não-contraditável — sua adoção viola presunção de inocência, individualização e o dever de motivação, configurando direito penal do autor disfarçado de estatística.* (Tese forte e atual.)

### 10 + 11. Reconhecimento facial e policiamento preditivo — vigilância, viés e finalidade do Direito Penal

**Pergunta:** o reconhecimento facial (com taxas de erro maiores para pessoas negras) e o policiamento preditivo (predizer *onde*/*quem*) são compatíveis com as garantias penais e com a **função** do direito penal (proteção subsidiária de bens jurídicos, não gestão atuarial de populações)?

**Núcleo dogmático:**
- **Reconhecimento facial:** prova/indício produzido por sistema enviesado → risco de **erro judiciário** e de abordagem/prisão baseada em *match* falso. Discussão de **standard probatório** (um match biométrico é indício, não prova plena), de cadeia de custódia do reconhecimento e da vedação a reconhecimento pessoal viciado (diálogo com art. 226 CPP e a virada do STJ sobre reconhecimento).
- **Policiamento preditivo:** desloca o penal do **fato passado** para o **risco futuro** → tensão com o **direito penal do fato** e com a subsidiariedade; cria *feedback loops* (mais policiamento onde já se policiava → mais registros → confirmação do viés).
- **Finalidade do direito penal:** se o fim é proteger bens jurídicos e reprovar condutas, a lógica **preventivo-atuarial** (gerir populações de risco) representa mutação para um **direito penal do inimigo/gerencial** — o cerne crítico do artigo 11.

**Âncoras:** art. 226 CPP e jurisprudência recente do STJ sobre invalidade de reconhecimento sem observância do rito; LGPD e o debate sobre dados biométricos como sensíveis (art. 5º, II); ADPF sobre câmeras/reconhecimento; literatura de criminologia atuarial (Feeley & Simon, "new penology"); vieses documentados (NIST FRVT mostra disparidade racial em taxas de erro).

**Dimensão tecnológica:** como funciona *face matching* (embeddings + limiar de similaridade), por que a taxa de falso positivo varia por fenótipo (dados de treino desbalanceados), e o que é um sistema de *hotspot policing*.

**Ângulo defensável:** *reconhecimento facial e policiamento preditivo importam a lógica atuarial para dentro do penal, deslocando-o do fato para o risco e do indivíduo para o grupo — o que é incompatível com o direito penal do fato, a presunção de inocência e a função de proteção subsidiária de bens jurídicos; como prova, o match biométrico enviesado não supera o standard exigido e amplia o risco de erro judiciário sobre populações já vulnerabilizadas.*

---

## Eixo E — Processo penal, oralidade e presença

### 8. Descorporificação do rito: audiências remotas em massa e o princípio da oralidade/imediação

**Pergunta:** a virtualização massiva de audiências preserva a **imediação**, a **oralidade** e a **identidade física do juiz**, ou as esvazia? Há um limite constitucional para a "audiência sem corpo"?

**Núcleo dogmático:**
- **Imediação** (contato direto do juiz com a prova/pessoas) e **oralidade** são pilares do processo penal. A tela **medeia** e filtra — perde-se linguagem corporal, a espontaneidade, o "olho no olho". Questão: eficiência × qualidade epistêmica da prova oral.
- Direito de **presença** do acusado e de **entrevista reservada** com o defensor (comprometida quando réu e advogado estão em locais diferentes na videoconferência). Debate sobre **nulidade** por cerceamento de defesa.
- Distinguir atos: interrogatório (mais sensível — direito de presença e de autodefesa) vs. oitivas técnicas.

**Âncoras:** arts. 185, 217 CPP (interrogatório e videoconferência excepcional), Lei 11.900/2009 (regras da videoconferência — *excepcionalidade*), CF art. 5º (ampla defesa, contraditório); resoluções do CNJ pós-pandemia que ampliaram o remoto; jurisprudência sobre nulidade por falta de entrevista reservada.

**Dimensão tecnológica:** latência/queda de conexão, deepfake/adulteração de vídeo, ausência de garantia de sala neutra, e o problema de gravação/segurança do ato.

**Ângulo defensável:** *a videoconferência é exceção legal (Lei 11.900/2009) e sua banalização inverte a regra da presença física; o interrogatório remoto sem entrevista reservada e sem controle do ambiente viola a ampla defesa e degrada a imediação — a eficiência não é base constitucional para suprimir a corporalidade do ato.*

### 9. A testemunha remota sob coação invisível: garantias da prova oral por vídeo

**Pergunta:** como assegurar, na oitiva por vídeo, que a testemunha depõe livre de coação, consulta a terceiros ou leitura de roteiro fora de quadro? A impossibilidade de controlar o ambiente compromete a validade do depoimento?

**Núcleo dogmático:**
- A oitiva presencial permite controlar o ambiente (incomunicabilidade de testemunhas, art. 210 CPP; ausência de sopro externo). No remoto, o **fora-de-quadro** é um ponto cego: alguém coagindo, um roteiro na parede, um celular com instruções.
- Confiabilidade epistêmica do depoimento e **incomunicabilidade** (art. 210) tornam-se inverificáveis → risco à **busca da verdade** e ao contraditório.
- Propor **protocolos de garantia**: câmera 360º/varredura do ambiente, presença de servidor no local, identificação, câmera que capte as mãos, etc. Artigo pode ser propositivo (lege ferenda).

**Âncoras:** arts. 210, 217, 218 CPP; regras do CNJ para atos por videoconferência; princípio da incomunicabilidade das testemunhas.

**Dimensão tecnológica:** técnicas antifraude em videoconferência (detecção de segunda tela, análise de direção do olhar), risco de deepfake, e limites práticos de fiscalizar um ambiente que não é o do juízo.

**Ângulo defensável:** *sem protocolos técnicos de controle do ambiente, a oitiva remota não assegura a incomunicabilidade (art. 210) nem a espontaneidade do depoimento, fragilizando a prova oral; a validade do ato deve condicionar-se a garantias mínimas verificáveis, sob pena de nulidade por comprometimento do contraditório.*

---

## Reagrupamento sugerido (para virar produção acadêmica coerente)

Os 12 tópicos organizam-se em **5 eixos** que já podem ser 5 artigos ou os capítulos de uma obra/tese maior sobre "Direito Penal na era digital":

| Eixo | Tópicos | Tese unificadora |
|------|---------|------------------|
| **A. Objeto material digital** | 1, 3 | Os tipos clássicos (coisa móvel, dispositivo) precisam de reinterpretação teleológica sem violar a legalidade |
| **B. Autoria e a máquina** | 2 (+ conexão com 12) | Autonomia técnica não cria vácuo de responsabilidade — desloca a autoria para o dever de cuidado no design |
| **C. Território e soberania** | 4, 5 | A arquitetura distribuída da rede exige novos critérios de jurisdição e cooperação probatória |
| **D. Prova e decisão algorítmica** | 6, 7, 10, 11, 12 | Integridade ≠ licitude; e a decisão penal por proxy/estatística viola garantias fundamentais |
| **E. Processo descorporificado** | 8, 9 | A virtualização não pode suprimir imediação, presença e incomunicabilidade sem custo constitucional |

**Sugestão de "carro-chefe" (maior impacto/atualidade):** o **Eixo D** — especialmente os tópicos **7 (senha × nemo tenetur)** e **12 (COMPAS/escore na cautelar)** — são os mais quentes, com jurisprudência viva e forte apelo garantista. Bom ponto de partida para um primeiro artigo publicável.

---

## Tópicos novos (não estavam na sua lista)

1. **Deepfake como meio de execução** — calúnia/difamação, falsa identidade, extorsão com vídeo/áudio sintético; e deepfake como **prova forjada** (impacto na cadeia de custódia e no standard probatório). Tese: necessidade de repensar a *autenticidade* da prova audiovisual num mundo em que "ver não é mais crer".
2. **Criptoativos, lavagem e confisco** — rastreabilidade da blockchain vs. mixers/privacy coins; possibilidade e limites do **confisco** de cripto (art. 91 CP; Lei 9.613/98); custódia de ativos apreendidos.
3. **Ransomware e a (a)tipicidade do pagamento de resgate** — extorsão (art. 158), dano, e a posição de quem paga; deveres de reporte (LGPD/ANPD) e o crime de organização criminosa.
4. **Responsabilidade penal por conteúdo gerado por IA** (incitação, apologia, pornografia infantil sintética — art. 241 ECA) — o material sintético "sem vítima real" é típico? (tende a sim — bem jurídico é a proteção difusa e o fomento ao mercado).
5. **Vigilância por dados e "prova derivada" de wearables/IoT doméstico** (Alexa, smartwatch, dados de saúde) — admissibilidade, expectativa de privacidade e a *third-party doctrine* à brasileira.
6. **Direito ao silêncio algorítmico / decisões automatizadas no inquérito** — uso de IA pela própria acusação (triagem de casos, priorização) e o dever de transparência/paridade de armas.
7. **Neurodireitos e interfaces cérebro-máquina** — prospectivo, mas fértil: nemo tenetur diante de dados neurais; "leitura" involuntária de estados mentais como autoincriminação.
8. **Jurisdição e a dark web / anonimato (Tor)** — imputação quando a autoria é tecnicamente ofuscada; presunções e o limite da prova indiciária.

---

## Como eu recomendaria transformar isto em produção

1. **Escolher 1 carro-chefe** (sugiro tópico 7 ou 12) e escrever um artigo denso e publicável — serve de "cartão de visita" acadêmico e alimenta o RAG do escritório (conecta com o outro projeto).
2. **Montar uma base bibliográfica** por eixo (doutrina + jurisprudência STF/STJ + direito comparado) — cada artigo produzido vira ativo reutilizável.
3. **Validar as âncoras legais** de cada tópico antes de publicar (texto vigente + jurisprudência atual), porque legislação penal/processual digital muda rápido.
4. Para cada tópico, o esqueleto de artigo é o mesmo: *problema → estado da arte dogmático → dado técnico decisivo → tese → objeções e réplica → conclusão de lege lata / lege ferenda*.

---

*Documento de brainstorming acadêmico. As teses são ângulos defensáveis — não pareceres. Antes de publicar/peticionar, confirme dispositivos e jurisprudência vigentes.*
