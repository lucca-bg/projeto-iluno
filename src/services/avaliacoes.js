// F03 — avaliação da disciplina em tópicos definidos (T06).
//
// disciplinas/{disciplinaId}/avaliacoes/{uid}
//   notas:    { dificuldade, carga_extraclasse, aplicacao_pratica, relevancia }  (inteiros 1 a 5)
//   criadoEm: timestamp do servidor
//
// O ID do documento é o uid do aluno: uma avaliação por aluno por disciplina.
import { doc, getDoc, serverTimestamp, setDoc } from "firebase/firestore";
import { db } from "../firebase";

const ref = (disciplinaId, uid) => doc(db, "disciplinas", disciplinaId, "avaliacoes", uid);

export async function obterMinhaAvaliacao(disciplinaId, uid) {
  const snap = await getDoc(ref(disciplinaId, uid));
  return snap.exists() ? snap.data() : null;
}

export function enviarAvaliacao(disciplinaId, uid, notas) {
  return setDoc(ref(disciplinaId, uid), { notas, criadoEm: serverTimestamp() });
}
