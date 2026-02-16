import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";
import MockPage from "./pages/MockPage";
import PlannerPage from "./pages/PlannerPage";

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/planner" element={<PlannerPage />} />
          <Route path="/mock" element={<MockPage />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}

export default App;
