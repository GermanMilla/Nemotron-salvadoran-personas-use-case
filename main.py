from datasets import load_dataset
import json

ds = load_dataset("nvidia/Nemotron-Personas-El-Salvador", split="train")

# Example: people with sports-related text mentioning running, gym, walking, or fútbol
keywords = ["correr", "gimnasio", "caminar", "fútbol", "futsal", "bicicleta", "trotar"]

def has_fitness_interest(row):
    text = (row.get("sports_persona") or "") + " " + (row.get("hobbies_and_interests") or "")
    text = text.lower()
    return any(k in text for k in keywords)

fitness_personas = ds.filter(has_fitness_interest)
persona = fitness_personas[0]

with open("persona_elsalvador.json", "w", encoding="utf-8") as f:
    json.dump(persona, f, ensure_ascii=False, indent=2)