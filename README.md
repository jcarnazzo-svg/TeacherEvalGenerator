 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..173939a2d0219298c789685c9e609a23b6065b86
--- /dev/null
+++ b/README.md
@@ -0,0 +1,59 @@
+# WUSD Teacher Evaluation App
+
+A lightweight web app for classroom observation write-ups and rubric-aligned scoring.
+
+## Features
+
+- Uses WUSD evaluation domains/elements from `rubricData.json`.
+- For each element:
+  - element title,
+  - score dropdown (`Unsatisfactory`, `Emerging`, `Proficient`, `Distinguished`),
+  - auto-filled rubric language textbox based on selected score,
+  - separate editable evidence/comments textbox.
+- Top-level observation information fields.
+- Summary sections:
+  - Summary of Lesson,
+  - Commendations,
+  - Recommendations.
+- Save/load functionality:
+  - Save/load via browser localStorage,
+  - Download/upload JSON files.
+- Print-friendly evaluation summary page.
+- Rubric language is fully separated from UI code in `rubricData.json`.
+
+## Setup
+
+### Option 1: Run with Python (recommended)
+
+```bash
+python -m http.server 8000
+```
+
+Then open:
+
+- `http://localhost:8000`
+
+### Option 2: Run with any static file server
+
+Serve this folder as static files and open `index.html` from the server URL.
+
+> Note: Use a server (not `file://`) so `fetch("rubricData.json")` works correctly in all browsers.
+
+## Customizing WUSD Rubric Content
+
+Edit `rubricData.json` to update:
+
+- observation fields,
+- summary fields,
+- domains,
+- elements,
+- rubric language for each rating level.
+
+No UI code changes are required when updating rubric wording.
+
+## Data Storage
+
+- **Save Evaluation** stores the current draft in browser localStorage.
+- **Load Saved Evaluation** restores the localStorage draft.
+- **Download JSON** exports the current draft.
+- **Load JSON** imports a previously exported draft.
 
EOF
)
