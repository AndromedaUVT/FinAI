from google import genai
from google.genai import types
import json

client = genai.Client(api_key=r"AIzaSyB6mapxENniFGA-MJr6ByMIIk9c2SjRnDs")

def standardize_with_gemini(raw_text, prompt_injection):
    prompt = f"O sa primesti niste text extras din fisiere legat de finante, tu trebuie sa le extragi in JSON: Numar/cod factura, Nume firma care emite, Data emiterii, Total cu TVA si moneda folosita. In plus, ia in calcul precizarile ca: {prompt_injection}. TEXT: {raw_text}. Vei returna strict JSON!"

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json'
        )
    )
    return json.loads(response.text)
