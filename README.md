# El Salvador Synthetic Persona Example

A small Python project for extracting fitness product requirements from synthetic El Salvadoran persona data.

## Files

- `analyze_personas.py` - Builds a synthetic persona sample from the `nvidia/Nemotron-Personas-El-Salvador` dataset and saves it as `persona_elsalvador.json`.
- `main.py` - Loads the saved persona and sends it to a local Llama-compatible chat completion endpoint for product analysis.
- `persona_elsalvador.json` - Example synthetic persona selected from the dataset.
- `persona_analysis.json` - Output file for the product analysis results.

## Usage

1. Install required packages:
   ```powershell
   pip install datasets requests
   ```

2. Create a sample persona:
   ```powershell
   python analyze_personas.py
   ```

3. Run the analysis flow:
   ```powershell
   python main.py
   ```

## Notes

- `main.py` expects a local Llama-compatible server at `http://127.0.0.1:8080/v1/chat/completions`, but you can quickly modify to support any endpoint.
- The prompt is designed to generate structured JSON product insights for a fitness app targeting Salvadoran personas.
- Update the endpoint or model configuration in `main.py` as needed for your local setup.
