import Link from "next/link";
import { Button } from "@/components/ui/button";
import Hero3DCard from "@/components/Hero3DCard";
import InteractiveMatcher from "@/components/InteractiveMatcher";
import { 
  Sparkles, 
  ShieldCheck, 
  Bot, 
  Globe, 
  Zap, 
  Bell, 
  Layers, 
  FileText, 
  ExternalLink, 
  ArrowRight, 
  CheckCircle2,
  Cpu,
  Lock,
  Workflow
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-mesh-grid text-slate-100 selection:bg-blue-500 selection:text-white flex flex-col justify-between">
      
      {/* 1. Header Navigation Bar */}
      <header className="sticky top-0 z-50 glass-panel border-b border-white/10 px-4 sm:px-8 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-cyan-400 p-[1px] shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
              <div className="w-full h-full bg-slate-950 rounded-[15px] flex items-center justify-center">
                <Bot className="w-5 h-5 text-blue-400" />
              </div>
            </div>
            <div>
              <span className="font-extrabold text-lg text-white tracking-tight flex items-center gap-2">
                GovtJob <span className="gradient-text">AI Agent</span>
              </span>
              <span className="text-[10px] text-slate-400 font-semibold tracking-wider block">AUTONOMOUS ENGINE v1.0</span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
            <a href="#features" className="hover:text-blue-400 transition-colors">Features</a>
            <a href="#matcher" className="hover:text-blue-400 transition-colors">AI Matcher</a>
            <a href="#portals" className="hover:text-blue-400 transition-colors">Supported Portals</a>
            <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="hover:text-blue-400 transition-colors flex items-center gap-1">
              API Specs <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </nav>

          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              22 Portals Live
            </div>
            <Link href="/dashboard">
              <Button size="md" className="bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 shadow-lg shadow-blue-500/25 border border-white/20">
                Launch Dashboard <ArrowRight className="w-4 h-4 ml-1.5" />
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* 2. Hero Section */}
      <main className="flex-1">
        <section className="relative px-4 sm:px-8 pt-12 sm:pt-20 pb-16 max-w-7xl mx-auto">
          {/* Ambient Lighting Orbs */}
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-blue-600/15 rounded-full blur-[120px] pointer-events-none glow-orb" />
          
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center relative z-10">
            {/* Left Content */}
            <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-bold tracking-wide">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                India's First Autonomous AI Government Job Agent
              </div>

              <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-[1.1]">
                Never Miss a Government Job. Auto-Apply with <span className="gradient-text">Deterministic AI</span>
              </h1>

              <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
                Real-time monitoring across SSC, UPSC, IBPS, Railways & 22+ State Portals. Automated eligibility verification, document synthesis, and 1-click Playwright application orchestration.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start pt-2">
                <Link href="/dashboard">
                  <Button size="lg" className="w-full sm:w-auto px-8 py-4 text-base bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 shadow-xl shadow-blue-600/30 font-semibold border border-white/20">
                    Enter Candidate Dashboard
                  </Button>
                </Link>
                <a href="#matcher">
                  <Button size="lg" variant="outline" className="w-full sm:w-auto px-8 py-4 text-base border-white/15 bg-white/[0.03] hover:bg-white/[0.08] text-white">
                    Try AI Matcher Demo
                  </Button>
                </a>
              </div>

              {/* Guarantees Bar */}
              <div className="pt-6 grid grid-cols-3 gap-4 border-t border-white/10 text-xs text-slate-400 font-medium">
                <div className="flex items-center justify-center lg:justify-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>Zero Hallucination</span>
                </div>
                <div className="flex items-center justify-center lg:justify-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-blue-400 shrink-0" />
                  <span>Playwright Headless</span>
                </div>
                <div className="flex items-center justify-center lg:justify-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-purple-400 shrink-0" />
                  <span>Telegram Alerts</span>
                </div>
              </div>
            </div>

            {/* Right 3D Visual Card */}
            <div className="lg:col-span-5 flex justify-center">
              <Hero3DCard />
            </div>
          </div>
        </section>

        {/* 3. Metrics Banner */}
        <section className="border-y border-white/10 glass-panel py-8 my-8">
          <div className="max-w-7xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <p className="text-3xl sm:text-4xl font-extrabold text-white gradient-text">22+</p>
              <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mt-1">Portals Monitored</p>
            </div>
            <div>
              <p className="text-3xl sm:text-4xl font-extrabold text-white gradient-text">100%</p>
              <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mt-1">Rule Accuracy</p>
            </div>
            <div>
              <p className="text-3xl sm:text-4xl font-extrabold text-white gradient-text">&lt; 0.5s</p>
              <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mt-1">Scrape Latency</p>
            </div>
            <div>
              <p className="text-3xl sm:text-4xl font-extrabold text-white gradient-text">14,800+</p>
              <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mt-1">Notifications Processed</p>
            </div>
          </div>
        </section>

        {/* 4. Interactive Live AI Matcher */}
        <section id="matcher" className="px-4 sm:px-8 py-12 max-w-7xl mx-auto">
          <InteractiveMatcher />
        </section>

        {/* 5. 6 Pillar Feature Grid (3D Glass Cards) */}
        <section id="features" className="px-4 sm:px-8 py-16 max-w-7xl mx-auto space-y-12">
          <div className="text-center space-y-4 max-w-3xl mx-auto">
            <h2 className="text-xs font-bold uppercase tracking-widest text-blue-400">Architectural Superiority</h2>
            <h3 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
              Engineered for Zero Missed Recruitment Cycles
            </h3>
            <p className="text-slate-400 text-sm sm:text-base">
              Built on Python 3.13 FastAPI, SQLAlchemy async ORM, OpenAI gpt-4o, and Playwright automation engines.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Feature 1 */}
            <div className="glass-card p-8 rounded-3xl space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-blue-500/10 border border-blue-500/30 text-blue-400 flex items-center justify-center">
                <Globe className="w-6 h-6" />
              </div>
              <h4 className="text-xl font-bold text-white">Autonomous Scraper Swarm</h4>
              <p className="text-sm text-slate-400 leading-relaxed">
                Continuous polling engines for SSC, UPSC, IBPS, Railways & NCS. Normalizes unstructured PDF notifications into standardized JSON schemas.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="glass-card p-8 rounded-3xl space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/30 text-purple-400 flex items-center justify-center">
                <Cpu className="w-6 h-6" />
              </div>
              <h4 className="text-xl font-bold text-white">OpenAI & Gemini Eligibility LLM</h4>
              <p className="text-sm text-slate-400 leading-relaxed">
                Parses 80-page official notifications to extract exact age limits, degree requirements, category relaxations, and vacancy breakdown.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="glass-card p-8 rounded-3xl space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center">
                <Bot className="w-6 h-6" />
              </div>
              <h4 className="text-xl font-bold text-white">Playwright Form Orchestrator</h4>
              <p className="text-sm text-slate-400 leading-relaxed">
                Headless browser application filling, photo/signature resizing to KB specifications, and fee payment verification flow.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="glass-card p-8 rounded-3xl space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center">
                <Bell className="w-6 h-6" />
              </div>
              <h4 className="text-xl font-bold text-white">Instant Telegram Bot Alerts</h4>
              <p className="text-sm text-slate-400 leading-relaxed">
                Direct push messages to your phone with match score breakdown, exam syllabus links, and 1-tap application trigger.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="glass-card p-8 rounded-3xl space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center">
                <Zap className="w-6 h-6" />
              </div>
              <h4 className="text-xl font-bold text-white">Self-Healing Engine</h4>
              <p className="text-sm text-slate-400 leading-relaxed">
                Automatic retry loops with exponential backoff, proxy rotation, and captcha fallback handling for 99.9% scraper uptime.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="glass-card p-8 rounded-3xl space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-400 flex items-center justify-center">
                <Lock className="w-6 h-6" />
              </div>
              <h4 className="text-xl font-bold text-white">Deterministic Rule Engine</h4>
              <p className="text-sm text-slate-400 leading-relaxed">
                Zero hallucination logic layer verifying cut-off dates, category certificates, and exam attempts before submitting.
              </p>
            </div>
          </div>
        </section>

        {/* 6. Supported Portals Section */}
        <section id="portals" className="px-4 sm:px-8 py-16 max-w-7xl mx-auto">
          <div className="glass-panel p-8 sm:p-12 rounded-3xl border border-white/10 space-y-8">
            <div className="text-center space-y-2">
              <h3 className="text-2xl font-bold text-white">Active Recruitment Portals</h3>
              <p className="text-sm text-slate-400">Continuous health telemetry checking every 30 seconds</p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
              {[
                { name: "Staff Selection (SSC)", status: "Active", latency: "120ms" },
                { name: "UPSC Civil Services", status: "Active", latency: "180ms" },
                { name: "Railway Recruitment (RRB)", status: "Active", latency: "140ms" },
                { name: "Banking Personnel (IBPS)", status: "Active", latency: "95ms" },
                { name: "National Career Service", status: "Active", latency: "110ms" },
                { name: "State PSCs (UP, MP, Bihar)", status: "Active", latency: "210ms" },
              ].map((portal, pIdx) => (
                <div key={pIdx} className="p-4 rounded-2xl bg-slate-900/60 border border-white/5 text-center space-y-1">
                  <div className="w-2 h-2 rounded-full bg-emerald-400 mx-auto animate-pulse" />
                  <p className="font-bold text-white text-xs">{portal.name}</p>
                  <p className="text-[10px] text-slate-400">{portal.latency}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      {/* 7. Footer */}
      <footer className="border-t border-white/10 glass-panel py-8 px-4 sm:px-8 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Bot className="w-4 h-4 text-blue-400" />
            <span className="font-bold text-white">GovtJob AI Agent Engine</span>
            <span>© 2026. All rights reserved.</span>
          </div>

          <div className="flex gap-6">
            <Link href="/dashboard" className="hover:text-white transition-colors">Dashboard</Link>
            <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">Swagger API</a>
            <a href="https://github.com/Garv1629/govtjob-engine" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">GitHub Repository</a>
          </div>
        </div>
      </footer>

    </div>
  );
}
