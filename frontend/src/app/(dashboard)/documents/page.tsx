"use client";

import { useState } from "react";
import { FileText, Upload, RefreshCw, Trash2, Eye, CheckCircle2, ShieldCheck, AlertCircle } from "lucide-react";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState([
    {
      id: "doc_1",
      name: "Passport Photograph",
      type: "JPG",
      size: "45 KB",
      status: "VALIDATED",
      last_updated: "2026-08-01",
      file_path: "/vault/photo_candidate.jpg",
    },
    {
      id: "doc_2",
      name: "Specimen Signature",
      type: "JPG",
      size: "28 KB",
      status: "VALIDATED",
      last_updated: "2026-08-01",
      file_path: "/vault/sig_candidate.jpg",
    },
    {
      id: "doc_3",
      name: "Class 10 Matriculation Certificate",
      type: "PDF",
      size: "340 KB",
      status: "VALIDATED",
      last_updated: "2026-08-02",
      file_path: "/vault/10th_certificate.pdf",
    },
    {
      id: "doc_4",
      name: "B.Tech Degree Certificate",
      type: "PDF",
      size: "820 KB",
      status: "VALIDATED",
      last_updated: "2026-08-02",
      file_path: "/vault/degree_certificate.pdf",
    },
    {
      id: "doc_5",
      name: "OBC Category Certificate",
      type: "PDF",
      size: "410 KB",
      status: "VALIDATED",
      last_updated: "2026-08-03",
      file_path: "/vault/obc_certificate.pdf",
    },
  ]);

  const [message, setMessage] = useState<string | null>(null);

  const handleUploadSim = (docName: string) => {
    setMessage(`Simulated document upload for '${docName}'. File validated!`);
    setTimeout(() => setMessage(null), 3000);
  };

  const handleDelete = (id: string, name: string) => {
    setDocuments(documents.filter((d) => d.id !== id));
    setMessage(`Document '${name}' removed from vault.`);
    setTimeout(() => setMessage(null), 3000);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Candidate Document Vault</h1>
          <p className="text-sm text-muted-foreground">
            Manage official certificates, photographs, and signatures auto-attached during portal browser automation.
          </p>
        </div>

        <div className="px-3.5 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold flex items-center gap-1.5">
          <ShieldCheck className="w-4 h-4" /> Vault Encrypted & Validated
        </div>
      </div>

      {message && (
        <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold animate-fadeIn">
          {message}
        </div>
      )}

      {/* Upload Zone */}
      <div className="p-8 rounded-2xl bg-card/40 border-2 border-dashed border-border/80 hover:border-primary/50 text-center space-y-3 transition-colors cursor-pointer">
        <div className="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mx-auto">
          <Upload className="w-6 h-6" />
        </div>
        <div>
          <div className="text-sm font-bold text-foreground">Click or Drag & Drop Document</div>
          <p className="text-xs text-muted-foreground mt-0.5">
            Supported Formats: PDF, JPG, PNG (Max File Size: 2 MB)
          </p>
        </div>
      </div>

      {/* Document List */}
      <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/80 space-y-4">
        <h2 className="text-sm font-bold text-foreground uppercase tracking-wider text-[11px]">
          Uploaded Candidate Documents ({documents.length})
        </h2>

        <div className="divide-y divide-border/40">
          {documents.map((doc) => (
            <div key={doc.id} className="py-3.5 flex items-center justify-between gap-4 hover:bg-muted/30 px-3 rounded-xl transition-colors text-xs">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20 flex items-center justify-center font-bold text-[11px]">
                  {doc.type}
                </div>
                <div>
                  <div className="font-bold text-foreground">{doc.name}</div>
                  <div className="text-[11px] text-muted-foreground">
                    Size: {doc.size} • Updated: {doc.last_updated}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold text-[10px] border border-emerald-500/20 flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" /> Validated
                </span>

                <div className="flex items-center gap-1">
                  <button
                    onClick={() => setMessage(`Previewing '${doc.name}'...`)}
                    className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted/60 transition-colors"
                    title="Preview Document"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleUploadSim(doc.name)}
                    className="p-1.5 rounded-lg text-muted-foreground hover:text-blue-400 hover:bg-muted/60 transition-colors"
                    title="Replace Document"
                  >
                    <RefreshCw className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(doc.id, doc.name)}
                    className="p-1.5 rounded-lg text-muted-foreground hover:text-red-400 hover:bg-muted/60 transition-colors"
                    title="Delete Document"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
