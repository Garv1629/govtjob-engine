"use client";

import { useState, useEffect } from "react";
import {
  FolderKanban,
  CheckCircle2,
  Clock,
  FileText,
  Image as ImageIcon,
  ExternalLink,
  ChevronRight,
  Sparkles,
  AlertTriangle
} from "lucide-react";
import { getApplications } from "@/lib/api";

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<any[]>([]);
  const [selectedApp, setSelectedApp] = useState<any | null>(null);

  useEffect(() => {
    fetchAppsData();
  }, []);

  const fetchAppsData = async () => {
    try {
      const data = await getApplications();
      setApplications(data && data.length > 0 ? data : getSampleApps());
    } catch {
      setApplications(getSampleApps());
    }
  };

  const getSampleApps = () => [
    {
      id: "app_101",
      workflow_id: "wf_ssc_cgl_987",
      portal: "SSC (Staff Selection Commission)",
      job_title: "Combined Graduate Level Examination 2026",
      application_number: "SSC_2026_98765",
      status: "SUBMITTED",
      submission_time: "2026-08-04 14:30 UTC",
      processing_duration: "18.4s",
      receipt_url: "/receipts/ssc_cgl_receipt.pdf",
      screenshot_url: "/screenshots/ssc_confirmation.png",
      timeline: [
        { step: "Job Discovered", time: "14:28:10", status: "COMPLETED" },
        { step: "AI Notification Extraction", time: "14:28:15", status: "COMPLETED" },
        { step: "Eligibility Evaluation", time: "14:28:18", status: "COMPLETED" },
        { step: "User Approval", time: "14:29:00", status: "COMPLETED" },
        { step: "Playwright Automation Executed", time: "14:29:40", status: "COMPLETED" },
        { step: "Receipt Downloaded & Saved", time: "14:29:58", status: "COMPLETED" },
      ]
    },
    {
      id: "app_102",
      workflow_id: "wf_upsc_cse_104",
      portal: "UPSC (Union Public Service Commission)",
      job_title: "Civil Services Examination 2026",
      application_number: "UPSC_2026_11204",
      status: "SUBMITTED",
      submission_time: "2026-08-03 11:15 UTC",
      processing_duration: "24.1s",
      receipt_url: "/receipts/upsc_cse_receipt.pdf",
      screenshot_url: "/screenshots/upsc_confirmation.png",
      timeline: [
        { step: "Job Discovered", time: "11:10:00", status: "COMPLETED" },
        { step: "AI Notification Extraction", time: "11:10:08", status: "COMPLETED" },
        { step: "Eligibility Evaluation", time: "11:10:12", status: "COMPLETED" },
        { step: "User Approval", time: "11:12:00", status: "COMPLETED" },
        { step: "Playwright Automation Executed", time: "11:14:30", status: "COMPLETED" },
        { step: "Receipt Downloaded & Saved", time: "11:15:24", status: "COMPLETED" },
      ]
    },
    {
      id: "app_103",
      workflow_id: "wf_rrb_ntpc_55",
      portal: "RRB (Railway Recruitment Board)",
      job_title: "NTPC Non-Technical Popular Categories",
      application_number: "Pending OTP",
      status: "WAITING_FOR_MANUAL_ACTION",
      submission_time: "2026-08-04 15:45 UTC",
      processing_duration: "12.0s",
      receipt_url: null,
      screenshot_url: "/screenshots/rrb_otp_pause.png",
      timeline: [
        { step: "Job Discovered", time: "15:40:00", status: "COMPLETED" },
        { step: "AI Notification Extraction", time: "15:40:05", status: "COMPLETED" },
        { step: "Eligibility Evaluation", time: "15:40:09", status: "COMPLETED" },
        { step: "User Approval", time: "15:42:00", status: "COMPLETED" },
        { step: "Form Filling Completed", time: "15:44:10", status: "COMPLETED" },
        { step: "Paused for User OTP & Payment", time: "15:45:00", status: "PAUSED" },
      ]
    }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Application History</h1>
        <p className="text-sm text-muted-foreground">
          Track and inspect automated job application submissions, receipts, and Playwright execution proofs.
        </p>
      </div>

      {/* Applications Table */}
      <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="border-b border-border/60 text-muted-foreground uppercase tracking-wider text-[10px]">
            <tr>
              <th className="pb-3 font-semibold">Portal & Job Title</th>
              <th className="pb-3 font-semibold">Application Number</th>
              <th className="pb-3 font-semibold">Submission Status</th>
              <th className="pb-3 font-semibold">Submission Time</th>
              <th className="pb-3 font-semibold">Proof Assets</th>
              <th className="pb-3 font-semibold text-right">Details</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/40">
            {applications.map((app) => (
              <tr key={app.id} className="hover:bg-muted/40 transition-colors">
                <td className="py-4">
                  <div className="font-bold text-foreground text-sm">{app.job_title}</div>
                  <div className="text-[11px] text-muted-foreground">{app.portal}</div>
                </td>
                <td className="py-4 font-mono font-bold text-foreground">
                  {app.application_number}
                </td>
                <td className="py-4">
                  {app.status === "SUBMITTED" || app.status === "COMPLETED" ? (
                    <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20 text-[11px] flex items-center gap-1 w-fit">
                      <CheckCircle2 className="w-3 h-3" /> Submitted
                    </span>
                  ) : (
                    <span className="px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-400 font-semibold border border-amber-500/20 text-[11px] flex items-center gap-1 w-fit">
                      <AlertTriangle className="w-3 h-3" /> Action Required
                    </span>
                  )}
                </td>
                <td className="py-4 text-muted-foreground font-medium">{app.submission_time}</td>
                <td className="py-4">
                  <div className="flex items-center gap-2">
                    {app.receipt_url && (
                      <span className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 text-[10px] font-semibold border border-blue-500/20 flex items-center gap-1">
                        <FileText className="w-3 h-3" /> Receipt PDF
                      </span>
                    )}
                    <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 text-[10px] font-semibold border border-purple-500/20 flex items-center gap-1">
                      <ImageIcon className="w-3 h-3" /> Screenshot
                    </span>
                  </div>
                </td>
                <td className="py-4 text-right">
                  <button
                    onClick={() => setSelectedApp(app)}
                    className="px-3 py-1.5 rounded-lg bg-primary/10 text-primary hover:bg-primary hover:text-primary-foreground font-semibold text-xs transition-all flex items-center gap-1 ml-auto"
                  >
                    Inspect <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Application Details Modal */}
      {selectedApp && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-md flex items-center justify-center p-4 z-50 animate-fadeIn">
          <div className="bg-card border border-border/80 rounded-2xl max-w-2xl w-full p-6 space-y-6 shadow-2xl overflow-y-auto max-h-[90vh]">
            <div className="flex items-center justify-between border-b border-border/60 pb-4">
              <div>
                <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold text-[10px] border border-emerald-500/20">
                  {selectedApp.portal}
                </span>
                <h2 className="text-xl font-bold text-foreground mt-1">{selectedApp.job_title}</h2>
                <p className="text-xs text-muted-foreground">Application Number: <code className="text-foreground">{selectedApp.application_number}</code></p>
              </div>
              <button
                onClick={() => setSelectedApp(null)}
                className="p-2 rounded-xl text-muted-foreground hover:bg-muted hover:text-foreground"
              >
                ✕
              </button>
            </div>

            {/* Workflow Timeline Execution */}
            <div className="space-y-3">
              <h3 className="text-xs font-bold text-foreground uppercase tracking-wider">Execution Timeline</h3>
              <div className="space-y-2 border-l-2 border-primary/40 pl-4">
                {selectedApp.timeline.map((step: any, idx: number) => (
                  <div key={idx} className="relative text-xs space-y-0.5">
                    <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-primary ring-4 ring-card"></div>
                    <div className="font-semibold text-foreground">{step.step}</div>
                    <div className="text-[11px] text-muted-foreground">{step.time}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Assets */}
            <div className="grid grid-cols-2 gap-4 pt-2">
              <div className="p-4 rounded-xl bg-muted/40 border border-border/60 space-y-2 text-xs">
                <div className="font-semibold text-foreground flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-blue-400" /> Official Application Receipt
                </div>
                <p className="text-muted-foreground text-[11px]">PDF proof generated by portal server</p>
                <button className="w-full py-1.5 rounded-lg bg-card border border-border hover:bg-muted text-xs font-semibold text-foreground transition-all">
                  Download Receipt PDF
                </button>
              </div>

              <div className="p-4 rounded-xl bg-muted/40 border border-border/60 space-y-2 text-xs">
                <div className="font-semibold text-foreground flex items-center gap-1.5">
                  <ImageIcon className="w-4 h-4 text-purple-400" /> Playwright Submission Screenshot
                </div>
                <p className="text-muted-foreground text-[11px]">Captured browser confirmation screen</p>
                <button className="w-full py-1.5 rounded-lg bg-card border border-border hover:bg-muted text-xs font-semibold text-foreground transition-all">
                  Preview Screenshot
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
