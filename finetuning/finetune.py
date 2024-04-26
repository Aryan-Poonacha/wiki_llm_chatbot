#help from https://medium.com/@anchen.li/fine-tune-llama-2-with-sft-and-dpo-8b57cf3ec69

from transformers import AutoModelForCausalLM, TrainingArguments
from datasets import load_dataset
from trl.sft import SFTTrainer

#Unused
#from trl.dpo import DPOTrainer

from trl.peft import get_peft_model, LoraConfig
from trl.bnb import BitsAndBytesConfig
from trl.utils import find_all_linear_names
import torch

output_dir = 'new_model'

# Load the custom dataset and prepare the formatting function for processing your training data
dataset = load_dataset("llmware/rag_instruct_benchmark_tester")

def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['query'])):
        text = f"### Input: ```{example['query'][i]}```\n ### Output: {example['answer'][i]}"
        output_texts.append(text)
    return output_texts

# Load the model in 4-bit quantization
model_name ="meta-llama/Meta-Llama-3-8B"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
base_model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, quantization_config=bnb_config)

# Create your peft lora configuration and get the peft model
peft_config = LoraConfig(
    r=128,
    lora_alpha=16,
    target_modules=find_all_linear_names(base_model),
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
base_model = get_peft_model(base_model, peft_config)

# Initiate the training argument and trainer
training_args = TrainingArguments(
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    gradient_checkpointing =True,
    max_grad_norm= 0.3,
    num_train_epochs=30, 
    learning_rate=2e-4,
    bf16=True,
    save_total_limit=3,
    logging_steps=10,
    output_dir=output_dir,
    optim="paged_adamw_32bit",
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
)

trainer = SFTTrainer(
    base_model,
    train_dataset=dataset,
    tokenizer=tokenizer,
    max_seq_length=2048,
    formatting_func=formatting_prompts_func,
    args=training_args
)
trainer.train() 
trainer.save_model(output_dir)
