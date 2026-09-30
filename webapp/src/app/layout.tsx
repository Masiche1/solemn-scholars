import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";

const inter = Inter({ 
  variable: "--rh-next-inter", 
  subsets: ["latin"],
  display: "swap"
});

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0b1020" },
  ],
};

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  applicationName: "Solemn Scholars",
  openGraph: { type: "website", siteName: "Solemn Scholars", title: "Solemn Scholars — Intelligent Learning & Tutor Marketplace" },
  title: {
    default: "Solemn Scholars — Intelligent Learning & Tutor Marketplace",
    template: "%s — Solemn Scholars",
  },
  description:
    "Solemn Scholars unifies IB curriculum learning, AI-powered diagnostics, and verified tutor marketplace in one intelligent platform.",
};

const themeInitScript = `
(function () {
  try {
    var t = localStorage.getItem("rh-theme");
    if (t === "dark" || (!t && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
      document.documentElement.setAttribute("data-theme", "dark");
    }
  } catch (e) {}
})();
`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      data-theme="light"
      className={`${inter.variable}`}
      suppressHydrationWarning
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInitScript }} />
      </head>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
