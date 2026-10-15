// T02 — formulário de cadastro com validação.
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { cadastrarUsuario, mensagemDeErro } from "../services/usuarios";

const VAZIO = { nome: "", email: "", senha: "", confirmacao: "", curso: "", semestre: "" };

export function validarCadastro(f) {
  const erros = {};
  if (f.nome.trim().length < 2) erros.nome = "Informe seu nome.";
  else if (f.nome.trim().length > 80) erros.nome = "Use no máximo 80 caracteres.";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) erros.email = "Informe um e-mail válido.";
  if (f.senha.length < 6) erros.senha = "A senha precisa ter pelo menos 6 caracteres.";
  if (f.confirmacao !== f.senha) erros.confirmacao = "As senhas não coincidem.";
  if (f.curso.trim().length < 2) erros.curso = "Informe seu curso.";
  const s = Number(f.semestre);
  if (!Number.isInteger(s) || s < 1 || s > 12) erros.semestre = "Escolha o semestre.";
  return erros;
}

export default function Cadastro() {
  const [form, setForm] = useState(VAZIO);
  const [erros, setErros] = useState({});
  const [erroGeral, setErroGeral] = useState("");
  const [enviando, setEnviando] = useState(false);
  const navigate = useNavigate();

  const alterar = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  async function enviar(e) {
    e.preventDefault();
    const encontrados = validarCadastro(form);
    setErros(encontrados);
    setErroGeral("");
    if (Object.keys(encontrados).length) return;

    setEnviando(true);
    try {
      await cadastrarUsuario(form);
      navigate("/perfil");
    } catch (err) {
      setErroGeral(mensagemDeErro(err));
    } finally {
      setEnviando(false);
    }
  }

  const campo = (nome, rotulo, props = {}) => (
    <label className="campo">
      <span>{rotulo}</span>
      <input name={nome} value={form[nome]} onChange={alterar} aria-invalid={!!erros[nome]} {...props} />
      {erros[nome] && <small className="erro">{erros[nome]}</small>}
    </label>
  );

  return (
    <section className="cartao estreito">
      <h1>Criar conta</h1>
      <p className="sub">Para avaliar disciplinas e ver seu perfil.</p>

      <form onSubmit={enviar} noValidate>
        {campo("nome", "Nome", { autoComplete: "name" })}
        {campo("email", "E-mail", { type: "email", autoComplete: "email" })}
        {campo("senha", "Senha", { type: "password", autoComplete: "new-password" })}
        {campo("confirmacao", "Confirme a senha", { type: "password", autoComplete: "new-password" })}
        {campo("curso", "Curso", { placeholder: "Ex.: Ciência da Computação" })}

        <label className="campo">
          <span>Semestre atual</span>
          <select name="semestre" value={form.semestre} onChange={alterar} aria-invalid={!!erros.semestre}>
            <option value="">Selecione</option>
            {Array.from({ length: 12 }, (_, i) => i + 1).map((n) => (
              <option key={n} value={n}>
                {n}º semestre
              </option>
            ))}
          </select>
          {erros.semestre && <small className="erro">{erros.semestre}</small>}
        </label>

        {erroGeral && <p className="erro bloco">{erroGeral}</p>}

        <button className="botao" disabled={enviando}>
          {enviando ? "Criando conta…" : "Criar conta"}
        </button>
      </form>

      <p className="rodape-form">
        Já tem conta? <Link to="/entrar">Entrar</Link>
      </p>
    </section>
  );
}
