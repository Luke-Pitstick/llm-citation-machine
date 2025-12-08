// Example Ollama client for local models (uncomment to use)
client<llm> CustomOllama {
  provider openai-generic
  options {
    base_url "http://localhost:11434/v1"
    model "llama3.2"
    default_role "user"
  }
}

client<llm> CustomGemma{
  provider openai-generic
  options {
    base_url "http://localhost:11434/v1"
    model "gemma3:4b"
    default_role "user"
  }
}

client<llm> OpenAIClient {
  provider "openai-responses"
  options {
    api_key env.OPENAI_API_KEY
    model "gpt-5-mini"
    temperature 1
    tools [
      {
        type "web_search"
      }
    ]
  }
}

client<llm> CustomGemini {
  provider google-ai
  options {
    model "gemini-2.5-flash"
    api_key env.GOOGLE_API_KEY
    default_role "user"
  }
}