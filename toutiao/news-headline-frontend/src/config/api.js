export const apiConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  apiEndpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  // Configure this only in a local .env file; never commit an API key to the frontend.
  apiKey: import.meta.env.VITE_DASHSCOPE_API_KEY || '',
  model: import.meta.env.VITE_DASHSCOPE_MODEL || 'qwen3-max-preview',
}
