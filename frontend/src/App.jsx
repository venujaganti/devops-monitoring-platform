import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";

import ProtectedRoute from "./components/ProtectedRoute";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Servers from "./pages/Servers";
import ServerDetails from "./pages/ServerDetails";
import Applications from "./pages/Applications";
import Alerts from "./pages/Alerts";
import Incidents from "./pages/Incidents";
import Logs from "./pages/Logs";
import Users from "./pages/Users";
import Settings from "./pages/Settings";

function Layout() {
  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Header />

        <div className="content">
          <Routes>
            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/servers"
              element={<Servers />}
            />

            <Route
              path="/servers/:id"
              element={<ServerDetails />}
            />

            <Route
              path="/applications"
              element={<Applications />}
            />

            <Route
              path="/alerts"
              element={<Alerts />}
            />

            <Route
              path="/incidents"
              element={<Incidents />}
            />

            <Route
              path="/logs"
              element={<Logs />}
            />

            <Route
              path="/users"
              element={<Users />}
            />

            <Route
              path="/settings"
              element={<Settings />}
            />
          </Routes>
        </div>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route
            path="/login"
            element={<Login />}
          />

          <Route element={<ProtectedRoute />}>
            <Route
              path="/*"
              element={<Layout />}
            />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}