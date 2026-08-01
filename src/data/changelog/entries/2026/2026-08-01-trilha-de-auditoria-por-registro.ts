import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-01-trilha-de-auditoria-por-registro',
  date: '2026-08-01',
  title: 'Cada tipo penal passa a dizer quando foi conferido contra a lei',
  summary:
    'Não basta saber que existe conferência semanal: quem cita um dado precisa saber deste dado. Cada registro do catálogo ganha três campos de auditoria — contra qual página oficial ele é conferido, em que data isso aconteceu pela última vez e com que resultado.',
  body: [
    'Os campos são preenchidos pela própria rodada semanal, que agora carimba o que conferiu. O resultado diz uma de quatro coisas: a moldura publicada bate com a que a lei comina; o dispositivo não traz moldura própria, porque a pena vem por referência a outro artigo ou porque a sanção não é de prisão; a moldura diverge, e virou achado da semana; ou o caso já foi julgado e consta da lista de exceções, com motivo e data.',
    'A trilha fica em um arquivo próprio, separado do catálogo editado à mão, e é publicada junto com os dados abertos. Um registro recém-criado, que nenhuma rodada alcançou ainda, tem os três campos vazios — o que também é informação: significa que aquele dado ainda não passou pela conferência.',
    'A documentação foi revisada por inteiro na mesma passagem. Havia contagens antigas (o catálogo aparecia com mil e sessenta e um tipos), a descrição de um fluxo de manutenção que não existe mais — atualização por inteligência artificial e raspagem do Diário Oficial —, o caminho errado para escrever uma nota de versão e, o mais grave, uma convenção invertida: a de que a pena publicada seria lida do campo de observações. Desde a versão 1.2.17 é o contrário, e escrever seguindo a instrução antiga produziria erro de dado.',
  ],
  tipo: 'novidade',
  areas: ['Tipos penais', 'Documentação'],
  version: 'v1.5.0',
  links: [
    {
      label: 'Como os dados são coletados e revisados',
      href: 'https://amorim-rc.github.io/sispenas/docs/dados-abertos',
    },
  ],
};

export default entrada;
