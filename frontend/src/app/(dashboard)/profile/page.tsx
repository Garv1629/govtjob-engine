"use client";

import { useState } from "react";
import { User, GraduationCap, Briefcase, FileCheck, Award, Save, CheckCircle2 } from "lucide-react";

export default function ProfilePage() {
  const [profile, setProfile] = useState({
    full_name: "Candidate User",
    date_of_birth: "1998-05-15",
    category: "OBC",
    email: "candidate@example.com",
    phone: "+91 98765 43210",
    qualification: "Bachelor of Technology",
    qualification_major: "Computer Science and Engineering",
    marks_percentage: "78.5%",
    passing_year: "2020",
    years_experience: "2.5 Years",
    current_designation: "Software Engineer",
  });

  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Candidate Profile</h1>
          <p className="text-sm text-muted-foreground">
            Manage your personal credentials, education, and experience used for AI eligibility evaluation and auto-filling portal forms.
          </p>
        </div>
        <div className="px-4 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" /> 100% Profile Readiness
        </div>
      </div>

      {saved && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold animate-fadeIn">
          Profile information updated successfully!
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Personal Details */}
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
          <div className="flex items-center gap-2 text-foreground font-bold text-sm border-b border-border/60 pb-3">
            <User className="w-4 h-4 text-primary" /> Personal Information
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 text-xs">
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Full Name</label>
              <input
                type="text"
                value={profile.full_name}
                onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Date of Birth</label>
              <input
                type="date"
                value={profile.date_of_birth}
                onChange={(e) => setProfile({ ...profile, date_of_birth: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Reservation Category</label>
              <select
                value={profile.category}
                onChange={(e) => setProfile({ ...profile, category: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              >
                <option value="UR">UR (Unreserved)</option>
                <option value="OBC">OBC (Non-Creamy Layer)</option>
                <option value="SC">SC (Scheduled Caste)</option>
                <option value="ST">ST (Scheduled Tribe)</option>
                <option value="EWS">EWS</option>
              </select>
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Email Address</label>
              <input
                type="email"
                value={profile.email}
                onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Mobile Phone</label>
              <input
                type="text"
                value={profile.phone}
                onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
          </div>
        </div>

        {/* Education Details */}
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
          <div className="flex items-center gap-2 text-foreground font-bold text-sm border-b border-border/60 pb-3">
            <GraduationCap className="w-4 h-4 text-primary" /> Educational Qualification
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Highest Qualification</label>
              <input
                type="text"
                value={profile.qualification}
                onChange={(e) => setProfile({ ...profile, qualification: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Major / Specialization</label>
              <input
                type="text"
                value={profile.qualification_major}
                onChange={(e) => setProfile({ ...profile, qualification_major: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Marks / Percentage</label>
              <input
                type="text"
                value={profile.marks_percentage}
                onChange={(e) => setProfile({ ...profile, marks_percentage: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Passing Year</label>
              <input
                type="text"
                value={profile.passing_year}
                onChange={(e) => setProfile({ ...profile, passing_year: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
          </div>
        </div>

        {/* Experience Details */}
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
          <div className="flex items-center gap-2 text-foreground font-bold text-sm border-b border-border/60 pb-3">
            <Briefcase className="w-4 h-4 text-primary" /> Work Experience
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Total Experience</label>
              <input
                type="text"
                value={profile.years_experience}
                onChange={(e) => setProfile({ ...profile, years_experience: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Current Designation</label>
              <input
                type="text"
                value={profile.current_designation}
                onChange={(e) => setProfile({ ...profile, current_designation: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            className="px-6 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-xs hover:opacity-90 transition-all flex items-center gap-2 shadow-lg shadow-primary/20"
          >
            <Save className="w-4 h-4" /> Save Candidate Profile
          </button>
        </div>
      </form>
    </div>
  );
}
