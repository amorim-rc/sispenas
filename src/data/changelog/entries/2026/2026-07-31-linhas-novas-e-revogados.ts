import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-31-linhas-novas-e-revogados',
  date: '2026-07-31',
  title: 'Noventa e cinco tipos penais que faltavam, e quatro revogados que sobravam',
  summary:
    'A conferência automática encontrou dispositivos com pena própria que o catálogo não registrava, preceitos que punem duas condutas com penas diferentes e crimes revogados que ainda constavam como vigentes. O catálogo passa de 1.358 a 1.449 tipos.',
  body: [
    'Entram 95 registros. A maior parte são parágrafos com pena própria que só apareciam mencionados na observação do caput — formas culposas, qualificadas pelo resultado e equiparadas. Entram também as segundas molduras: quando um mesmo preceito comina penas diferentes para situações diferentes, como a inundação dolosa e a culposa do art. 254 do Código Penal, ou a falsidade ideológica em documento público e em particular, cada uma passa a ter registro próprio, com sua pena e seu endereço.',
    'Saem quatro crimes revogados que o catálogo publicava como vigentes: a violação de domicílio contra funcionário público e o exercício arbitrário de poder, ambos revogados pela Lei de Abuso de Autoridade; a usurpação de nome alheio, revogada em 2003; e a tortura de criança do Estatuto, revogada pela Lei de Tortura em 1997. Ficam registrados na página de Acervo histórico, com o dispositivo que os revogou.',
    'Corrigiu-se ainda a admissão de tentativa em 23 crimes culposos. Crime culposo não admite tentativa — não há como tentar um resultado que não se quis —, e o registro dizia o contrário. É um erro que nenhuma conferência contra o texto da lei encontraria, porque não está escrito na lei: está na doutrina.',
    'A página de Dados abertos passou a explicar para que serve cada campo do JSON — quais definem o que o sistema responde e quais apenas descrevem —, e teve corrigidas as referências a campos que não existem mais.',
  ],
  tipo: 'novidade',
  areas: ['Tipos penais', 'Documentação'],
  version: 'v1.3.0',
  links: [
    {
      label: 'Ver a inundação culposa (art. 254)',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=1335',
    },
    {
      label: 'Ver o acervo histórico',
      href: 'https://amorim-rc.github.io/sispenas/docs/acervo-historico',
    },
  ],
};

export default entrada;
