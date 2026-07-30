import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-29-roadmap-infraestrutura',
  date: '2026-07-29',
  title: 'Roadmap: domínio próprio, organização e proteção do repositório',
  summary:
    'O roadmap ganhou uma seção de infraestrutura com o passo a passo do domínio próprio, as observações para a migração do repositório a uma organização e a política de proteção da branch principal.',
  body: [
    'A ordem registrada é deliberada: o domínio vem antes da migração, porque o endereço github.io do site não redireciona quando o repositório muda de dono — e as URLs dos tipos penais são citadas em pareceres e pesquisas. Com o domínio configurado, a URL canônica sobrevive à mudança, e um repositório-toco preservará os links antigos.',
    'A proteção da branch principal (ruleset) exigirá pull request com aprovação do mantenedor e verificação contínua verde, com exceções para os fluxos automáticos do repositório — as regras passam a valer de fato quando houver mais colaboradores.',
  ],
  tipo: 'melhoria',
  areas: ['Documentação'],
  version: 'v1.2.14',
  links: [
    {
      label: 'Ver o Roadmap',
      href: 'https://amorim-rc.github.io/sispenas/docs/roadmap',
    },
  ],
};

export default entrada;
