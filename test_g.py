import google.generativeai as genai
from tqdm import tqdm
import glob

genai.configure(api_key="AIzaSyDbh0mLOlOMwOb5ft9i63ol7KZIg4iBXGQ")

model = genai.GenerativeModel('gemini-1.5-flash-002')

with open('model_solution.py', 'r') as f:
    model_solution = f.read()

with open('question_paper.md', 'r') as f:
    question_paper = f.read()

with open('rubric_updated.md', 'r') as f:
    rubric = f.read()

with open('evaluation_prompt_v0.txt', 'r') as f:
    evaluation_prompt = f.read()

sol_path = r'D:\llm_exam\11601001325_CS F441_AUG_2024-Mid-sem exam submission-42941'

sol_paths = glob.glob(sol_path + r"\*assignsubmission_file_\*.*py*", recursive=True)

for solution_path in tqdm(sol_paths):
    with open(solution_path, 'r', encoding='utf-8', errors='ignore') as f:
        try:
            student_solution = f.read()
        except:
            pass

    prompt = evaluation_prompt.format(
        question_paper=question_paper,
        model_solution=model_solution,
        rubric=rubric,
        student_solution=student_solution
    )

    result = model.generate_content(["CONTEXT\n\n", prompt])
 
    output_path = './evaluation_reports_g/' + '_'.join(solution_path.split('\\')[-2].split('_')[:2]) + '_report.md'
    
    with open(output_path, 'w') as f:
        f.write(result.text)