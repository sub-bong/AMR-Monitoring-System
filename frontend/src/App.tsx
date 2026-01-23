import { BrowserRouter, Routes, Route, Link, useLocation, Navigate } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import MapCapturePage from "./pages/MapCapturePage";
import AuthPage from "./pages/AuthPage";
import { useAuth } from "./hooks/auth/useAuth";
import DeviceAdminPage from "./pages/DeviceAdminPage";
import RemoteViewerPage from "./pages/RemoteViewerPage";

function RequireAuth({ children }: { children: React.ReactNode }) {
  const { userToken } = useAuth();
  const location = useLocation();
  if (!userToken) return <Navigate to="/auth" state={{ from: location }} replace />;
  return children;
}

export default function App() {
  const { userToken } = useAuth();

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-linear-to-br from-slate-50 via-white to-slate-100">
        <nav className="fixed right-0 left-0 mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="text-slate-900 text-sm font-semibold">AMR</div>
          <div className="flex gap-3 text-sm">
            <Link to="/" className="text-slate-700 hover:text-slate-900">
              Dashboard
            </Link>
            <Link to="/capture" className="text-slate-700 hover:text-slate-900">
              Capture
            </Link>
            <Link to="/devices" className="text-slate-700 hover:text-slate-900">
              Devices
            </Link>
            <Link to="/remote" className="text-slate-700 hover:text-slate-900">
              Remote
            </Link>
            <Link to="/auth" className="text-slate-700 hover:text-slate-900">
              Auth
            </Link>
          </div>
        </nav>

        <Routes>
          <Route path="/auth" element={userToken ? <Navigate to="/" replace /> : <AuthPage />} />
          <Route
            path="/"
            element={
              <RequireAuth>
                <DashboardPage />
              </RequireAuth>
            }
          />
          <Route
            path="/capture"
            element={
              <RequireAuth>
                <MapCapturePage />
              </RequireAuth>
            }
          />
          <Route
            path="/devices"
            element={
              <RequireAuth>
                <DeviceAdminPage />
              </RequireAuth>
            }
          />
          <Route
            path="/remote"
            element={
              <RequireAuth>
                <RemoteViewerPage />
              </RequireAuth>
            }
          />
          <Route path="*" element={<div className="p-8">Not Found</div>} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
