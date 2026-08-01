import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-31-auditoria-e-renumeracao',
  date: '2026-07-31',
  title: 'Auditoria completa do catálogo: nenhuma divergência com a lei, e a numeração recomeça do 1',
  summary:
    'O catálogo inteiro foi confrontado, registro a registro, com o texto compilado do Planalto. Os doze pontos que restavam foram resolvidos, e o resultado passa a ser publicado como número: de 1.412 tipos penais, 1.158 estão conferidos contra a lei e nenhum diverge dela.',
  body: [
    'A conferência agora mede a própria cobertura, e não só o que encontra. Dos 1.412 registros, 1.158 foram confrontados com a moldura que a lei comina e batem com ela. Os 252 restantes não são incógnitas: 138 têm pena definida por referência a outro dispositivo (equiparações, causas de aumento e de diminuição), 27 não têm pena de prisão — multa e outras sanções — e 87 estão em artigos cuja pena aparece em outro lugar do mesmo artigo. Nenhum registro ficou sem correspondência no texto oficial. Publicar esse número junto do relatório é a diferença entre "não encontramos erro" e "conferimos isto, e não conferimos aquilo".',
    'Doze pontos pendentes foram resolvidos. Sete registros saíram: quatro eram duplicatas de crimes que já constavam com o artigo certo, dois apontavam para dispositivos que não existem na lei, e um estava revogado. Cinco foram corrigidos: a falsidade ideológica eleitoral, que constava com o nome de outro crime e com pena de 15 dias a 6 meses, quando a lei comina até 5 anos para documento público e até 3 para o particular; o sequestro qualificado pela internação da vítima em casa de saúde, que trazia a pena de outro parágrafo; o amotinamento militar, cujo texto pune os cabeças com reclusão e os demais com detenção, e agora tem um registro para cada; e a promoção de migração ilegal, que estava sob um artigo inexistente da Lei de Migração quando o crime está no Código Penal.',
    'O aumento de pena da organização criminosa deixou de ser um tipo penal e virou o que sempre foi: uma causa de aumento, de um sexto a dois terços, aplicada sobre a pena do art. 2º da Lei 12.850. Constava como crime autônomo, sob um parágrafo que a lei não tem.',
    'Por fim, os identificadores dos tipos penais foram renumerados de 1 a 1.412, sem buracos. A numeração vinha de acréscimos e remoções sucessivos e tinha 250 lacunas; como a ferramenta ainda é um protótipo e nenhum endereço de tipo havia sido citado fora do repositório, esta é a última oportunidade de começar limpo. Daqui em diante a regra volta a valer sem exceção: identificador não é reaproveitado, e registro retirado deixa seu número aposentado para sempre.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Documentação'],
  version: 'v1.4.0',
  links: [
    {
      label: 'Como os dados são coletados e revisados',
      href: 'https://amorim-rc.github.io/sispenas/docs/dados-abertos',
    },
  ],
};

export default entrada;
