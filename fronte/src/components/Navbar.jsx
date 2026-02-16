import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import logo from "../assets/logo.png";

export default function Navbar() {
  return (
    <nav className="flex justify-between items-center px-10 py-5 
                    bg-black/40 backdrop-blur-xl 
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
            className="w-10 h-10 object-contain transition-all duration-300
                       group-hover:drop-shadow-[0_0_15px_rgba(34,211,238,0.7)]"
            whileHover={{ rotate: 5 }}
          />

          <h1 className="text-xl font-bold 
                         bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 
                         bg-clip-text text-transparent">
            Olympiad Mastery AI
          </h1>
        </motion.div>
      </Link>

      {/* Navigation Links */}
      <div className="flex gap-8 text-gray-300 text-sm font-medium">
        <NavItem to="/" label="Home" />
        <NavItem to="/chat" label="Chat" />
        <NavItem to="/planner" label="Planner" />
        <NavItem to="/mock" label="Mock" />
      </div>
    </nav>
  );
}

function NavItem({ to, label }) {
  return (
    <Link
      to={to}
      className="relative group transition duration-300"
    >
      <span className="group-hover:text-cyan-400 transition">
        {label}
      </span>

      <span className="absolute left-0 -bottom-1 h-[2px] w-0 
                       bg-gradient-to-r from-cyan-400 to-purple-400 
                       transition-all duration-300 
                       group-hover:w-full">
      </span>
    </Link>
  );
}
