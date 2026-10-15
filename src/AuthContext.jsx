import { createContext, useContext, useEffect, useState } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "./firebase";

const AuthContext = createContext({ usuario: null, carregando: true });

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(
    () =>
      onAuthStateChanged(auth, (u) => {
        setUsuario(u);
        setCarregando(false);
      }),
    []
  );

  return (
    <AuthContext.Provider value={{ usuario, carregando }}>{children}</AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
