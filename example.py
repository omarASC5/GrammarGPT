import torch
from transformers import AutoModelForCausalLM,AutoTokenizer

base_model = "FreedomIntelligence/phoenix-inst-chat-7b"
tokenizer = AutoTokenizer.from_pretrained(base_model, cache_dir="../cache")
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
    cache_dir="../cache",
)