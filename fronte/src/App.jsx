import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<ChatPage />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}

export default App;
