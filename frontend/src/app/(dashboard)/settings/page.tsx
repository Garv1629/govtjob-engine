"use client";

import { useState } from "react";
import { Settings, Bot, Cpu, Clock, Sliders, Bell, CheckCircle2, Save } from "lucide-react";

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    telegram_bot_token: "••••••••••••••••••••••••••••••••••••",
    telegram_allowed_ids: "123456789, 987654321",
    telegram_enabled: true,
    ai_model: "GEMINI_3_PRO",
    ai_temperature: 0.2,
    eligibility_threshold: 70,
    poll_interval_minutes: 30,
    auto_retry_max: 3,
    enable_ssc: true,
    enable_upsc: true,
    enable_ncs: true,
    enable_rrb: true,
    auto_apply_high_match: false,
  });

  const [saved, setSaved] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">System Preferences & Settings</h1>
        <p className="text-sm text-muted-foreground">
          Configure Telegram AI bot tokens, AI extraction models, scraper poll frequencies, and automation thresholds.
        </p>
      </div>

      {saved && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold animate-fadeIn flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" /> Settings updated successfully!
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Telegram Configuration */}
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
          <div className="flex items-center gap-2 text-foreground font-bold text-sm border-b border-border/60 pb-3">
            <Bot className="w-4 h-4 text-primary" /> Telegram Command Center Configuration
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Telegram Bot Token</label>
              <input
                type="password"
                value={settings.telegram_bot_token}
                onChange={(e) => setSettings({ ...settings, telegram_bot_token: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40 font-mono"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Allowed Telegram User IDs</label>
              <input
                type="text"
                value={settings.telegram_allowed_ids}
                onChange={(e) => setSettings({ ...settings, telegram_allowed_ids: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40 font-mono"
              />
            </div>
          </div>
        </div>

        {/* AI & Extraction Configuration */}
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
          <div className="flex items-center gap-2 text-foreground font-bold text-sm border-b border-border/60 pb-3">
            <Cpu className="w-4 h-4 text-primary" /> AI Model & Eligibility Engine
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">AI Extraction Model</label>
              <select
                value={settings.ai_model}
                onChange={(e) => setSettings({ ...settings, ai_model: e.target.value })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              >
                <option value="GEMINI_3_PRO">Google Gemini 3 Pro</option>
                <option value="GEMINI_3_FLASH">Google Gemini 3 Flash</option>
                <option value="DEEPSEEK_R1">DeepSeek R1 Orchestrator</option>
              </select>
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Eligibility Score Threshold (%)</label>
              <input
                type="number"
                value={settings.eligibility_threshold}
                onChange={(e) => setSettings({ ...settings, eligibility_threshold: parseInt(e.target.value) })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-muted-foreground font-medium">Temperature</label>
              <input
                type="number"
                step="0.05"
                value={settings.ai_temperature}
                onChange={(e) => setSettings({ ...settings, ai_temperature: parseFloat(e.target.value) })}
                className="w-full bg-card border border-border/80 rounded-xl px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
            </div>
          </div>
        </div>

        {/* Scheduler & Sources */}
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
          <div className="flex items-center gap-2 text-foreground font-bold text-sm border-b border-border/60 pb-3">
            <Clock className="w-4 h-4 text-primary" /> Scheduler & Portal Source Toggles
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <label className="flex items-center gap-2 p-3 rounded-xl bg-muted/40 border border-border/60 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.enable_ssc}
                onChange={(e) => setSettings({ ...settings, enable_ssc: e.target.checked })}
                className="rounded border-border text-primary focus:ring-primary"
              />
              <span className="font-semibold text-foreground">SSC Portal</span>
            </label>
            <label className="flex items-center gap-2 p-3 rounded-xl bg-muted/40 border border-border/60 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.enable_upsc}
                onChange={(e) => setSettings({ ...settings, enable_upsc: e.target.checked })}
                className="rounded border-border text-primary focus:ring-primary"
              />
              <span className="font-semibold text-foreground">UPSC Portal</span>
            </label>
            <label className="flex items-center gap-2 p-3 rounded-xl bg-muted/40 border border-border/60 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.enable_ncs}
                onChange={(e) => setSettings({ ...settings, enable_ncs: e.target.checked })}
                className="rounded border-border text-primary focus:ring-primary"
              />
              <span className="font-semibold text-foreground">NCS Portal</span>
            </label>
            <label className="flex items-center gap-2 p-3 rounded-xl bg-muted/40 border border-border/60 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.enable_rrb}
                onChange={(e) => setSettings({ ...settings, enable_rrb: e.target.checked })}
                className="rounded border-border text-primary focus:ring-primary"
              />
              <span className="font-semibold text-foreground">Railways (RRB)</span>
            </label>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            className="px-6 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-xs hover:opacity-90 transition-all flex items-center gap-2 shadow-lg shadow-primary/20"
          >
            <Save className="w-4 h-4" /> Save System Settings
          </button>
        </div>
      </form>
    </div>
  );
}
