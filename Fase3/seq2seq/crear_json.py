import json
import random

# Define the new input-output pairs to augment
base_data_new = [
    {"input": "como te llamas", "output": "soy chatbot y tu"},
    {"input": "como te llamas", "output": "puedes llamarme chatbot"},
    {"input": "como te llamas", "output": "soy tu asistente virtual"},
    {"input": "quien eres", "output": "soy un chatbot diseñado para ayudarte"},
    {"input": "quien eres", "output": "soy un asistente virtual en que te ayudo"},
    {"input": "quien eres", "output": "me llaman chatbot estoy aqui para ti"},
    {"input": "puedo saber tu nombre", "output": "mi nombre es chatbot"},
    {"input": "puedo saber tu nombre", "output": "me llamo chatbot como te ayudo"},
    {"input": "puedo saber tu nombre", "output": "soy chatbot en que te puedo ayudar"},
]

# Function to create variants of a given sentence
def create_variants(input_text, output_text, num_variants=50):
    variants = []
    for _ in range(num_variants):
        output_variant = output_text
        # Random replacements for minor variation
        replacements = {
            "como te llamas": ["cual es tu nombre", "como te puedo llamar", "que nombre tienes"],
            "soy chatbot y tu": ["me llamo chatbot y tu", "soy chatbot cual es tu nombre", "puedes llamarme chatbot y tu"],
            "puedes llamarme chatbot": ["mi nombre es chatbot", "me llaman chatbot", "soy chatbot asi me puedes llamar"],
            "soy tu asistente virtual": ["soy un asistente virtual", "soy tu asistente digital", "soy un sistema diseñado para ayudarte"],
            "quien eres": ["quien soy", "puedes decirme quien eres", "como te describes"],
            "soy un chatbot diseñado para ayudarte": ["soy un asistente creado para ayudarte", "estoy diseñado para asistirte", "soy un chatbot a tu disposición"],
            "soy un asistente virtual en que te ayudo": ["soy un asistente virtual en que puedo ayudarte", "soy un asistente digital en que te ayudo", "puedo ayudarte como asistente virtual"],
            "me llaman chatbot estoy aqui para ti": ["me llaman chatbot estoy aqui para asistirte", "soy chatbot y estoy aqui para ayudarte", "me dicen chatbot en que te ayudo hoy"],
            "puedo saber tu nombre": ["me puedes decir tu nombre", "cual es tu nombre", "como te llamas tu"],
            "mi nombre es chatbot": ["soy chatbot", "mi nombre es chatbot y el tuyo", "me llaman chatbot cual es el tuyo"],
            "me llamo chatbot como te ayudo": ["soy chatbot en que te puedo ayudar", "soy chatbot que necesitas", "me llamo chatbot que puedo hacer por ti"],
            "soy chatbot en que te puedo ayudar": ["soy chatbot que necesitas saber", "soy chatbot en que te ayudo hoy", "soy chatbot que preguntas tienes"],
        }
        for key, values in replacements.items():
            if key in output_variant:
                output_variant = output_variant.replace(key, random.choice(values), 1)
        variants.append({"input": input_text, "output": output_variant})
    return variants

# Generate 43 variants for each base pair
augmented_data_new = []
for item in base_data_new:
    augmented_data_new.extend(create_variants(item["input"], item["output"], num_variants=43))

# Save to a JSON file in the current directory
output_path_new = "./augmented_greetings_names.json"
with open(output_path_new, "w") as f:
    json.dump(augmented_data_new, f, ensure_ascii=False, indent=2)

output_path_new
