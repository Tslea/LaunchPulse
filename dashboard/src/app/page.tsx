export default function Home() {
  return (
    <main
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        padding: "2rem",
        textAlign: "center",
      }}
    >
      <h1
        style={{
          fontSize: "clamp(2rem, 5vw, 3.5rem)",
          fontWeight: 800,
          letterSpacing: "-0.02em",
          marginBottom: "1rem",
        }}
      >
        Launch<span style={{ color: "var(--accent)" }}>Pulse</span>
      </h1>
      <p
        style={{
          fontSize: "1.25rem",
          color: "var(--text-secondary)",
          maxWidth: "480px",
          lineHeight: 1.6,
        }}
      >
        Dashboard coming soon. The backend API is live at{" "}
        <code
          style={{
            background: "#f0f0f5",
            padding: "2px 6px",
            borderRadius: "4px",
            fontSize: "0.9em",
          }}
        >
          /api/v1
        </code>
      </p>
      <div
        style={{
          marginTop: "2rem",
          display: "flex",
          gap: "1rem",
          flexWrap: "wrap",
          justifyContent: "center",
        }}
      >
        <a
          href="/api/v1/docs"
          style={{
            display: "inline-flex",
            padding: "12px 24px",
            background: "var(--accent)",
            color: "#fff",
            borderRadius: "8px",
            fontWeight: 600,
            textDecoration: "none",
          }}
        >
          API Docs
        </a>
        <a
          href="/health"
          style={{
            display: "inline-flex",
            padding: "12px 24px",
            background: "#f0f0f5",
            color: "var(--text)",
            borderRadius: "8px",
            fontWeight: 600,
            textDecoration: "none",
          }}
        >
          Health Check
        </a>
      </div>
    </main>
  );
}
