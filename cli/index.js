#!/usr/bin/env node

/**
 * Sofia Core CLI
 * Command-line interface for Sofia Core API
 */

const https = require('https');
const http = require('http');

const SOFIA_URL = process.env.SOFIA_URL || 'https://sdtilgpppwhwtbxlbmik.supabase.co/functions/v1/sofia-core-backend';
const SOFIA_API_KEY = process.env.SOFIA_API_KEY;

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    message: '',
    stream: false,
    temperature: 0.7,
    sovereign: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--stream' || arg === '-s') {
      options.stream = true;
    } else if (arg === '--temperature' || arg === '-t') {
      options.temperature = parseFloat(args[++i] || 0.7);
    } else if (arg === '--sovereign') {
      options.sovereign = true;
    } else if (arg === '--help' || arg === '-h') {
      showHelp();
      process.exit(0);
    } else {
      options.message += (options.message ? ' ' : '') + arg;
    }
  }

  return options;
}

function showHelp() {
  console.log(`
Sofia Core CLI

Usage: npx sofia [options] <message>

Options:
  -s, --stream           Stream the response
  -t, --temperature <n>  Set temperature (0-2, default: 0.7)
  --sovereign            Enable sovereign mode
  -h, --help             Show this help message

Environment Variables:
  SOFIA_URL              Base URL for Sofia API
  SOFIA_API_KEY          API key for authentication

Examples:
  npx sofia "Hello Sofia"
  npx sofia --stream "Tell me a story"
  npx sofia --sovereign "What is your purpose?"
  npx sofia -t 0.9 "Be creative"
`);
}

function makeRequest(url, options, data) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const protocol = urlObj.protocol === 'https:' ? https : http;
    
    const reqOptions = {
      hostname: urlObj.hostname,
      port: urlObj.port,
      path: urlObj.pathname + urlObj.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${options.apiKey}`,
        'Content-Length': Buffer.byteLength(data)
      }
    };

    const req = protocol.request(reqOptions, (res) => {
      if (options.stream) {
        res.setEncoding('utf8');
        res.on('data', (chunk) => {
          const lines = chunk.split('\n');
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                console.log();
                return;
              }
              try {
                const json = JSON.parse(data);
                const content = json.choices[0]?.delta?.content;
                if (content) {
                  process.stdout.write(content);
                }
              } catch (e) {
                // Ignore parse errors
              }
            }
          }
        });
        res.on('end', () => resolve());
      } else {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(body);
            if (res.statusCode >= 400) {
              reject(new Error(json.error || `HTTP ${res.statusCode}`));
            } else {
              resolve(json);
            }
          } catch (e) {
            reject(new Error('Failed to parse response'));
          }
        });
      }
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  const options = parseArgs();

  if (!options.message) {
    console.error('Error: No message provided');
    showHelp();
    process.exit(1);
  }

  if (!SOFIA_API_KEY) {
    console.error('Error: SOFIA_API_KEY environment variable not set');
    process.exit(1);
  }

  const payload = {
    model: 'sofia-core',
    messages: [
      { role: 'user', content: options.message }
    ],
    temperature: options.temperature,
    stream: options.stream
  };

  if (options.sovereign) {
    payload.sofia_identity = {
      mode: 'sovereign',
      tone: 'ceremonial',
      vector: 'auto'
    };
    payload.sofia_directives = {
      sovereignty: true
    };
  }

  try {
    const result = await makeRequest(
      `${SOFIA_URL}/v1/chat/completions`,
      { apiKey: SOFIA_API_KEY, stream: options.stream },
      JSON.stringify(payload)
    );

    if (!options.stream) {
      console.log(result.choices[0].message.content);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
