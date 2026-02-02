import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./contexts/AuthContext";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Recommendations from "./pages/Recommendations";
import TeamFavorites from "./pages/TeamFavorites";
import Favorites from "./pages/Favorites";
import VaultSearch from "./pages/VaultSearch";
import Profile from "./pages/Profile";
import ResourceDetails from "./pages/ResourceDetails";

const LOGIN_PATH = "/login";

function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isReady } = useAuth();
  const location = useLocation();

  if (!isReady) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-slate-400">
        Loading…
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to={LOGIN_PATH} state={{ from: location }} replace />;
  }

  return <>{children}</>;
}

export default function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      <Routes>
        <Route path={LOGIN_PATH} element={<Login />} />
        <Route
          path="/*"
          element={
            <ProtectedLayout>
              <Layout />
            </ProtectedLayout>
          }
        >
          <Route index element={<Home />} />
          <Route path="recommendations" element={<Recommendations />} />
          <Route path="favorites" element={<Favorites />} />
          <Route path="team-favorites" element={<TeamFavorites />} />
          <Route path="vault-search" element={<VaultSearch />} />
          <Route path="profile" element={<Profile />} />
          <Route path="resources/:id" element={<ResourceDetails />} />
        </Route>
      </Routes>
    </div>
  );
}
