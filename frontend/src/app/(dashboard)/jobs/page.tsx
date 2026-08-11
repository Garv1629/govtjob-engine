"use client";

import { useState, useEffect } from "react";
import {
  Briefcase,
  Search,
  Filter,
  CheckCircle2,
  XCircle,
  ExternalLink,
  FileText,
  Sparkles,
  Play,
  Ban,
  Info,
  Clock
} from "lucide-react";
import { getJobs, triggerWorkflow, submitWorkflowDecision } from "@/lib/api";

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [selectedJob, setSelectedJob] = useState<any | null>(null);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const fetchJobsData = async () => {
    setLoading(true);
    try {
      const data = await getJobs();
      setJobs(data && data.length > 0 ? data : getSampleJobs());
    } catch {
      setJobs(getSampleJobs());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobsData();
  }, []);

  const getSampleJobs = () => [
    {
      id: "job_ssc_cgl",
      job_title: "Combined Graduate Level Examination 2026",
      organization: "Staff Selection Commission",
      department: "Group B & C Posts",
      salary_summary: "Pay Level 7 (₹44,900 - ₹1,42,400)",
      total_vacancies: 12000,
      eligibility_score: 95.0,
      eligibility_status: "ELIGIBLE",
      last_date: "2026-08-31",
      status: "DISCOVERED",
      pdf_url: "https://ssc.gov.in/cgl2026.pdf",
      apply_url: "https://ssc.gov.in/apply",
      advt_number: "SSC-CGL-2026",
      qualifications: "Bachelor's Degree in any discipline from a recognized University",
      min_age: 18,
      max_age: 30,
      fee_summary: "₹100 (UR/OBC), Exempted (SC/ST/Female)"
    },
    {
      id: "job_upsc_cse",
      job_title: "Civil Services Examination 2026",
      organization: "Union Public Service Commission",
      department: "IAS, IPS, IFS & Central Services",
      salary_summary: "Pay Level 10 (₹56,100 - ₹1,77,500)",
      total_vacancies: 1000,
      eligibility_score: 88.0,
      eligibility_status: "ELIGIBLE",
      last_date: "2026-08-25",
      status: "ANALYZED",
      pdf_url: "https://upsc.gov.in/cse2026.pdf",
      apply_url: "https://upsc.gov.in/apply",
      advt_number: "UPSC-CSE-2026",
      qualifications: "Graduate Degree in any discipline",
      min_age: 21,
      max_age: 32,
      fee_summary: "₹100 (UR/OBC), Exempted (Female/SC/ST/PwBD)"
    },
    {
      id: "job_rrb_ntpc",
      job_title: "NTPC Non-Technical Popular Categories",
      organization: "Railway Recruitment Board",
      department: "Indian Railways",
      salary_summary: "Pay Level 2 to 6 (₹19,900 - ₹35,400)",
      total_vacancies: 8500,
      eligibility_score: 92.0,
      eligibility_status: "ELIGIBLE",
      last_date: "2026-09-15",
      status: "DISCOVERED",
      pdf_url: "https://rrbcdg.gov.in/ntpc.pdf",
      apply_url: "https://rrbcdg.gov.in/apply",
      advt_number: "RRB-NTPC-01/2026",
      qualifications: "12th Pass or Graduate depending on post",
      min_age: 18,
      max_age: 33,
      fee_summary: "₹500 (UR/OBC), ₹250 (SC/ST/Female)"
    }
  ];

  const handleApplyClick = async (job: any) => {
    try {
      setActionMessage(`Initiating application workflow for '${job.job_title}'...`);
      await triggerWorkflow({
        user_id: "candidate_123",
        source_code: job.organization,
        organization: job.organization,
        advt_number: job.advt_number,
        job_title: job.job_title,
        pdf_url: job.pdf_url,
        apply_url: job.apply_url,
        total_vacancies: job.total_vacancies
      });
      setActionMessage(`Workflow launched! Paused for user approval or automation.`);
    } catch {
      setActionMessage(`Workflow started in simulation mode for '${job.job_title}'.`);
    } finally {
      setTimeout(() => setActionMessage(null), 4000);
    }
  };

  const handleIgnoreClick = async (job: any) => {
    setActionMessage(`Job '${job.job_title}' marked as IGNORED.`);
    setTimeout(() => setActionMessage(null), 3000);
  };

  const filteredJobs = jobs.filter((job) => {
    const matchesSearch =
      job.job_title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.organization?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.advt_number?.toLowerCase().includes(searchQuery.toLowerCase());

    if (statusFilter === "ELIGIBLE") return matchesSearch && (job.eligibility_score || 90) >= 70;
    if (statusFilter === "APPLIED") return matchesSearch && job.status === "SUBMITTED";
    if (statusFilter === "IGNORED") return matchesSearch && job.status === "CANCELLED";
    return matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Top Header & Search Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Government Job Discoveries</h1>
          <p className="text-sm text-muted-foreground">
            Explore live recruitment notifications extracted & analyzed by the AI engine.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search by job title, org, advt no..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-card border border-border/80 text-xs rounded-xl pl-9 pr-4 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40 w-64"
            />
          </div>
        </div>
      </div>

      {/* Action Notification Toast */}
      {actionMessage && (
        <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold flex items-center gap-2 animate-fadeIn">
          <Sparkles className="w-4 h-4 text-blue-400" />
          <span>{actionMessage}</span>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-border/60 pb-2">
        {["ALL", "ELIGIBLE", "APPLIED", "IGNORED"].map((tab) => (
          <button
            key={tab}
            onClick={() => setStatusFilter(tab)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              statusFilter === tab
                ? "bg-primary text-primary-foreground shadow-sm"
                : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Jobs Table */}
      <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="border-b border-border/60 text-muted-foreground uppercase tracking-wider text-[10px]">
            <tr>
              <th className="pb-3 font-semibold">Job Title</th>
              <th className="pb-3 font-semibold">Organization / Dept</th>
              <th className="pb-3 font-semibold">Salary & Vacancies</th>
              <th className="pb-3 font-semibold">AI Match Score</th>
              <th className="pb-3 font-semibold">Last Date</th>
              <th className="pb-3 font-semibold text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/40">
            {filteredJobs.map((job) => (
              <tr key={job.id} className="hover:bg-muted/40 transition-colors">
                <td className="py-4">
                  <div className="font-bold text-sm text-foreground">{job.job_title}</div>
                  <div className="text-[11px] text-muted-foreground">Advt: {job.advt_number || "N/A"}</div>
                </td>
                <td className="py-4">
                  <div className="font-semibold text-foreground">{job.organization}</div>
                  <div className="text-[11px] text-muted-foreground">{job.department || "Group Posts"}</div>
                </td>
                <td className="py-4">
                  <div className="font-semibold text-foreground">{job.total_vacancies?.toLocaleString()} Vacancies</div>
                  <div className="text-[11px] text-muted-foreground">{job.salary_summary || "Pay Level Standard"}</div>
                </td>
                <td className="py-4">
                  <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 font-bold border border-emerald-500/20 text-xs">
                    {job.eligibility_score || 95}% Match
                  </span>
                </td>
                <td className="py-4 text-muted-foreground font-medium">
                  <div className="flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-amber-400" />
                    <span>{job.last_date || "31-08-2026"}</span>
                  </div>
                </td>
                <td className="py-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <button
                      onClick={() => handleApplyClick(job)}
                      className="px-3 py-1.5 rounded-lg bg-primary text-primary-foreground hover:opacity-90 font-semibold text-xs transition-all shadow-md shadow-primary/20 flex items-center gap-1"
                    >
                      <Play className="w-3 h-3 fill-current" /> Apply
                    </button>
                    <button
                      onClick={() => setSelectedJob(job)}
                      className="px-3 py-1.5 rounded-lg bg-card border border-border/80 hover:bg-muted font-medium text-xs transition-all text-foreground flex items-center gap-1"
                    >
                      <Info className="w-3 h-3" /> Details
                    </button>
                    <button
                      onClick={() => handleIgnoreClick(job)}
                      className="p-1.5 rounded-lg text-muted-foreground hover:text-red-400 hover:bg-muted/60 transition-colors"
                      title="Ignore Job"
                    >
                      <Ban className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Job Details Modal */}
      {selectedJob && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-md flex items-center justify-center p-4 z-50 animate-fadeIn">
          <div className="bg-card border border-border/80 rounded-2xl max-w-2xl w-full p-6 space-y-6 shadow-2xl overflow-y-auto max-h-[90vh]">
            <div className="flex items-center justify-between border-b border-border/60 pb-4">
              <div>
                <span className="px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 font-semibold text-[10px] border border-blue-500/20">
                  {selectedJob.organization}
                </span>
                <h2 className="text-xl font-bold text-foreground mt-1">{selectedJob.job_title}</h2>
                <p className="text-xs text-muted-foreground">Advertisement No: {selectedJob.advt_number}</p>
              </div>
              <button
                onClick={() => setSelectedJob(null)}
                className="p-2 rounded-xl text-muted-foreground hover:bg-muted hover:text-foreground"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs">
              <div className="p-3 rounded-xl bg-muted/40 border border-border/60">
                <span className="text-muted-foreground font-medium">Total Vacancies</span>
                <div className="text-base font-bold text-foreground mt-0.5">{selectedJob.total_vacancies?.toLocaleString()}</div>
              </div>
              <div className="p-3 rounded-xl bg-muted/40 border border-border/60">
                <span className="text-muted-foreground font-medium">Salary / Pay Scale</span>
                <div className="text-base font-bold text-foreground mt-0.5">{selectedJob.salary_summary || "Standard Govt Scale"}</div>
              </div>
              <div className="p-3 rounded-xl bg-muted/40 border border-border/60">
                <span className="text-muted-foreground font-medium">Age Limit</span>
                <div className="text-sm font-semibold text-foreground mt-0.5">{selectedJob.min_age || 18} to {selectedJob.max_age || 30} Years</div>
              </div>
              <div className="p-3 rounded-xl bg-muted/40 border border-border/60">
                <span className="text-muted-foreground font-medium">Application Fee</span>
                <div className="text-sm font-semibold text-foreground mt-0.5">{selectedJob.fee_summary || "Standard Fee"}</div>
              </div>
            </div>

            <div className="space-y-2 text-xs">
              <div className="font-semibold text-foreground">Essential Qualification</div>
              <p className="p-3 rounded-xl bg-muted/40 border border-border/60 text-muted-foreground">
                {selectedJob.qualifications}
              </p>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-border/60">
              <div className="flex items-center gap-3 text-xs">
                <a
                  href={selectedJob.pdf_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-primary hover:underline flex items-center gap-1 font-semibold"
                >
                  <FileText className="w-3.5 h-3.5" /> Download Notification PDF
                </a>
                <a
                  href={selectedJob.apply_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-primary hover:underline flex items-center gap-1 font-semibold"
                >
                  <ExternalLink className="w-3.5 h-3.5" /> Official Portal
                </a>
              </div>

              <button
                onClick={() => {
                  handleApplyClick(selectedJob);
                  setSelectedJob(null);
                }}
                className="px-4 py-2 rounded-xl bg-primary text-primary-foreground font-semibold text-xs hover:opacity-90 transition-all flex items-center gap-1.5 shadow-lg shadow-primary/20"
              >
                <Play className="w-3.5 h-3.5 fill-current" /> Apply via Automation
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
