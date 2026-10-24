// Runs before each render of the website (Quarto runs .ts files with its
// built-in Deno, so no R or Python is needed). Copies all dataset files from data/
// into content/playground/, so readers can download them and the interactive
// Pyodide playground pages can load them seamlessly.

const repo = ".";

function copy(from: string, to: string) {
  Deno.copyFileSync(from, to);
}

Deno.mkdirSync("content/playground", { recursive: true });

// Copy all CSV datasets from data/ into content/playground/
for (const entry of Deno.readDirSync(`${repo}/data`)) {
  if (entry.isFile && entry.name.endsWith(".csv")) {
    copy(`${repo}/data/${entry.name}`, `content/playground/${entry.name}`);
  }
}

// The language model's saved coding (Chapter 18)
const aiCoding = `${repo}/data-raw/ai_coding_results.csv`;
try {
  if (Deno.statSync(aiCoding).isFile) {
    copy(aiCoding, "content/playground/ai_coding_results.csv");
  }
} catch {
  // Ignore if not present
}
