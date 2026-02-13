import Navbar from "../components/Navbar";

export default function MainLayout({ children }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-black to-purple-950 text-white">
      <Navbar />
      <div className="p-10 max-w-7xl mx-auto">
        {children}
      </div>
    </div>
  );
}
