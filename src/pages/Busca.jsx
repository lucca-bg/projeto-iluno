// F02 — tela de busca de disciplinas pelo nome (consome o endpoint do T05).
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { buscarDisciplinas } from "../services/api";

export default function Busca() {
  const [termo, setTermo] = useState("");
  const [resultado, setResultado] = useState(null);
  const [erro, setErro] = useState("");

  useEffect(() => {
    const t = setTimeout(() => {
      setErro("");
      buscarDisciplinas(termo)
        .then(setResultado)
        .catch(() => setErro("Não foi possível buscar as disciplinas."));
    }, 250);
    return () => clearTimeout(t);
  }, [termo]);

  return (
    <section>
      <div className="hero">
        <h1>Saiba o que esperar antes de escolher a cadeira</h1>
        <p className="sub">Avaliações de quem já cursou: dificuldade, carga extraclasse e mais.</p>
        <input
          className="busca"
          type="search"
          placeholder="Buscar disciplina pelo nome…"
          value={termo}
          onChange={(e) => setTermo(e.target.value)}
          aria-label="Buscar disciplina pelo nome"
          autoFocus
        />
      </div>

      {erro && <p className="erro bloco">{erro}</p>}
      {resultado && resultado.total === 0 && (
        <p className="aviso">Nenhuma disciplina encontrada para “{termo}”.</p>
      )}

      <ul className="lista">
        {resultado?.disciplinas.map((d) => (
          <li key={d.id}>
            <Link to={`/disciplina/${d.id}`} className="item">
              <strong>{d.nome}</strong>
              <span>
                {d.curso} · {d.modalidade} · {d.cargaHoraria}h
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
