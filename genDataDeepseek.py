import os
import json
import logging
from openai import OpenAI

# Cấu hình API DeepSeek
deepseek_api_key = "sk-95ed2c2142f44a72a9796043b3278eaa"
base_url = "https://api.deepseek.com"
model_name = "deepseek-chat"

# Định nghĩa function gọi DeepSeek API
def get_deepseek_response(system_prompt, user_prompt, retries=2, timeout=60):
    client = OpenAI(api_key=deepseek_api_key, base_url=base_url)
    
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=False,
                timeout=timeout
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"[get_deepseek_response] Attempt {attempt+1}/{retries} failed: {e}")
    
    return ""  # Nếu thất bại, trả về nội dung rỗng

# Định nghĩa đường dẫn file
input_file = "/Users/trannguyenmyanh/Documents/HUST/AUTH SCAN/authscan/data/generated/arxiv_abstract/data/test1.jsonl"
output_file_path = "/Users/trannguyenmyanh/Documents/HUST/AUTH SCAN/authscan/data/generated/arxiv_abstract/data/test3.jsonl"

# Đọc dữ liệu đầu vào và xử lý từng record
solution_id_counter = 1

with open(input_file, 'r', encoding='utf-8') as file, open(output_file_path, "a", encoding="utf-8") as outfile:
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

        # Tạo prompt cho mô hình
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
        user_prompt = f"Your task is to generate an abstract for this paper following the given guidelines.\n\nTitle: {problem_title}"

        # Gọi DeepSeek API để sinh nội dung
        content = get_deepseek_response(system_prompt, user_prompt)

        # Tạo record kết quả
        output_record = {
            "solution_id": f"deepseek-{solution_id_counter:04d}",
            "problem_id": problem_id,
            "content": content,
            "label": "AI",
            "label_detailed": "DeepSeek"
        }

        # Ghi ngay vào file JSONL
        outfile.write(json.dumps(output_record, ensure_ascii=False) + "\n")
        outfile.flush()  

        print(f"✅ Processed record {solution_id_counter}: Problem ID {problem_id}")

        solution_id_counter += 1

print(f"✅ Dataset saved to {output_file_path}")


print(f"✅ Dataset saved to {output_file}")
