/* app.js — shared utilities */

/**
 * Fetch wrapper: POSTs or GETs JSON, returns parsed response or throws {message}.
 */
async function apiRequest(method, url, body) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body !== undefined) {
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(url, opts);
  const data = await res.json();
  if (!res.ok) {
    throw { message: data.detail || `HTTP ${res.status}` };
  }
  return data;
}

async function apiGet(url)        { return apiRequest("GET",  url); }
async function apiPost(url, body) { return apiRequest("POST", url, body); }

/**
 * Map badge state → CSS colour class suffix.
 */
function badgeColorClass(color) {
  const map = { green: "green", yellow: "yellow", orange: "orange", red: "red" };
  return "badge-" + (map[color] || "red");
}

/**
 * Map badge color to sidebar-specific CSS class.
 */
function badgeSidebarClass(color) {
  return "badge-sidebar badge-sidebar-" + (color || "red");
}

/**
 * Format a number to at most `decimals` significant decimal places.
 * Returns "n/a" for null/undefined.
 */
function fmt(value, decimals = 3) {
  if (value === null || value === undefined) return "n/a";
  return Number(value).toFixed(decimals);
}

/**
 * Format a recovery percentage with one decimal, or return "n/a".
 */
function fmtPct(value) {
  if (value === null || value === undefined) return "n/a";
  return Number(value).toFixed(1) + "%";
}
