import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-06-pena-por-remissao',
  date: '2026-08-06',
  title: 'O crime que não comina pena própria passa a dizer de onde a pena vem',
  summary:
    'O art. 304 do Código Penal pune o uso de documento falso com "a pena cominada à falsificação". A moldura depende de qual falsificação foi usada — e o catálogo não tinha como dizer isso. Publicava a de um dos artigos remetidos, como se fosse certa. Agora há um campo para o estado.',
  body: [
    'Eram duas saídas ruins. Publicar a moldura de um dos dispositivos-fonte afirma como certa uma pena que depende do caso: o art. 304 remete aos arts. 297 a 302, cujas faixas vão de detenção de um mês a reclusão de seis anos. Deixar os campos em branco é indistinguível de campo não preenchido, e um registro sem pena satisfaz qualquer patamar de benefício.',
    'O campo novo, pena_por_remissao, diz o dispositivo-fonte e, quando há, o operador e a fração. Quatro registros o declaram: o art. 304 do Código Penal, o art. 315 do Código Penal Militar e os arts. 2º e 3º da Lei 2.889/56, cujas penas são metade das do art. 1º. Os dois últimos ganharam, junto, os dez registros que trazem cada uma dessas metades já calculada, um por alínea do art. 1º.',
    'Na tela, esses registros deixam de mostrar uma faixa e passam a dizer de onde a pena vem. Eles ficam fora das estatísticas de alcance dos benefícios, que se medem por patamar de pena — estar lá dentro com pena zero era o defeito.',
    'O conferidor semanal já contava 138 registros com pena definida por referência. Os quatro que a revisão leu são os que tinham moldura publicada sem sustentação no próprio artigo; os demais continuam com a moldura que a lei lhes dá diretamente.',
  ],
  tipo: 'estrutural',
  areas: ['Tipos penais', 'Benefícios', 'Interface'],
  version: 'v2.0.0',
  links: [
    {
      label: 'Ver o uso de documento falso',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=237',
    },
  ],
};

export default entrada;
