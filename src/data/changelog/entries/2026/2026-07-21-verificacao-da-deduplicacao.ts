import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  "id": "2026-07-21-verificacao-da-deduplicacao",
  "date": "2026-07-21",
  "title": "Verificação rigorosa da deduplicação e limpeza de encoding",
  "summary": "Revisão de segurança sobre a deduplicação da versão anterior, provocada por uma pergunta direta: havia mesmo só duplicatas? A reconferência achou descrições trocadas e mais duplicatas escondidas, todas corrigidas.",
  "body": [
    "A lição ficou registrada: deduplicar por (lei, artigo) exato não basta — é preciso conferir sem o caput, sem o “(atualiz.)” e com os sufixos de artigo, e rodar similaridade de nome antes de remover."
  ],
  "tipo": "correcao",
  "areas": [
    "Tipos penais"
  ],
  "version": "v1.1.7"
};

export default entrada;
