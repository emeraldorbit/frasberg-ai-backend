import type { SofiaSystemConfig } from './types';

export function loadSofiaConfig(): SofiaSystemConfig {
  const required = (name: string): string => {
    const value = process.env[name];
    if (!value) {
      throw new Error(`Missing required environment variable: ${name}`);
    }
    return value;
  };

  return {
    ai: {
      provider: 'sofia-core',
      apiKeySource: required('AI_API_KEY_SOURCE') as 'github' | 'supabase',
      allowExternalProviders: false,
      fallbackProviders: []
    },
    imageGeneration: {
      provider: 'sofia-core',
      apiKeySource: required('IMAGE_API_KEY_SOURCE') as 'github' | 'supabase',
      allowExternalProviders: false,
      fallbackProviders: []
    },
    videoGeneration: {
      provider: 'sofia-core',
      apiKeySource: required('VIDEO_API_KEY_SOURCE') as 'github' | 'supabase',
      allowExternalProviders: false,
      fallbackProviders: []
    },
    disabledProviders: [
      'openai',
      'anthropic',
      'google-gemini',
      'stability-ai',
      'emergent-llm'
    ]
  };
}
