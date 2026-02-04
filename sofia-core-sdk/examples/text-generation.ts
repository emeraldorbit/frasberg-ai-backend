import { createSofiaClient } from "../src";

async function main() {
  const client = createSofiaClient();

  const response = await client.generateText(
    "Explain the concept of resonance in simple terms."
  );

  console.log("Text Response:", response);
}

main();
