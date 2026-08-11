import type { Metadata } from "next";
import "@/app/globals.css";

export const metadata: Metadata = {
  title: "GovtJob AI Agent - Automated Recruitment & Eligibility Platform",
  description: "AI-driven real-time government job monitoring, eligibility matching, and automated application assistant.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased">{children}</body>
    </html>
  );
}
