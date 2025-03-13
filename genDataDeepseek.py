import json
import os
import requests

# Cấu hình API DeepSeek V3
API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = "sk-95ed2c2142f44a72a9796043b3278eaa"  # Thay thế bằng API key hợp lệ

system_prompt = """
You are a university student working in the field of computer science. 
You have been assigned to write the abstract section for a scientific paper based on the given paper title. 
Only output is given, no explanation of how to write, no citation of article link with the name given.
In the field of Information Technology (IT), the abstract of a scientific paper must meet several key requirements to ensure clarity, accuracy, and value for readers. Your task is to generate an abstract for this paper following the given guidelines:
1. Clear Structure
An abstract in IT typically follows a standard structure, including: 
- Objective/Purpose: A brief introduction to the problem or research question addressed. 
- Methods/Approach: Description of the approach, model, algorithm, or technology used. 
- Results/Findings: Summary of key findings, system performance, or comparisons with other methods. 
- Conclusion/Implications: Important insights, contributions of the research, and potential applications. 
2. Concise and Succinct
- The abstract is typically limited to 150-300 words (depending on the journal or conference requirements). 
- Avoid lengthy explanations or excessive theoretical background. 
3. Avoid Excessive Technical Jargon
- While IT is a technical field, the abstract should be clear and understandable, even for readers who are not deeply specialized in a specific subfield. 
- If abbreviations or technical terms are used, ensure they are widely recognized or briefly explained. 
4. No Citations or References
- The abstract should be self-contained and not rely on external references.
5. Emphasize Novelty and Contributions
- Highlight what makes the research unique compared to previous works.
- If the study involves AI, Machine Learning, 3D Reconstruction, or other advanced technologies, clearly state the innovations or improvements. 
6. Include Key Keywords
- Helps the paper be easily discoverable in scientific databases. 
Example: For research on large language models, relevant keywords might include GPT, transformer, fine-tuning, AI models. 
"""

def generate_text(prompt, problem_id):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat-v3",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        response_data = response.json()
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"Generation failed - Problem ID: {problem_id}, Error: {str(e)}")
        return ""

base_path = "your_base_path"  # Đường dẫn thư mục chứa file input/output
inputfile = os.path.join(base_path, "input.jsonl")  # Đặt tên file input
output_jsonl = os.path.join(base_path, "output.jsonl")  # Đặt tên file output

solution_id_counter = 1

with open(inputfile, 'r', encoding='utf-8') as file, open(output_jsonl, "a", encoding="utf-8") as output_file:
    for line in file:
        try:
            problem_data = json.loads(line)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON line: {line}")
            continue
        
        problem_id = problem_data.get("ID", "unknown")
        problem_title = problem_data.get("file_name", "")

        if not problem_title:
            print(f"Skipping problem ID {problem_id} due to missing title")
            continue

        prompt = f"Title of the paper: {problem_title}\n\nYour task is to generate an abstract for this paper following the given guidelines."

        generated_text = generate_text(prompt, problem_id)

        entry = {
            "solution_id": f"deepseek-v3-{solution_id_counter:04d}",
            "problem_id": problem_id,
            "content": generated_text if generated_text else "",
            "label": "AI",
            "label_detailed": "DeepSeek V3"
        }

        output_file.write(json.dumps(entry) + "\n")
        output_file.flush()

        print(f"✅ Processed record {solution_id_counter}: Problem ID {problem_id}")

        solution_id_counter += 1

print(f"Dataset saved to {output_jsonl}")
