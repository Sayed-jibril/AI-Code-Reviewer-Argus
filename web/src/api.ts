export interface Issue {
  id: string;
  ruleId: string;
  title: string;
  severity: string;
  filePath: string;
  lineStart: number;
  lineEnd: number;
  confidence: number;
  tags: string[];
  explanation?: string;
  suggestion?: string;
  codeFrame?: string;
}

export interface TestSuggestion {
  title: string;
  description: string;
  filePath: string;
  rationale: string;
  content: string;
}

export interface ReviewMetrics {
  files: number;
  functions: number;
  avgComplexity: number;
}

export interface ReviewResult {
  issues: Issue[];
  tests: TestSuggestion[];
  metrics: ReviewMetrics;
}

export async function reviewFiles(files: File[]): Promise<ReviewResult> {
  const form = new FormData();
  files.forEach(f => form.append("files", f, f.name));
  const res = await fetch("/api/review", { method: "POST", body: form });
  if (!res.ok) throw new Error("Review failed");
  return await res.json();
}
