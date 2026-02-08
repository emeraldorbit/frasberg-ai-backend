// llm/brain.js
import fetch from "node-fetch";

export async function runLLM(transcript) {
  console.log("Sending transcript to LLM:", transcript);

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.LLM_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-5.2",
        messages: [
          { role: "system", content: "You are Sofia, a warm, human-like conversational AI." },
          { role: "user", content: transcript }
        ]
      })
    });

    if (!response.ok) {
      throw new Error(`LLM request failed: ${response.statusText}`);
    }

    const result = await response.json();
    const reply = result.choices[0].message.content;

    console.log("LLM reply:", reply);
    return reply;
  } catch (err) {
    console.error("LLM error:", err);
    return "Sorry, I had trouble generating a response.";
  }
}

export async function generateSessionSummaryWithTags(events) {
  console.log("Generating session summary with tags...");

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.LLM_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-5.2",
        messages: [
          { role: "system", content: "You are Sofia, a conversational AI. Summarize the session clearly and warmly, and also provide 2–5 tags that describe the conversation (e.g., greeting, question, farewell, small talk)." },
          { role: "user", content: `Here are the session events:\n${JSON.stringify(events, null, 2)}` }
        ]
      })
    });

    if (!response.ok) {
      throw new Error(`LLM summary request failed: ${response.statusText}`);
    }

    const result = await response.json();
    const reply = result.choices[0].message.content;

    // Expecting output like:
    // "Summary: ...\nTags: tag1, tag2"
    const [summaryLine, tagsLine] = reply.split("\n").map(line => line.trim());

    return {
      summary: summaryLine ? summaryLine.replace(/^Summary:\s*/i, "") : reply,
      tags: tagsLine ? tagsLine.replace(/^Tags:\s*/i, "").split(",").map(t => t.trim()) : []
    };
  } catch (err) {
    console.error("Summary error:", err);
    return { summary: "Summary unavailable due to error.", tags: [] };
  }
}

