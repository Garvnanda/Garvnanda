import { THEME, svgHeaders, esc } from "./svg.js";

const KEY = "guestbook:entries";
const MAX_ENTRIES = 8;
const MAX_NAME = 24;
const MAX_MSG = 80;

async function getEntries(env) {
  const raw = await env.PROFILE_KV.get(KEY);
  return raw ? JSON.parse(raw) : [];
}

function stripHtml(s) {
  return s.replace(/<[^>]*>/g, "").replace(/[\r\n\t]+/g, " ").trim();
}

export async function handleGuestbook(request, env, path) {
  if (path === "/guestbook/wall.svg") {
    const entries = await getEntries(env);
    return new Response(renderWall(entries), { headers: svgHeaders() });
  }

  if (path === "/guestbook/sign" && request.method === "GET") {
    return new Response(signPage(), { headers: { "Content-Type": "text/html; charset=utf-8" } });
  }

  if (path === "/guestbook/submit" && request.method === "POST") {
    const form = await request.formData();
    let name = stripHtml(String(form.get("name") || "")).slice(0, MAX_NAME);
    let message = stripHtml(String(form.get("message") || "")).slice(0, MAX_MSG);

    if (!name) name = "anonymous";
    if (message) {
      const entries = await getEntries(env);
      entries.unshift({ name, message, ts: Date.now() });
      await env.PROFILE_KV.put(KEY, JSON.stringify(entries.slice(0, MAX_ENTRIES)));
    }

    return new Response(thanksPage(), { headers: { "Content-Type": "text/html; charset=utf-8" } });
  }

  return new Response("not found", { status: 404 });
}

function renderWall(entries) {
  const rowH = 26;
  const width = 600;
  const height = 40 + Math.max(entries.length, 1) * rowH;
  const rows = entries.length
    ? entries
        .map(
          (e, i) =>
            `<text class="mono" x="16" y="${40 + i * rowH}" font-size="12"><tspan fill="var(--accent)">${esc(e.name)}</tspan><tspan fill="var(--muted)"> — </tspan><tspan fill="var(--bone)">${esc(e.message)}</tspan></text>`
        )
        .join("\n")
    : `<text class="mono" x="16" y="40" font-size="12" fill="var(--muted)">no messages yet — be the first</text>`;

  return `<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Guestbook wall">
  <style>${THEME}</style>
  <line x1="16" y1="20" x2="${width - 16}" y2="20" stroke="var(--rule)"/>
  <text class="mono" x="16" y="14" font-size="10" fill="var(--muted)" letter-spacing="2">GUESTBOOK — LAST ${entries.length || 0}</text>
  ${rows}
</svg>`;
}

function signPage() {
  return `<!doctype html>
<html><head><meta charset="utf-8"><title>Sign the guestbook</title>
<style>body{font-family:ui-monospace,monospace;max-width:420px;margin:64px auto;color:#333}input,textarea{width:100%;padding:8px;margin:6px 0;font-family:inherit}button{padding:8px 16px;font-family:inherit;background:#000;color:#fff;border:0;cursor:pointer}</style>
</head><body>
<h2>Sign my guestbook</h2>
<form method="POST" action="/guestbook/submit">
<label>Name<input name="name" maxlength="${MAX_NAME}" required></label>
<label>Message<textarea name="message" maxlength="${MAX_MSG}" rows="3" required></textarea></label>
<button type="submit">Sign</button>
</form>
</body></html>`;
}

function thanksPage() {
  return `<!doctype html><html><head><meta charset="utf-8"><title>Thanks</title></head>
<body style="font-family:ui-monospace,monospace;max-width:420px;margin:96px auto;text-align:center">
<p>Thanks — refresh the profile to see it on the wall.</p>
<a href="https://github.com/Garvnanda">Back to profile</a>
</body></html>`;
}
