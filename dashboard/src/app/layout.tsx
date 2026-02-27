import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LaunchPulse Dashboard",
  description: "Automated idea validation pipeline — monitor your ideas and campaigns",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
