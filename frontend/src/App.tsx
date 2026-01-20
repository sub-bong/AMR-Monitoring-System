import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import MapCapturePage from "./pages/MapCapturePage";
import AuthPage from "./pages/AuthPage";

export default function App() {
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
            <Link to="/auth" className="text-slate-700 hover:text-slate-900">
              Auth
            </Link>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/capture" element={<MapCapturePage />} />
          <Route path="/auth" element={<AuthPage />} />
          <Route path="*" element={<div className="p-8">Not Found</div>} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
