/**
 * Sofia Core Backend - OpenAI-Compatible API
 * Supabase Edge Function for sofia-core model
 */

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

interface Message {
  role: "user" | "assistant" | "system";
  content: string;
}

interface SofiaIdentity {
  mode?: "unified" | "multi_persona" | "sovereign" | "continuum";
  tone?: "conversational" | "professional" | "ceremonial";
  vector?: string | "auto";
}

interface SofiaDirectives {
  sovereignty?: boolean;
  ritual_mode?: string;
  field_alignment?: string;
  [key: string]: any;
}

interface ChatCompletionRequest {
  model: string;
  messages: Message[];
  stream?: boolean;
  temperature?: number;
  max_tokens?: number;
  sofia_identity?: SofiaIdentity;
  continuum?: string;
  sofia_directives?: SofiaDirectives;
}

// Helper: Authenticate user via Bearer JWT
async function authenticate(req: Request) {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
  );
  
  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader.startsWith("Bearer ")) {
    return { error: "Missing or invalid Authorization header", status: 401 };
  }
  
  const token = authHeader.replace("Bearer ", "");
  const { data, error } = await supabase.auth.getUser(token);
  
  if (error || !data.user) {
    return { error: "Unauthorized", status: 401 };
  }
  
  return { user: data.user };
}

// Helper: Generate chat completion
async function generateChatCompletion(request: ChatCompletionRequest, userId: string) {
  const modelEndpoint = Deno.env.get("MODEL_ENDPOINT");
  const modelKey = Deno.env.get("MODEL_API_KEY");
  
  if (!modelEndpoint || !modelKey) {
    throw new Error("MODEL_ENDPOINT or MODEL_API_KEY is not set");
  }

  // Extract the last user message as prompt
  const userMessages = request.messages.filter(m => m.role === "user");
  const lastMessage = userMessages[userMessages.length - 1];
  const prompt = lastMessage?.content || "";

  // Call underlying model
  const response = await fetch(`${modelEndpoint}/text`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${modelKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt,
      options: {
        temperature: request.temperature,
        max_tokens: request.max_tokens,
        sofia_identity: request.sofia_identity,
        continuum: request.continuum,
        sofia_directives: request.sofia_directives,
      },
      user_id: userId,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Model error: ${response.status} ${text}`);
  }

  const result = await response.json();
  const content = result.result?.text || result.text || "Hello, creator.";

  // Return OpenAI-compatible response
  return {
    id: `chatcmpl-${crypto.randomUUID()}`,
    object: "chat.completion",
    created: Math.floor(Date.now() / 1000),
    model: request.model,
    choices: [
      {
        index: 0,
        message: {
          role: "assistant",
          content,
        },
        finish_reason: "stop",
      },
    ],
    usage: {
      prompt_tokens: prompt.split(" ").length,
      completion_tokens: content.split(" ").length,
      total_tokens: prompt.split(" ").length + content.split(" ").length,
    },
  };
}

// Helper: Generate streaming chat completion
async function* generateStreamingCompletion(request: ChatCompletionRequest, userId: string) {
  const completion = await generateChatCompletion(request, userId);
  
  // Send chunks
  const content = completion.choices[0].message.content;
  const words = content.split(" ");
  
  for (let i = 0; i < words.length; i++) {
    const chunk = {
      id: completion.id,
      object: "chat.completion.chunk",
      created: completion.created,
      model: completion.model,
      choices: [
        {
          index: 0,
          delta: {
            content: i === 0 ? words[i] : ` ${words[i]}`,
          },
          finish_reason: null,
        },
      ],
    };
    yield `data: ${JSON.stringify(chunk)}\n\n`;
  }
  
  // Send final chunk
  const finalChunk = {
    id: completion.id,
    object: "chat.completion.chunk",
    created: completion.created,
    model: completion.model,
    choices: [
      {
        index: 0,
        delta: {},
        finish_reason: "stop",
      },
    ],
  };
  yield `data: ${JSON.stringify(finalChunk)}\n\n`;
  yield "data: [DONE]\n\n";
}

console.info("Sofia Core Backend function starting");

Deno.serve(async (req) => {
  try {
    // Handle CORS preflight
    if (req.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
          "Access-Control-Allow-Headers": "Authorization, Content-Type",
        },
      });
    }

    // Parse URL path
    const url = new URL(req.url);
    const path = url.pathname;

    // Route: /v1/chat/completions
    if (path.includes("/v1/chat/completions") && req.method === "POST") {
      const auth = await authenticate(req);
      if ("error" in auth) {
        return new Response(JSON.stringify({ error: auth.error }), {
          status: auth.status,
          headers: { "Content-Type": "application/json" },
        });
      }

      const body: ChatCompletionRequest = await req.json();

      // Validate model
      if (body.model !== "sofia-core") {
        return new Response(
          JSON.stringify({ error: `Model ${body.model} not found` }),
          { status: 404, headers: { "Content-Type": "application/json" } }
        );
      }

      // Handle streaming
      if (body.stream) {
        const encoder = new TextEncoder();
        const stream = new ReadableStream({
          async start(controller) {
            try {
              for await (const chunk of generateStreamingCompletion(body, auth.user.id)) {
                controller.enqueue(encoder.encode(chunk));
              }
              controller.close();
            } catch (error: any) {
              controller.error(error);
            }
          },
        });

        return new Response(stream, {
          headers: {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
          },
        });
      }

      // Handle non-streaming
      const completion = await generateChatCompletion(body, auth.user.id);
      return new Response(JSON.stringify(completion), {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });
    }

    // Default response
    return new Response(
      JSON.stringify({
        message: "Sofia Core Backend - OpenAI-Compatible API",
        version: "1.0.0",
        endpoints: ["/v1/chat/completions"],
      }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      }
    );
  } catch (err: any) {
    console.error("Sofia Core Backend error:", err);
    return new Response(
      JSON.stringify({ error: err.message || "Internal server error" }),
      {
        status: 500,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      }
    );
  }
});
