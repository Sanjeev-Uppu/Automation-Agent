import { Link, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import logo from "../assets/logo.png";

export default function Navbar() {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav
      className="sticky top-0 z-50 
      bg-black/50 backdrop-blur-2xl 
      border-b border-white/10"
    >
      <div className="w-full flex justify-between items-center px-6 sm:px-10 py-4">

        {/* Logo */}
        <Link to="/">
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center gap-2 cursor-pointer group"
          >
            <motion.img
              src={logo}
              alt="Olympiad Mastery Logo"
              className="w-9 h-9 sm:w-10 sm:h-10 object-contain
              transition-all duration-300
              group-hover:drop-shadow-[0_0_12px_rgba(34,211,238,0.8)]"
              whileHover={{ rotate: 5 }}
            />

            <h1 className="hidden sm:block text-lg sm:text-xl font-extrabold text-white tracking-wide">
              Master Olympiad
            </h1>
          </motion.div>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex gap-8 text-sm sm:text-base font-medium">
          <NavItem to="/" label="Home" current={location.pathname} />
          <NavItem to="/chat" label="Chat" current={location.pathname} />
          <NavItem to="/planner" label="Planner" current={location.pathname} />
          <NavItem to="/mock" label="Mock" current={location.pathname} />
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden text-white text-2xl"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          ☰
        </button>

      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {menuOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="md:hidden bg-black/90 backdrop-blur-xl border-t border-white/10"
          >
            <div className="flex flex-col items-center gap-6 py-6 text-lg">

              <MobileItem to="/" label="Home" setMenuOpen={setMenuOpen} />
              <MobileItem to="/chat" label="Chat" setMenuOpen={setMenuOpen} />
              <MobileItem to="/planner" label="Planner" setMenuOpen={setMenuOpen} />
              <MobileItem to="/mock" label="Mock" setMenuOpen={setMenuOpen} />

            </div>
          </motion.div>
        )}
      </AnimatePresence>

    </nav>
  );
}

function NavItem({ to, label, current }) {
  const isActive = current === to;

  return (
    <Link to={to} className="relative group transition duration-300">

      <span
        className={`transition duration-300 
        ${isActive ? "text-cyan-400" : "text-gray-300 group-hover:text-white"}`}
      >
        {label}
      </span>

      <motion.span
        layoutId="underline"
        className={`absolute left-0 -bottom-1 h-[2px] 
        bg-gradient-to-r from-cyan-400 to-purple-400
        ${isActive ? "w-full" : "w-0 group-hover:w-full"}
        transition-all duration-300`}
      />

    </Link>
  );
}

function MobileItem({ to, label, setMenuOpen }) {
  return (
    <Link
      to={to}
      onClick={() => setMenuOpen(false)}
      className="text-gray-300 hover:text-cyan-400 transition"
    >
      {label}
    </Link>
  );
}