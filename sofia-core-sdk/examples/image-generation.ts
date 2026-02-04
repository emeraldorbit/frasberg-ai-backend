import { createSofiaClient } from "../src";

async function main() {
  const client = createSofiaClient();

  const result = await client.generateImage(
    "A serene landscape with mountains at sunrise."
  );

  console.log("Image Result:", result);
}

main().catch(console.error);
