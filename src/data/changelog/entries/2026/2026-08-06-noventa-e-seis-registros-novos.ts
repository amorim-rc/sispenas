import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-06-noventa-e-seis-registros-novos',
  date: '2026-08-06',
  title: 'Noventa e seis condutas que tinham pena própria e não tinham registro',
  summary:
    'O catálogo tem um registro por conduta com pena própria. Faltavam noventa e seis: incisos que descrevem crime completo sob a moldura do caput, molduras derivadas que a lei manda calcular sobre mais de uma base, e os crimes militares de tempo de guerra.',
  body: [
    'Dezessete vêm de artigos que cominam a pena no caput e descrevem as condutas nos incisos. Quem procurava "negar emprego a pessoa idosa por motivo de idade" não encontrava nada, porque só o inciso I do art. 100 do Estatuto da Pessoa Idosa estava cadastrado. O critério para desdobrar não é ter incisos: é o inciso descrever conduta completa, poder ser praticado isoladamente e a prática de dois gerar concurso de crimes.',
    'Trinta e nove vêm da regra do registro por moldura-base. Quando uma causa de aumento ou de diminuição alcança o caput e também os parágrafos, ela não produz uma moldura, produz uma por base — e publicar só a do caput esconde as outras. A delação premiada da extorsão mediante sequestro alcança quatro molduras; a incitação ao genocídio, cinco; o art. 141, §2º do Código Penal triplica a pena da calúnia, da difamação e da injúria, que são três faixas diferentes.',
    'Vinte e dois são crimes militares de tempo de guerra. Os arts. 391, 404 e 405 do Código Penal Militar não repetem a descrição da conduta: mandam aplicar a pena do tipo de tempo de paz com um fator — metade a mais na deserção, o dobro no furto, no roubo e na extorsão. Cada divisão do tipo de paz gera uma moldura de guerra própria, e agora cada uma tem registro. Os tipos de paz correspondentes passaram a dizer "(tempo de paz)" no nome, para que o par fique visível na busca.',
    'Os demais fecham lacunas apontadas pela própria revisão: o roubo e a extorsão qualificados do Código Penal Militar, o latrocínio militar, a hipótese do §2º do art. 5º da Lei Antiterrorismo e o inciso VI do §2º do art. 205 do CPM — a única qualificadora do homicídio militar sem correspondente no Código Penal, que por isso não é hedionda e precisava sair do registro que cobria as outras seis.',
  ],
  tipo: 'novidade',
  areas: ['Tipos penais', 'Benefícios'],
  version: 'v2.0.0',
  links: [
    {
      label: 'Ver a negativa de emprego por motivo de idade',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=1410',
    },
  ],
};

export default entrada;
