// T01 — modelo de usuário no Firestore.
//
// usuarios/{uid}
//   nome:      string   (2 a 80 caracteres)
//   email:     string   (o mesmo do Firebase Authentication)
//   curso:     string
//   semestre:  number   (1 a 12)
//   criadoEm:  timestamp do servidor
//
// As restrições acima também são validadas em firestore.rules (T08).
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from "firebase/auth";
import { doc, getDoc, serverTimestamp, setDoc } from "firebase/firestore";
import { auth, db } from "../firebase";

export async function cadastrarUsuario({ nome, email, senha, curso, semestre }) {
  const cred = await createUserWithEmailAndPassword(auth, email, senha);
  await setDoc(doc(db, "usuarios", cred.user.uid), {
    nome: nome.trim(),
    email: cred.user.email,
    curso: curso.trim(),
    semestre: Number(semestre),
    criadoEm: serverTimestamp(),
  });
  return cred.user;
}

export const entrar = (email, senha) => signInWithEmailAndPassword(auth, email, senha);

export const sair = () => signOut(auth);

export async function obterPerfil(uid) {
  const snap = await getDoc(doc(db, "usuarios", uid));
  return snap.exists() ? snap.data() : null;
}

// Traduz os códigos de erro do Firebase Authentication para mensagens em português.
export function mensagemDeErro(erro) {
  const mapa = {
    "auth/email-already-in-use": "Este e-mail já está cadastrado.",
    "auth/invalid-email": "E-mail inválido.",
    "auth/weak-password": "A senha precisa ter pelo menos 6 caracteres.",
    "auth/invalid-credential": "E-mail ou senha incorretos.",
    "auth/too-many-requests": "Muitas tentativas. Tente novamente em alguns minutos.",
  };
  return mapa[erro?.code] || "Não foi possível concluir. Tente novamente.";
}
