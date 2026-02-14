import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import ChatPage from "./pages/ChatPage";
import MockPage from "./pages/MockPage";
import PlannerPage from "./pages/PlannerPage";
 

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/mock" element={<MockPage />} />
          <Route path="/planner" element={<PlannerPage />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}

export default App;
