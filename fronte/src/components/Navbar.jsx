import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import logo from "../assets/logo.png";

export default function Navbar() {
  const location = useLocation();

  return (
    <nav className="flex justify-between items-center 
    px-6 sm:px-10 py-4
    bg-black/50 backdrop-blur-2xl 
    border-b border-white/10 
    sticky top-0 z-50">

      {/* Logo Section */}
      <Link to="/">
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <motion.img
            src={logo}
            alt="Olympiad Mastery Logo"
            className="w-9 h-9 sm:w-10 sm:h-10 object-contain
            transition-all duration-300
            group-hover:drop-shadow-[0_0_12px_rgba(34,211,238,0.8)]"
            whileHover={{ rotate: 5 }}
          />

          <h1 className="text-lg sm:text-xl font-extrabold text-white tracking-wide">
            Master Olympiad
          </h1>
        </motion.div>
      </Link>

      {/* Navigation Links */}
      <div className="flex gap-6 sm:gap-8 text-sm sm:text-base font-medium">
        <NavItem to="/" label="Home" current={location.pathname} />
        <NavItem to="/chat" label="Chat" current={location.pathname} />
        <NavItem to="/planner" label="Planner" current={location.pathname} />
        <NavItem to="/mock" label="Mock" current={location.pathname} />
      </div>
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

      {/* Animated Underline */}
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
