import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-03-nomes-que-vieram-de-outro-artigo',
  date: '2026-08-03',
  title: 'Dezoito tipos penais estavam com o nome de outro artigo, e um deles com a pena junto',
  summary:
    'O nome do crime é o que a busca mostra. Quando ele vem do artigo errado, a conferência automática de penas não percebe: ela confere a moldura contra o artigo que o registro diz ser. Dezoito registros foram corrigidos, e num deles a pena publicada não tinha nada a ver com a que a lei comina.',
  body: [
    'O caso mais grave é o art. 313 do Código Eleitoral. O registro publicava reclusão de dois a seis anos e multa. O artigo comina apenas o pagamento de 90 a 120 dias-multa, sem pena de prisão. A moldura publicada era a do art. 348, o mesmo artigo de onde o nome tinha vindo: nome e pena viajaram juntos.',
    'A diferença não é de detalhe. Um crime apenado só com multa não tem regime, não tem progressão, não tem livramento condicional, prescreve em dois anos e admite transação penal de plano. Enquanto o registro publicasse dois a seis anos de reclusão, todo cálculo de benefício derivado dele estava errado.',
    'Outros três registros publicavam uma multa que o artigo não comina: o reingresso de estrangeiro expulso, os crimes contra o sistema eletrônico de votação e os crimes contra a locação. Nos três, a multa veio junto com o nome importado de outro artigo. Na direção oposta, o art. 310 do Código Eleitoral tem multa alternativa à detenção, e o sistema a lia como cumulativa, o que importa porque com multa alternativa a pena de multa sozinha basta para punir o fato.',
    'Nove correções vieram de uma varredura nova, que a revisão sugeriu e que agora roda toda semana: ela pergunta se o nome de cada registro descreve melhor outro artigo do mesmo diploma. Achou os arts. 68 e 69 da Lei de Crimes Ambientais com os nomes trocados entre si, seis artigos seguidos da Lei de Racismo cada um com o nome do artigo seguinte, e o art. 315 do Código Eleitoral com o nome do art. 323.',
    'Essa varredura existe por causa de um ponto cego. Quando dois artigos cominam a mesma pena, trocar os nomes não produz divergência nenhuma para a conferência de molduras. Foi assim que o art. 33 da Lei de Crimes Ambientais passou com o nome do art. 34, e assim que os seis artigos da Lei de Racismo ficaram deslocados, cada um com a pena certa no artigo errado.',
    'Dois registros deixaram de ser tipos penais. O art. 40 da Lei de Drogas é causa de aumento, e publicava uma pena calculada, de cinco anos e dez meses a vinte e cinco anos, como se existisse um crime com essa moldura. E o caput do art. 2º da Lei dos Crimes contra a Ordem Tributária não descreve conduta nenhuma: diz apenas que constitui crime da mesma natureza e comina a pena, com as condutas nos incisos. Foi desdobrado nos incisos III, IV e V, que faltavam.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais'],
  version: 'v1.8.0',
  links: [
    {
      label: 'Ver o art. 313 do Código Eleitoral',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=784',
    },
  ],
};

export default entrada;
