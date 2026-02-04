import { createSofiaClient } from "../src";

async function main() {
  const client = createSofiaClient();

  const result = await client.generateVideo(
    "A slow pan across a futuristic city skyline."
  );

  console.log("Video Result:", result);
}

main();
