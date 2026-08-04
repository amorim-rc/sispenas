import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-04-o-que-a-conferencia-nao-garante',
  date: '2026-08-04',
  title: 'O que a conferência não garante agora tem nome, endereço e limite',
  summary:
    'A ferramenta publicava quantos registros ficavam sem conferência, mas não quais nem por quê — e um dos três motivos chamava-se "indeterminado". Cada registro não conferido passa a sair identificado, classificado por motivo, e o total de cada motivo passa a ser um limite que não pode crescer sem que alguém decida.',
  body: [
    'A falha que mais dói neste projeto não é ler a lei errado: é não ler e não dizer nada. Um registro que a conferência não alcança não aparece como divergente — aparece como nada, e um número agregado no rodapé do relatório não dá a ninguém como agir sobre ele. Foi debaixo de um número desses que três incisos do art. 151 do Código Penal publicaram por anos seis vezes a pena que a lei comina.',
    'Os motivos agora são cinco, e a diferença entre eles é o que se pode fazer a seguir. Registro sem pena privativa: não há moldura a comparar. Pena importada de outro dispositivo: é copiável, basta resolver a remissão. Pena derivada por cálculo, como aumento ou diminuição: é derivável, e o motor de dosimetria do projeto já sabe fazer a conta. Dispositivo que não é preceito, como norma explicativa ou extensiva: não há pena ali para ler. E o quinto, que é o alarme: a lei escreveu a pena e a ferramenta não conseguiu ler.',
    'Os quatro primeiros são limites declarados. O quinto tende a zero, e hoje tem dois casos, ambos nomeados. Um deles é um erro de digitação no próprio texto oficial de um decreto-lei de 1944, e não há o que fazer com ele além de dizer que existe.',
    'Sobre esses números foi posta uma trava. O tamanho aceito de cada grupo fica escrito num arquivo, como já acontece com as exceções de auditoria. Se um grupo cresce, a rodada acusa regressão e sai com erro mesmo que nenhuma divergência tenha sido encontrada — porque um registro que sai da conferência é justamente aquilo que ninguém veria de outro modo. Se encolhe, a rodada avisa que dá para apertar o limite. E o arquivo não se atualiza sozinho: se ele se regravasse quando a cobertura piora, a trava não travaria nada.',
  ],
  tipo: 'melhoria',
  areas: ['Documentação'],
  version: 'v1.9.3',
};

export default entrada;
