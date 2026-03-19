let lastCode = "";
function getCode() {
  const lines = document.querySelectorAll(".view-line");
  return Array.from(lines).map(function(l) { return l.innerText; }).join("\n");
}
function createPanel() {
  const existing = document.getElementById("bugfinder-panel");
  if (existing) existing.remove();
  const panel = document.createElement("div");
  panel.id = "bugfinder-panel";
  panel.style.position = "fixed";
  panel.style.bottom = "20px";
  panel.style.right = "20px";
  panel.style.background = "#1a1a2e";
  panel.style.color = "#ffffff";
  panel.style.padding = "16px";
  panel.style.borderRadius = "12px";
  panel.style.zIndex = "99999";
  panel.style.width = "340px";
  panel.style.fontFamily = "monospace";
  panel.style.fontSize = "13px";
  panel.style.border = "1px solid #0f3460";
  panel.style.boxShadow = "0 4px 24px rgba(0,0,0,0.6)";
  document.body.appendChild(panel);
  return panel;
}
function makeIssueHtml(icon, color, message, line) {
  var div = document.createElement("div");
  div.style.marginBottom = "10px";
  div.style.padding = "8px";
  div.style.background = "#16213e";
  div.style.borderRadius = "6px";
  div.style.borderLeft = "3px solid " + color;
  div.innerHTML = icon + " <span style=color:" + color + ">" + message + "</span>";
  if (line) {
    var lineDiv = document.createElement("div");
    lineDiv.style.color = "#888";
    lineDiv.style.fontSize = "11px";
    lineDiv.style.marginTop = "4px";
    lineDiv.innerText = "Line " + line;
    div.appendChild(lineDiv);
  }
  return div.outerHTML;
}
function showResults(data) {
  const panel = createPanel();
  var html = "<b style=color:#e94560>&#128269; BugFinder</b><hr style=border-color:#0f3460>";
  if (!data.has_issues) {
    html += "<span style=color:#4caf50>&#9989; No issues detected</span>";
  } else {
    data.static.forEach(function(issue) {
      var icon, color;
      if (issue.severity === "error") { icon = "&#128308;"; color = "#ff5252"; }
      else if (issue.severity === "warning") { icon = "&#128993;"; color = "#ffab40"; }
      else { icon = "&#128994;"; color = "#69f0ae"; }
      html += makeIssueHtml(icon, color, issue.message, issue.line);
    });
    if (data.ml.bug) {
      html += makeIssueHtml("&#129302;", "#ff5252", data.ml.type + " (" + Math.round(data.ml.confidence * 100) + "%)", null);
    }
  }
  panel.innerHTML = html;
}
function analyzeCode() {
  const code = getCode();
  if (code === lastCode || !code.trim()) return;
  lastCode = code;
  fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code })
  })
  .then(function(res) { return res.json(); })
  .then(function(data) { showResults(data); })
  .catch(function() {});
}
setInterval(analyzeCode, 3000);