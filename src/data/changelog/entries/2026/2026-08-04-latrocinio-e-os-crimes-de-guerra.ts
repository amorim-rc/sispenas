import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-04-latrocinio-e-os-crimes-de-guerra',
  date: '2026-08-04',
  title: 'O latrocínio e trinta e três crimes militares passaram a ser conferidos contra a lei',
  summary:
    'Três lacunas de leitura tiravam da conferência dispositivos cuja pena está escrita no texto oficial em formato que a ferramenta não reconhecia. Uma delas era pior que silêncio: fazia a conferência ler a pena de um crime e atribuí-la a outro.',
  body: [
    'A primeira lacuna era um conectivo. Quando a lei escreve o número por extenso entre parênteses e o número é composto — "de 24 (vinte e quatro) a 30 (trinta) anos" —, a limpeza do texto removia os dois numerais e deixava o "e" para trás. O que sobrava não era mais um intervalo, e a moldura desaparecia. Vítima concreta: o latrocínio, no art. 157, parágrafo 3º, inciso II do Código Penal, nunca havia sido confrontado com a lei.',
    'A segunda era a fórmula de graus com que o Código Penal Militar comina os crimes de tempo de guerra: "morte, grau máximo; reclusão, de vinte anos, grau mínimo". Não é um intervalo, e trinta e três registros do Livro II ficavam de fora. Agora se confere o piso, que a lei escreve. O teto continua sem conferência, e por um motivo declarado: a lei diz "morte", e o número que o catálogo publica no lugar dela é uma escolha do projeto, não uma leitura da lei.',
    'A terceira era estrutural e a mais grave. Quando o dispositivo é só um cabeçalho — "Se da violência resulta:" — e cada inciso traz a sua própria pena, todas as penas eram atribuídas ao mesmo dispositivo e a última vencia. Sobrava a pena do último inciso e a do primeiro sumia. Isso não é silêncio, é leitura errada: quem corrigisse o catálogo por ela trocaria a pena da lesão corporal grave pela do latrocínio. Dois artigos do Código Penal Militar chegaram a ser acusados de divergência sendo ambos corretos.',
    'A distribuição das penas pelos incisos é deliberadamente conservadora, porque o caso comum é o oposto: onde a lei enumera modalidades da conduta e comina uma pena só ao final, ela é do artigo. E a redação nova de uma pena não conta como pena de inciso — sem essa ressalva, o crime de lavagem de dinheiro se partiria em dois, já que o texto oficial imprime a pena antiga depois de um inciso e a nova depois de outro.',
    'Cobertura da conferência: de 82,0% para 86,3% do catálogo.',
  ],
  tipo: 'melhoria',
  areas: ['Tipos penais', 'Documentação'],
  version: 'v1.9.3',
};

export default entrada;
