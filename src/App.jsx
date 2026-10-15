import { Link, Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./AuthContext";
import Busca from "./pages/Busca";
import Cadastro from "./pages/Cadastro";
import Disciplina from "./pages/Disciplina";
import Login from "./pages/Login";
import Perfil from "./pages/Perfil";

function RotaPrivada({ children }) {
  const { usuario, carregando } = useAuth();
  if (carregando) return <p className="aviso">Carregando…</p>;
  return usuario ? children : <Navigate to="/entrar" replace />;
}

export default function App() {
  const { usuario } = useAuth();

  return (
    <>
      <header className="topo">
        <Link to="/" className="marca">
          iLuno
        </Link>
        <nav>
          {usuario ? (
            <Link to="/perfil">Meu perfil</Link>
          ) : (
            <>
              <Link to="/entrar">Entrar</Link>
              <Link to="/cadastro" className="botao pequeno">
                Criar conta
              </Link>
            </>
          )}
        </nav>
      </header>

      <main className="conteudo">
        <Routes>
          <Route path="/" element={<Busca />} />
          <Route path="/disciplina/:id" element={<Disciplina />} />
          <Route path="/cadastro" element={<Cadastro />} />
          <Route path="/entrar" element={<Login />} />
          <Route
            path="/perfil"
            element={
              <RotaPrivada>
                <Perfil />
              </RotaPrivada>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </>
  );
}
