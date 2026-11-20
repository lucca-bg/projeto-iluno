// Médias aritméticas das notas de cada tópico de avaliação da disciplina.
import { useEffect, useState } from "react";
import { obterMedias } from "../services/api";

const formatar = (n) => n.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

export default function Medias({ disciplinaId, topicos, atualizacao }) {
  const [dados, setDados] = useState(null);
  const [erro, setErro] = useState("");

  useEffect(() => {
    setErro("");
    obterMedias(disciplinaId)
      .then(setDados)
      .catch(() => setErro("Não foi possível carregar as médias."));
  }, [disciplinaId, atualizacao]);

  return (
    <section className="medias">
      <h2>Médias das avaliações</h2>
      {erro && <p className="erro bloco">{erro}</p>}
      {!erro && !dados && <p className="sub">Carregando…</p>}
      {dados && dados.total === 0 && <p className="sub">Esta disciplina ainda não foi avaliada.</p>}
      {dados && dados.total > 0 && (
        <>
          <p className="sub">
            {dados.total} {dados.total === 1 ? "avaliação" : "avaliações"}
          </p>
          <dl>
            {topicos.map((t) => {
              const media = dados.medias[t.id];
              return (
                <div key={t.id} className="media">
                  <dt>{t.titulo}</dt>
                  <dd>
                    <span className="barra" aria-hidden="true">
                      <span style={{ width: `${((media ?? 0) / 5) * 100}%` }} />
                    </span>
                    <strong>{media == null ? "—" : formatar(media)}</strong>
                    <small> / 5</small>
                  </dd>
                </div>
              );
            })}
          </dl>
        </>
      )}
    </section>
  );
}
