import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";
import MockPage from "./pages/MockPage";
import PlannerPage from "./pages/PlannerPage";
import QuestionPaperSetupPage from "./pages/QuestionPaperSetupPage";
import QuestionPaperPreviewPage from "./pages/QuestionPaperPreviewPage";


function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/planner" element={<PlannerPage />} />
          <Route path="/mock" element={<MockPage />} />
          <Route path="/question-paper-setup" element={<QuestionPaperSetupPage />} />
          <Route path="/question-paper-preview" element={<QuestionPaperPreviewPage />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}

export default App;
