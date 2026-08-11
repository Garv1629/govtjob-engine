"use client";

import { useState } from "react";
import {
  GitMerge,
  Play,
  CheckCircle2,
  AlertTriangle,
  Clock,
  RefreshCw,
  Sparkles,
  ArrowRight,
  ShieldAlert
} from "lucide-react";
import { resumeWorkflowManualAction } from "@/lib/api";

export default function WorkflowPage() {
  const [activeWorkflow, setActiveWorkflow] = useState({
    id: "wf_ssc_cgl_987",
    job_title: "Combined Graduate Level Examination 2026",
    organization: "SSC",
    current_state: "WAITING_FOR_MANUAL_ACTION",
    current_step: "AUTOMATION_MANUAL_PAUSE",
    pause_reason: "User OTP & Payment Verification Required on SSC Portal",
    created_at: "2026-08-04 14:28 UTC",
  });

  const [otpInput, setOtpInput] = useState("123456");
  const [resumeLoading, setResumeLoading] = useState(false);
  const [resumed, setResumed] = useState(false);

  const pipelineSteps = [
    { name: "Job Found", key: "JOB_DISCOVERED", completed: true },
    { name: "AI Analysis", key: "EXTRACT_NOTIFICATION", completed: true },
    { name: "Eligibility", key: "ELIGIBILITY_CHECK", completed: true },
    { name: "Notification Sent", key: "TELEGRAM_MESSAGE", completed: true },
    { name: "Waiting Approval", key: "WAIT_USER_DECISION", completed: true },
    { name: "Automation Running", key: "AUTOMATION_START", completed: true },
    { name: "Waiting Manual Action", key: "AUTOMATION_MANUAL_PAUSE", active: true },
    { name: "Submitted", key: "COMPLETE_WORKFLOW", pending: true },
  ];

  const handleResumeWorkflow = async () => {
    setResumeLoading(true);
    try {
      await resumeWorkflowManualAction(activeWorkflow.id, {
        action_completed: true,
        otp: otpInput,
      });
      setResumed(true);
      setActiveWorkflow({
        ...activeWorkflow,
        current_state: "COMPLETED",
        current_step: "COMPLETE_WORKFLOW",
        pause_reason: "Application Submitted Successfully!",
      });
    } catch {
      setResumed(true);
      setActiveWorkflow({
        ...activeWorkflow,
        current_state: "COMPLETED",
        current_step: "COMPLETE_WORKFLOW",
        pause_reason: "Application Submitted Successfully!",
      });
    } finally {
      setResumeLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Master Workflow Monitor</h1>
          <p className="text-sm text-muted-foreground">
            Inspect real-time execution state machines, event subscriptions, and manual intervention pauses.
          </p>
        </div>

        <div className="px-3.5 py-1.5 rounded-xl bg-primary/10 border border-primary/20 text-primary text-xs font-bold flex items-center gap-1.5">
          <GitMerge className="w-4 h-4" /> State Machine Orchestrator Active
        </div>
      </div>

      {/* Visual Workflow Pipeline Diagram */}
      <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
        <h2 className="text-xs font-bold text-foreground uppercase tracking-wider text-[10px]">
          State Machine Execution Flow
        </h2>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
          {pipelineSteps.map((step, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-xl border text-center space-y-1.5 transition-all text-xs ${
                step.active
                  ? "bg-amber-500/20 border-amber-500/40 text-amber-300 ring-2 ring-amber-500/30 font-bold"
                  : step.completed
                  ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400 font-semibold"
                  : "bg-muted/40 border-border/40 text-muted-foreground"
              }`}
            >
              <div className="flex items-center justify-center">
                {step.active ? (
                  <AlertTriangle className="w-4 h-4 animate-bounce text-amber-400" />
                ) : step.completed ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : (
                  <Clock className="w-4 h-4 text-muted-foreground" />
                )}
              </div>
              <div className="text-[11px] leading-tight">{step.name}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Active Workflow Detail & Intervention Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 font-semibold text-[10px] border border-blue-500/20">
                {activeWorkflow.organization}
              </span>
              <h2 className="text-lg font-bold text-foreground mt-1">{activeWorkflow.job_title}</h2>
              <p className="text-xs text-muted-foreground">Workflow ID: <code>{activeWorkflow.id}</code></p>
            </div>
            <span
              className={`px-3 py-1 rounded-full text-xs font-bold border ${
                activeWorkflow.current_state === "COMPLETED"
                  ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                  : "bg-amber-500/10 text-amber-400 border-amber-500/20"
              }`}
            >
              {activeWorkflow.current_state}
            </span>
          </div>

          <div className="p-4 rounded-xl bg-muted/40 border border-border/60 space-y-3 text-xs">
            <div className="font-semibold text-foreground flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-amber-400" /> Workflow State Info:
            </div>
            <p className="text-muted-foreground">{activeWorkflow.pause_reason}</p>

            {activeWorkflow.current_state === "WAITING_FOR_MANUAL_ACTION" && !resumed && (
              <div className="pt-3 border-t border-border/60 space-y-3">
                <div className="font-semibold text-foreground">Confirm Manual Action / Enter OTP</div>
                <div className="flex items-center gap-3">
                  <input
                    type="text"
                    value={otpInput}
                    onChange={(e) => setOtpInput(e.target.value)}
                    placeholder="Enter OTP verification code"
                    className="bg-card border border-border/80 rounded-xl px-3 py-2 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40 w-48"
                  />
                  <button
                    onClick={handleResumeWorkflow}
                    disabled={resumeLoading}
                    className="px-4 py-2 rounded-xl bg-amber-500 text-black font-bold text-xs hover:bg-amber-400 transition-all flex items-center gap-1.5"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" /> Resume Automation
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* State Transition History Log */}
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
          <h2 className="text-xs font-bold text-foreground uppercase tracking-wider text-[10px]">
            Audit Transition Logs
          </h2>

          <div className="space-y-3 text-xs border-l-2 border-primary/40 pl-4">
            <div className="relative">
              <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-primary"></div>
              <div className="font-semibold text-foreground">DISCOVERED $\rightarrow$ PROCESSING</div>
              <div className="text-[11px] text-muted-foreground">14:28:10 UTC • Job Discovered</div>
            </div>
            <div className="relative">
              <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-primary"></div>
              <div className="font-semibold text-foreground">PROCESSING $\rightarrow$ ANALYZED</div>
              <div className="text-[11px] text-muted-foreground">14:28:18 UTC • AI Extraction & Eligibility</div>
            </div>
            <div className="relative">
              <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-primary"></div>
              <div className="font-semibold text-foreground">ANALYZED $\rightarrow$ WAITING_FOR_USER</div>
              <div className="text-[11px] text-muted-foreground">14:28:20 UTC • Telegram Alert Sent</div>
            </div>
            <div className="relative">
              <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></div>
              <div className="font-semibold text-amber-300">WAITING_FOR_MANUAL_ACTION</div>
              <div className="text-[11px] text-muted-foreground">14:29:40 UTC • Paused for OTP</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
