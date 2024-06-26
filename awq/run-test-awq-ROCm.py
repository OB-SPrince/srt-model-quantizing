from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer, TextStreamer

#model_path = "TheBloke/Mixtral-8x7B-Instruct-v0.1-AWQ"
model_path = "kaist-ai/mistral-orpo-capybara-7k"

# Load model
model = AutoAWQForCausalLM.from_quantized(model_path, fuse_layers=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

# Convert prompt to tokens
prompt_template = """\
<|system|>
</s>
<|user|>
{prompt}</s>
<|assistant|>"""

prompt = "You're standing on the surface of the Earth. "\
        "You walk one mile south, one mile west and one mile north. "\
        "You end up exactly where you started. Where are you?"

tokens = tokenizer(
    prompt_template.format(prompt=prompt), 
    return_tensors='pt'
).input_ids.cuda()

# Generate output
generation_output = model.generate(
    tokens, 
    streamer=streamer,
    max_seq_len=512
)
