// T03 — tela de perfil do usuário.
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import { obterPerfil, sair } from "../services/usuarios";

export default function Perfil() {
  const { usuario } = useAuth();
  const [perfil, setPerfil] = useState(null);
  const [erro, setErro] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    obterPerfil(usuario.uid)
      .then((p) => (p ? setPerfil(p) : setErro("Perfil não encontrado.")))
      .catch(() => setErro("Não foi possível carregar o perfil."));
  }, [usuario.uid]);

  async function encerrar() {
    await sair();
    navigate("/");
  }

  if (erro) return <p className="erro bloco">{erro}</p>;
  if (!perfil) return <p className="aviso">Carregando perfil…</p>;

  const desde = perfil.criadoEm?.toDate?.().toLocaleDateString("pt-BR");

  return (
    <section className="cartao estreito">
      <div className="avatar" aria-hidden="true">
        {perfil.nome.charAt(0).toUpperCase()}
      </div>
      <h1>{perfil.nome}</h1>
      <p className="sub">{perfil.email}</p>

      <dl className="dados">
        <div>
          <dt>Curso</dt>
          <dd>{perfil.curso}</dd>
        </div>
        <div>
          <dt>Semestre</dt>
          <dd>{perfil.semestre}º</dd>
        </div>
        {desde && (
          <div>
            <dt>Membro desde</dt>
            <dd>{desde}</dd>
          </div>
        )}
      </dl>

      <button className="botao secundario" onClick={encerrar}>
        Sair
      </button>
    </section>
  );
}
