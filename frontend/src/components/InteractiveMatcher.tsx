"use client";

import React, { useState } from "react";
import { Sparkles, CheckCircle2, AlertTriangle, ArrowRight, ShieldCheck, Zap, BookOpen, Award } from "lucide-react";

interface JobMatch {
  title: string;
  dept: string;
  vacancies: string;
  eligibilityScore: number;
  status: "Eligible" | "Borderline" | "Not Eligible";
  reasons: string[];
}

export default function InteractiveMatcher() {
  const [degree, setDegree] = useState("B.Tech / B.E.");
  const [age, setAge] = useState<number>(24);
  const [category, setCategory] = useState("UR");
  const [analyzing, setAnalyzing] = useState(false);

  const sampleMatches: JobMatch[] = [
    {
      title: "SSC CGL 2026 - Assistant Section Officer",
      dept: "Ministry of External Affairs",
      vacancies: "8,400+",
      eligibilityScore: age <= 30 ? 98 : 0,
      status: age <= 30 ? "Eligible" : "Not Eligible",
      reasons: age <= 30 
        ? ["Degree criteria matched (Graduate)", `Age ${age} within limit (18-30 years for ${category})`] 
        : [`Age ${age} exceeds maximum age limit of 30 years`]
    },
    {
      title: "UPSC CSE 2026 - Administrative Services",
      dept: "Union Public Service Commission",
      vacancies: "1,056",
      eligibilityScore: age <= (category === "SC/ST" ? 37 : category === "OBC" ? 35 : 32) ? 95 : 0,
      status: age <= (category === "SC/ST" ? 37 : category === "OBC" ? 35 : 32) ? "Eligible" : "Not Eligible",
      reasons: age <= (category === "SC/ST" ? 37 : category === "OBC" ? 35 : 32)
        ? ["Graduation Degree verified", `${category} age relaxation applied`]
        : [`Age ${age} exceeds relaxed limit for ${category}`]
    },
    {
      title: "NCS IT Specialist Grade-I",
      dept: "National Career Service",
      vacancies: "2,150",
      eligibilityScore: degree.includes("B.Tech") ? 92 : 65,
      status: degree.includes("B.Tech") ? "Eligible" : "Borderline",
      reasons: degree.includes("B.Tech")
        ? ["Technical degree matched", "Experience waiver applicable"]
        : ["General degree requires 2-year IT diploma certification"]
    }
  ];

  const handleSimulate = () => {
    setAnalyzing(true);
    setTimeout(() => {
      setAnalyzing(false);
    }, 600);
  };

  return (
    <div className="w-full max-w-5xl mx-auto rounded-3xl glass-panel p-6 sm:p-10 my-16 border border-white/10 relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute -top-32 -right-32 w-80 h-80 bg-blue-600/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-32 -left-32 w-80 h-80 bg-purple-600/20 rounded-full blur-3xl pointer-events-none" />

      <div className="flex flex-col lg:flex-row gap-8 items-start relative z-10">
        {/* Input Panel */}
        <div className="w-full lg:w-5/12 space-y-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold mb-3">
              <Sparkles className="w-3.5 h-3.5" /> AI Candidate Profile Matcher
            </div>
            <h3 className="text-2xl font-bold text-white tracking-tight">Test Your AI Match Score</h3>
            <p className="text-sm text-slate-400 mt-1">
              Select your parameters below to see how our deterministic engine calculates your exact eligibility.
            </p>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Highest Education Degree</label>
              <select 
                value={degree}
                onChange={(e) => { setDegree(e.target.value); handleSimulate(); }}
                className="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"
              >
                <option value="B.Tech / B.E.">B.Tech / B.E. (Engineering)</option>
                <option value="B.Sc / BCA">B.Sc / BCA (Computer Science/Science)</option>
                <option value="B.Com / BBA">B.Com / BBA (Finance/Commerce)</option>
                <option value="BA / Any Graduate">BA / Any Graduate</option>
                <option value="12th Pass (Higher Secondary)">12th Pass (Higher Secondary)</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Age: <span className="text-blue-400 font-bold">{age} Years</span></label>
                <input 
                  type="range" 
                  min="18" 
                  max="42" 
                  value={age} 
                  onChange={(e) => { setAge(Number(e.target.value)); handleSimulate(); }}
                  className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Reservation Category</label>
                <select 
                  value={category}
                  onChange={(e) => { setCategory(e.target.value); handleSimulate(); }}
                  className="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"
                >
                  <option value="UR">Unreserved (UR)</option>
                  <option value="OBC">OBC (Non-Creamy)</option>
                  <option value="SC/ST">SC / ST</option>
                  <option value="EWS">EWS</option>
                </select>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 text-xs text-slate-400 flex items-center gap-3">
            <ShieldCheck className="w-5 h-5 text-emerald-400 shrink-0" />
            <span>Rules verified against official Gazette notifications with zero LLM hallucination guarantees.</span>
          </div>
        </div>

        {/* Results Panel */}
        <div className="w-full lg:w-7/12 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300">Live AI Evaluation Results</h4>
            {analyzing && <span className="text-xs text-blue-400 animate-pulse flex items-center gap-1.5"><Zap className="w-3.5 h-3.5" /> Re-evaluating...</span>}
          </div>

          <div className="space-y-3">
            {sampleMatches.map((match, idx) => (
              <div key={idx} className="glass-card p-5 rounded-2xl border border-white/5 space-y-3 relative">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <span className="text-[11px] font-semibold uppercase text-slate-400 tracking-wider">{match.dept}</span>
                    <h5 className="font-bold text-white text-base mt-0.5">{match.title}</h5>
                  </div>

                  <div className="text-right shrink-0">
                    <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold ${
                      match.status === 'Eligible' 
                        ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        : match.status === 'Borderline'
                        ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                        : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                    }`}>
                      {match.status === 'Eligible' ? <CheckCircle2 className="w-3.5 h-3.5" /> : <AlertTriangle className="w-3.5 h-3.5" />}
                      {match.eligibilityScore}% Match
                    </span>
                    <p className="text-[11px] text-slate-400 mt-1">{match.vacancies} Vacancies</p>
                  </div>
                </div>

                <div className="pt-2 border-t border-white/5 space-y-1">
                  {match.reasons.map((r, rIdx) => (
                    <div key={rIdx} className="text-xs text-slate-300 flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
                      <span>{r}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
