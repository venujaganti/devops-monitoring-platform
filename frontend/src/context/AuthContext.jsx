import {
  createContext,
  useEffect,
  useState
} from "react";

import { authApi } from "../services/api";

import {
  TOKEN_KEY,
  USER_KEY
} from "../utils/constants";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const savedUser =
      localStorage.getItem(USER_KEY);

    return savedUser
      ? JSON.parse(savedUser)
      : null;
  });

  const [loading, setLoading] = useState(true);

  const isAuthenticated =
    Boolean(localStorage.getItem(TOKEN_KEY));

  useEffect(() => {
    async function loadUser() {
      const token =
        localStorage.getItem(TOKEN_KEY);

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const currentUser =
          await authApi.me();

        setUser(currentUser);

        localStorage.setItem(
          USER_KEY,
          JSON.stringify(currentUser)
        );
      } catch {
        logout();
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, []);

  async function login(username, password) {
    const data =
      await authApi.login(
        username,
        password
      );

    localStorage.setItem(
      TOKEN_KEY,
      data.access_token
    );

    const currentUser =
      await authApi.me();

    setUser(currentUser);

    localStorage.setItem(
      USER_KEY,
      JSON.stringify(currentUser)
    );

    return currentUser;
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);

    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}