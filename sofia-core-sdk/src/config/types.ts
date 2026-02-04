export interface SofiaSystemConfig {
  ai: {
    provider: 'sofia-core';
    apiKeySource: 'github' | 'supabase';
    allowExternalProviders: false;
    fallbackProviders: [];
  };
  imageGeneration: {
    provider: 'sofia-core';
    apiKeySource: 'github' | 'supabase';
    allowExternalProviders: false;
    fallbackProviders: [];
  };
  videoGeneration: {
    provider: 'sofia-core';
    apiKeySource: 'github' | 'supabase';
    allowExternalProviders: false;
    fallbackProviders: [];
  };
  disabledProviders: Array<
    'openai' | 'anthropic' | 'google-gemini' | 'stability-ai' | 'emergent-llm'
  >;
}
