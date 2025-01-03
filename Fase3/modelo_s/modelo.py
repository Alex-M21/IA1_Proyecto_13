from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset

# Cargar modelo y tokenizer
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(model_name)
model.resize_token_embeddings(len(tokenizer))

# Cargar dataset
dataset = load_dataset("json", data_files={"train": "train.json", "validation": "validation.json"})

# Preprocesar datos
def preprocess_data(example):
    inputs = tokenizer(
        example["query"],
        truncation=True,
        padding="max_length",
        max_length=128
    )
    outputs = tokenizer(
        example["response"],
        truncation=True,
        padding="max_length",
        max_length=128
    )
    return {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"],
        "labels": outputs["input_ids"]
    }

tokenized_dataset = dataset.map(preprocess_data, batched=True).filter(lambda x: x is not None)

# Configuración de entrenamiento
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    save_steps=10_000,
    save_total_limit=2,
    remove_unused_columns=True,
    logging_dir='./logs',
)

# Forzar padding y truncación en el Trainer
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  # No usar enmascarado si es un modelo causal
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Entrenar modelo
trainer.train()

# Guardar modelo
trainer.save_model("./trained_model")
