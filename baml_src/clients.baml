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


