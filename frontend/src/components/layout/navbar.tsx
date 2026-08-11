"use client";

import { Bell, Search, RefreshCw, Cpu } from "lucide-react";
import { ThemeToggle } from "./theme-toggle";

export function Navbar() {
  return (
    <header className="h-16 border-b border-border bg-card/40 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-3 w-96">
        <div className="relative w-full">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search jobs, advertisement numbers, applications..."
            className="w-full bg-muted/50 text-xs rounded-xl pl-9 pr-4 py-2 border border-border/50 focus:outline-none focus:ring-2 focus:ring-primary/40 text-foreground placeholder:text-muted-foreground transition-all"
          />
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
          <Cpu className="w-3.5 h-3.5 animate-pulse" />
          <span>Orchestrator v1.0.0</span>
        </div>

        <button
          onClick={() => window.location.reload()}
          className="p-2 rounded-xl text-muted-foreground hover:text-foreground hover:bg-muted/60 transition-colors"
          title="Refresh Data"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        <button
          className="p-2 rounded-xl text-muted-foreground hover:text-foreground hover:bg-muted/60 transition-colors relative"
          title="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="w-2 h-2 rounded-full bg-primary absolute top-1.5 right-1.5 ring-2 ring-background"></span>
        </button>

        <ThemeToggle />
      </div>
    </header>
  );
}
