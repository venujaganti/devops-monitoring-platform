import {
  useState
} from "react";

import {
  Navigate,
  useLocation,
  useNavigate
} from "react-router-dom";

import {
  Activity,
  Lock,
  User
} from "lucide-react";

import { useAuth } from "../hooks/useAuth";

import {
  validateLogin
} from "../utils/validators";

import ErrorMessage from "../components/ErrorMessage";

export default function Login() {
  const {
    login,
    isAuthenticated
  } = useAuth();

  const navigate = useNavigate();

  const location = useLocation();

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [errors, setErrors] =
    useState({});

  const [loading, setLoading] =
    useState(false);

  if (isAuthenticated) {
    return (
      <Navigate to="/" replace />
    );
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const validationErrors =
      validateLogin(
        username,
        password
      );

    setErrors(validationErrors);

    if (
      Object.keys(validationErrors)
        .length > 0
    ) {
      return;
    }

    try {
      setLoading(true);

      await login(
        username,
        password
      );

      const destination =
        location.state?.from?.pathname ||
        "/";

      navigate(destination, {
        replace: true
      });
    } catch (error) {
      setErrors({
        general:
          error.response?.data?.detail ||
          "Invalid username or password"
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-brand">
          <Activity size={42} />

          <h1>DevOps Monitoring</h1>

          <p>
            Monitoring & Incident Management
          </p>
        </div>

        <form
          className="login-form"
          onSubmit={handleSubmit}
        >
          <h2>Sign in</h2>

          <p>
            Sign in to access the monitoring
            dashboard.
          </p>

          {errors.general && (
            <ErrorMessage
              message={errors.general}
            />
          )}

          <label>
            Username

            <div className="input-wrapper">
              <User size={18} />

              <input
                type="text"
                value={username}
                onChange={(event) =>
                  setUsername(
                    event.target.value
                  )
                }
                placeholder="Enter username"
                autoComplete="username"
              />
            </div>
          </label>

          {errors.username && (
            <small className="field-error">
              {errors.username}
            </small>
          )}

          <label>
            Password

            <div className="input-wrapper">
              <Lock size={18} />

              <input
                type="password"
                value={password}
                onChange={(event) =>
                  setPassword(
                    event.target.value
                  )
                }
                placeholder="Enter password"
                autoComplete="current-password"
              />
            </div>
          </label>

          {errors.password && (
            <small className="field-error">
              {errors.password}
            </small>
          )}

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading
              ? "Signing in..."
              : "Sign In"}
          </button>
        </form>

        <div className="login-footer">
          Development credentials:
          <br />
          <strong>admin / Admin@123</strong>
        </div>
      </div>
    </div>
  );
}