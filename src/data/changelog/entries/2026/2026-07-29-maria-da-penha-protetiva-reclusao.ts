import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-29-maria-da-penha-protetiva-reclusao',
  date: '2026-07-29',
  title: 'Maria da Penha: descumprir medida protetiva vira reclusão de 2 a 5 anos',
  summary:
    'O crime de descumprimento de medida protetiva de urgência (art. 24-A da Lei 11.340/2006) estava com a pena antiga no catálogo. A Lei 14.994/2024 elevou a pena, e a Lei 15.383/2026 acrescentou uma causa de aumento — ambas incorporadas.',
  body: [
    'A pena passou de detenção de 3 meses a 2 anos para reclusão de 2 a 5 anos, e multa (Lei 14.994/2024). Na mesma correção, a descrição foi ajustada: o registro anterior atribuía ao artigo uma causa de aumento por arma de fogo que não existe nesse dispositivo.',
    'A Lei 15.383/2026 somou o §4º: a pena é aumentada de um terço até a metade se o descumprimento decorre de violação das áreas de exclusão monitoradas eletronicamente ou da remoção, violação ou alteração do dispositivo de monitoração sem autorização judicial. Entra como modificador da dosimetria.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Dosimetria'],
  version: 'v1.2.11',
  links: [
    {
      label: 'Ver o descumprimento de medida protetiva (art. 24-A)',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=481',
    },
  ],
};

export default entrada;
