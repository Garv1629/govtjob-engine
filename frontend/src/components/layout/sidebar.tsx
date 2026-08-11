"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Briefcase,
  FolderKanban,
  User,
  FileText,
  GitMerge,
  Activity,
  Terminal,
  Settings,
  ShieldCheck,
  Bot
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Jobs", href: "/jobs", icon: Briefcase },
  { name: "Applications", href: "/applications", icon: FolderKanban },
  { name: "Candidate Profile", href: "/profile", icon: User },
  { name: "Documents Vault", href: "/documents", icon: FileText },
  { name: "Workflow Monitor", href: "/workflow", icon: GitMerge },
  { name: "Scraper Health", href: "/scrapers", icon: Activity },
  { name: "Log Viewer", href: "/logs", icon: Terminal },
  { name: "System Status", href: "/system", icon: ShieldCheck },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-border bg-card/60 backdrop-blur-xl flex flex-col h-screen sticky top-0 z-40">
      <div className="p-5 flex items-center gap-3 border-b border-border/80">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/20">
          <Bot className="w-5 h-5" />
        </div>
        <div>
          <h1 className="font-bold text-base tracking-tight text-foreground">GovtJob AI</h1>
          <p className="text-[11px] text-muted-foreground font-medium">Orchestration Platform</p>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {navigation.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-primary text-primary-foreground font-semibold shadow-md shadow-primary/25"
                  : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"
              )}
            >
              <Icon className="w-4 h-4" />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border/80 text-[11px] text-muted-foreground text-center bg-card/40">
        <div className="flex items-center justify-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Engine Status: Online</span>
        </div>
      </div>
    </aside>
  );
}
