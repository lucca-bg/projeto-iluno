// Chamadas à API Python (T05 / T17).
async function get(caminho) {
  const r = await fetch(caminho);
  if (!r.ok) {
    const erro = new Error(`Erro ${r.status} em ${caminho}`);
    erro.status = r.status;
    throw erro;
  }
  return r.json();
}

export const buscarDisciplinas = (nome) =>
  get(`/api/disciplinas?nome=${encodeURIComponent(nome)}`);

export const obterDisciplina = (id) => get(`/api/disciplinas/${encodeURIComponent(id)}`);

export const listarTopicos = () => get("/api/topicos");
