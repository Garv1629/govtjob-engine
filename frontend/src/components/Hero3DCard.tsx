"use client";

import React, { useState } from "react";
import { ShieldCheck, Bot, CheckCircle, Bell, ArrowUpRight, Cpu, Activity, Play } from "lucide-react";

export default function Hero3DCard() {
  const [activeTab, setActiveTab] = useState<"notifications" | "automation">("notifications");

  return (
    <div className="relative w-full max-w-xl mx-auto perspective-1000">
      {/* Glow Backing */}
      <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-500 rounded-3xl blur-2xl opacity-40 animate-pulse-slow" />

      {/* Main 3D Card Shell */}
      <div className="relative glass-panel rounded-3xl p-6 border border-white/15 shadow-2xl tilt-3d space-y-6">
        
        {/* Card Header Bar */}
        <div className="flex items-center justify-between border-b border-white/10 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-blue-500/20 border border-blue-500/40 flex items-center justify-center text-blue-400">
              <Cpu className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <h3 className="font-bold text-white text-sm">GovtJob AI Agent Engine</h3>
              <p className="text-xs text-emerald-400 flex items-center gap-1.5 font-medium">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                Live Swarm Active (22 Portals)
              </p>
            </div>
          </div>

          <div className="flex bg-slate-900/90 p-1 rounded-xl border border-white/10">
            <button 
              onClick={() => setActiveTab("notifications")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === "notifications" ? "bg-blue-600 text-white shadow-lg" : "text-slate-400 hover:text-white"
              }`}
            >
              Feed
            </button>
            <button 
              onClick={() => setActiveTab("automation")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === "automation" ? "bg-purple-600 text-white shadow-lg" : "text-slate-400 hover:text-white"
              }`}
            >
              Playwright
            </button>
          </div>
        </div>

        {/* Tab Content 1: Live Notifications Feed */}
        {activeTab === "notifications" && (
          <div className="space-y-3">
            <div className="p-3.5 rounded-2xl bg-white/[0.03] border border-white/10 hover:border-blue-500/50 transition-all flex items-center justify-between group">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold text-xs">
                  SSC
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white group-hover:text-blue-400 transition-colors">SSC CGL 2026 Notification</h4>
                  <p className="text-[11px] text-slate-400">14,500+ Posts • Group B & C</p>
                </div>
              </div>
              <span className="px-2.5 py-1 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-[10px] font-semibold">
                98.4% Match
              </span>
            </div>

            <div className="p-3.5 rounded-2xl bg-white/[0.03] border border-white/10 hover:border-purple-500/50 transition-all flex items-center justify-between group">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center font-bold text-xs">
                  UPSC
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white group-hover:text-purple-400 transition-colors">Civil Services Prelims 2026</h4>
                  <p className="text-[11px] text-slate-400">1,056 Posts • IAS / IPS / IFS</p>
                </div>
              </div>
              <span className="px-2.5 py-1 rounded-full bg-blue-500/15 border border-blue-500/30 text-blue-400 text-[10px] font-semibold">
                Verified
              </span>
            </div>

            <div className="p-3.5 rounded-2xl bg-white/[0.03] border border-white/10 hover:border-cyan-500/50 transition-all flex items-center justify-between group">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center font-bold text-xs">
                  NCS
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white group-hover:text-cyan-400 transition-colors">IT Specialist & Data Analyst</h4>
                  <p className="text-[11px] text-slate-400">National Career Service Portal</p>
                </div>
              </div>
              <span className="px-2.5 py-1 rounded-full bg-cyan-500/15 border border-cyan-500/30 text-cyan-400 text-[10px] font-semibold">
                Auto-Alerted
              </span>
            </div>
          </div>
        )}

        {/* Tab Content 2: Playwright Headless Automation Status */}
        {activeTab === "automation" && (
          <div className="space-y-3 p-4 rounded-2xl bg-slate-950/80 border border-white/10 text-xs">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-slate-400 flex items-center gap-2"><Play className="w-3.5 h-3.5 text-blue-400" /> Playwright Task ID:</span>
              <span className="font-mono text-blue-400">#PLW-99482</span>
            </div>
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-slate-400">Step 1: Document Upload & Photo Resizing</span>
              <span className="text-emerald-400 font-semibold">Complete ✓</span>
            </div>
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-slate-400">Step 2: Category Fee Payment Orchestration</span>
              <span className="text-emerald-400 font-semibold">Verified ✓</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Step 3: Registration Slip Generation</span>
              <span className="text-blue-400 font-semibold animate-pulse">In Progress...</span>
            </div>
          </div>
        )}

        {/* Live Metric Footer */}
        <div className="pt-2 flex items-center justify-between text-[11px] text-slate-400">
          <span className="flex items-center gap-1.5"><Activity className="w-3.5 h-3.5 text-blue-400" /> 0.42s Scrape Speed</span>
          <span className="flex items-center gap-1.5 text-emerald-400"><ShieldCheck className="w-3.5 h-3.5" /> 100% Deterministic Guarantee</span>
        </div>

      </div>
    </div>
  );
}
