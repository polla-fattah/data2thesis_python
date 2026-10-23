// Runs before each render of the website (Quarto runs .ts files with its
// built-in Deno, so no R or Python is needed). Copies the case-study data and
// the data package from data/ into the site, so readers can download them and
// the playground can load them. The originals stay in data/.

const repo = ".";

function copy(from: string, to: string) {
  Deno.copyFileSync(from, to);
}

// Playground pages read the data from their own folder, exactly as the
// downloadable chapter projects do: pd.read_csv("students.csv")
Deno.mkdirSync("content/playground", { recursive: true });
for (const file of ["students.csv", "semesters.csv", "questionnaire.csv", "supervisors.csv",
                     "counselling_visits.csv", "open_responses.csv", "open_responses_coded.csv"]) {
  copy(`${repo}/data/${file}`, `content/playground/${file}`);
}
// The language model's saved coding (Chapter 18)
copy(`${repo}/data-raw/ai_coding_results.csv`, "content/playground/ai_coding_results.csv");

