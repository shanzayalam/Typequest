const API_BASE = "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export function startQuiz() {
  return request("/api/quiz/start");
}

export function adaptQuiz(answers) {
  return request("/api/quiz/adapt", {
    method: "POST",
    body: JSON.stringify({ answers })
  });
}

export function getResult(answers) {
  return request("/api/quiz/result", {
    method: "POST",
    body: JSON.stringify({ answers })
  });
}
