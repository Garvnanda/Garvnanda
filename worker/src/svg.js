// Shared monochrome SVG helpers matching the README theme.

export const THEME = `
  :root { --bone:#444444; --rule:#C0C0C0; --muted:#888888; --accent:#555555; --paper:#FFFFFF; }
  @media (prefers-color-scheme: dark) { :root { --bone:#DDDDDD; --rule:#444444; --muted:#777777; --accent:#AAAAAA; --paper:#111111; } }
  .mono { font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }
`;

export function svgHeaders(extra = {}) {
  return {
    "Content-Type": "image/svg+xml",
    "Cache-Control": "no-store, max-age=0",
    ...extra,
  };
}

export function esc(s = "") {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
