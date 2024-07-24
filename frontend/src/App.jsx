import react from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";
import Operations from "./pages/Operations";
import ProtectedRoute from "./components/ProtectedRoute";
import Pockets from "./components/Pockets";
import PocketDetail from "./pages/PocketDetail";
import PocketCharts from "./pages/PocketCharts";
import PocketHistory from "./pages/PocketHistory";

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/operations"
          element={
            <ProtectedRoute>
              <Operations />
            </ProtectedRoute>
          }
        />
        <Route
          path="/pockets"
          element={
            <ProtectedRoute>
              <Pockets />
            </ProtectedRoute>
          }
        />
        <Route
          path="/pockets/:slug"
          element={
            <ProtectedRoute>
              <PocketDetail />
            </ProtectedRoute>
          }
        />
        <Route
          path="/pockets/:slug/charts"
          element={
            <ProtectedRoute>
              <PocketCharts />
            </ProtectedRoute>
          }
        />
        <Route
          path="/pockets/:slug/history"
          element={
            <ProtectedRoute>
              <PocketHistory />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
