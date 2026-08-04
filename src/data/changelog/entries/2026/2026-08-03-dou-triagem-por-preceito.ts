import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-03-dou-triagem-por-preceito',
  date: '2026-08-03',
  title: 'O aviso semanal sobre leis novas trazia seis textos por semana e nada de penal',
  summary:
    'Medido contra catorze dias reais do Diário Oficial — 3.569 atos publicados —, o filtro devolvia seis leis para ler e nenhuma criava ou alterava crime. Ele passa a cortar pelo que distingue lei penal de lei que fala de pena: a cominação de uma pena.',
  body: [
    'Toda semana o sistema lê a Seção 1 do Diário Oficial em busca de lei penal nova — aquela que cria crime em diploma que a conferência ainda não acompanha. É o único ponto cego declarado da conferência semanal, e o filtro existia para cobri-lo.',
    'Só que ele casava quem citasse um diploma acompanhado OU tivesse vocabulário penal, e as duas condições são largas demais. Medido contra catorze dias reais, ele devolveu seis candidatas: uma medida provisória sobre fundo garantidor, pela palavra revoga; uma lei sobre recursos do fundo penitenciário, pela palavra crime; uma sobre divulgação de telefone de denúncias, por passa a vigorar acrescida; uma sobre honorários de advogado, por citar o Estatuto da OAB. Nenhuma das seis cominava pena alguma.',
    'Ler seis textos por semana para não achar nada é o jeito mais rápido de parar de ler, e um filtro que ninguém lê é um filtro que não existe.',
    'O corte passa a ser o preceito secundário — a fórmula Pena, reclusão de, detenção de. Um ato que fale de pena sem cominar nenhuma não cria nem altera crime. Contra os mesmos catorze dias esse critério devolve zero; contra a lei de março que criou dois tipos penais, ele acerta.',
    'Duas redes de segurança, porque deixar passar uma lei penal custa meses de catálogo desatualizado: a ementa que anuncia o crime sobe o ato de nível mesmo quando o texto integral não abre, e revogar dispositivo de diploma acompanhado também sobe, porque suprimir um tipo não deixa a palavra pena no texto do ato.',
    'E o que foi cortado não some. Cada ato descartado aparece em uma linha, com o motivo e o link — três segundos de leitura, e a decisão do filtro fica auditável. O que era ruído virou ainda um aviso pequeno e útil: os diplomas citados na janela saem numa linha de rodapé, porque se uma dessas leis os alterou, a prova de que a página baixada está atualizada precisa mudar junto.',
  ],
  tipo: 'melhoria',
  areas: ['Tipos penais'],
  version: 'v1.9.0',
};

export default entrada;
