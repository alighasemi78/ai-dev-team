import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


class LLMEngine:
    def __init__(self, model_id="Qwen/Qwen2.5-Coder-7B-Instruct"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"--- INITIALIZING ENGINE ON: {self.device.upper()} ---")

        # 1. Config for 4-bit loading (Only works on GPU)
        if self.device == "cuda":
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_type=torch.float16,
            )
        else:
            bnb_config = None
            print(
                "Warning: Running on CPU. 4-bit quantization disabled. This will be slow."
            )

        # 2. Load tokenizer
        print(f"Loading Tokenizer for {model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        # 3. Load model
        print(f"Loading Model Weights (This may take a while first time)...")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=bnb_config,
                device_map="auto" if self.device == "cuda" else None,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            )
            print("Model loaded successfully.")
        except Exception as e:
            print(f"CRITICAL ERROR LOADING MODEL: {e}")
            raise e

    def generate(self, messages, max_new_tokens=1024):
        # Format the prompt using the model's specific template
        text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        # Tokenize and move to GPU
        inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        # Generate
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.7,
                do_sample=True,
            )

        # Decode (Slice off the prompt tokens to get just the response)
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[
            0
        ]
        return response
