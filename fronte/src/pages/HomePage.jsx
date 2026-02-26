import { api } from "../services/api";
import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

/* ===========================
   Custom Premium Dropdown
=========================== */
function CustomDropdown({
  label,
  value,
  setValue,
  options,
  disabled,
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () =>
      document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={ref} className="relative">
      <button
        disabled={disabled}
        onClick={() => setOpen(!open)}
        className={`w-full p-3 rounded-xl text-left font-semibold
        bg-black/80 text-white
        border border-slate-600
        transition-all duration-300
        ${disabled ? "opacity-50 cursor-not-allowed" : "hover:border-pink-500"}`}
      >
        {value || label}
      </button>

      <AnimatePresence>
        {open && !disabled && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.25 }}
            className="absolute mt-2 w-full z-50
            bg-slate-900 border border-white/10
            rounded-xl shadow-2xl
            overflow-hidden backdrop-blur-xl"
          >
            {options.length === 0 ? (
              <div className="px-4 py-3 text-gray-400">
                No options available
              </div>
            ) : (
              options.map((opt) => (
                <div
                  key={opt}
                  onClick={() => {
                    setValue(opt);
                    setOpen(false);
                  }}
                  className="px-4 py-3 text-white cursor-pointer
                  hover:bg-gradient-to-r hover:from-pink-500/30 hover:to-cyan-500/30
                  transition-all duration-200"
                >
                  {opt}
                </div>
              ))
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/* ===========================
   Main Page
=========================== */

export default function HomePage() {
  const [grade, setGrade] = useState("");
  const [subject, setSubject] = useState("");
  const [chapter, setChapter] = useState("");

  const [grades, setGrades] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [chapters, setChapters] = useState([]);

  const navigate = useNavigate();

  // ================= LOAD GRADES =================
  useEffect(() => {
    const loadGrades = async () => {
      try {
        const data = await api.get("/grades");
        setGrades(data);
      } catch (err) {
        console.error("Failed to load grades", err);
      }
    };

    loadGrades();
  }, []);

  // ================= LOAD SUBJECTS =================
  useEffect(() => {
    if (!grade) return;

    const loadSubjects = async () => {
      try {
        const cleanGrade = grade.replace("Grade ", "");
        const data = await api.get(`/subjects?grade=${cleanGrade}`);
        setSubjects(data);
      } catch (err) {
        console.error("Failed to load subjects", err);
      }
    };

    loadSubjects();
  }, [grade]);

  // ================= LOAD CHAPTERS =================
  useEffect(() => {
    if (!grade || !subject) return;

    const loadChapters = async () => {
      try {
        const cleanGrade = grade.replace("Grade ", "");
        const data = await api.get(
          `/chapters?grade=${cleanGrade}&subject=${subject}`
        );
        setChapters(data);
      } catch (err) {
        console.error("Failed to load chapters", err);
      }
    };

    loadChapters();
  }, [subject, grade]);

  const openChat = () => {
    navigate("/chat", {
      state: {
        grade: grade.replace("Grade ", ""),
        subject,
        chapter_name: chapter || null,
      },
    });
  };

  return (
    <div
      className="relative min-h-screen flex items-center justify-center 
    bg-gradient-to-br from-black via-slate-900 to-purple-950 
    px-4 sm:px-6 md:px-10 py-12 overflow-hidden"
    >
      {/* Background Orbs */}
      <motion.div
        animate={{ y: [0, 30, 0] }}
        transition={{ duration: 6, repeat: Infinity }}
        className="absolute w-[450px] h-[450px] bg-pink-500/20 
        rounded-full blur-3xl top-[-120px] left-[-120px]"
      />
      <motion.div
        animate={{ y: [0, -40, 0] }}
        transition={{ duration: 8, repeat: Infinity }}
        className="absolute w-[400px] h-[400px] bg-cyan-500/20 
        rounded-full blur-3xl bottom-[-120px] right-[-120px]"
      />

      <motion.div
        initial={{ opacity: 0, y: 80, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 w-full max-w-xl md:max-w-2xl
        bg-white/10 backdrop-blur-2xl 
        border border-white/20
        shadow-[0_20px_60px_rgba(0,0,0,0.7)]
        rounded-3xl 
        p-6 sm:p-8 md:p-12"
      >
        <h1
          className="text-3xl sm:text-4xl md:text-5xl
        font-extrabold text-white text-center tracking-wide
        drop-shadow-[0_0_15px_rgba(255,255,255,0.3)]
        mb-3"
        >
          Olympiad AI Learning Hub
        </h1>

        <div
          className="h-[3px] w-36 mx-auto mb-8
        bg-gradient-to-r from-pink-500 via-cyan-400 to-yellow-400
        rounded-full"
        />

        <div className="space-y-5">
          <CustomDropdown
            label="Select Grade"
            value={grade}
            setValue={(val) => {
              setGrade(val);
              setSubject("");
              setChapter("");
            }}
            options={grades.map((g) => `Grade ${g}`)}
          />

          <CustomDropdown
            label="Select Subject"
            value={subject}
            setValue={(val) => {
              setSubject(val);
              setChapter("");
            }}
            options={subjects}
            disabled={!grade}
          />

          <CustomDropdown
            label="Choose Chapter"
            value={chapter}
            setValue={setChapter}
            options={chapters}
            disabled={!subject}
          />
        </div>

        <motion.button
          whileHover={{ scale: 1.06 }}
          whileTap={{ scale: 0.96 }}
          onClick={openChat}
          disabled={!grade || !subject}
          className="mt-8 w-full py-4 rounded-xl
          bg-gradient-to-r from-pink-500 via-cyan-500 to-green-400
          text-white font-bold text-lg
          shadow-[0_0_30px_rgba(0,255,255,0.4)]
          transition-all duration-300"
        >
          Open Chat
        </motion.button>
      </motion.div>
    </div>
  );
}