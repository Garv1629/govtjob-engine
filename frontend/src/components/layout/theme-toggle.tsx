"use client";

import { Moon, Sun } from "lucide-react";
import { useState } from "react";

export function ThemeToggle() {
  const [isDark, setIsDark] = useState(true);

  const toggleTheme = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle("dark");
  };

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg text-muted-foreground hover:bg-muted transition-colors"
      title="Toggle Dark / Light Theme"
    >
      {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
    </button>
  );
}
