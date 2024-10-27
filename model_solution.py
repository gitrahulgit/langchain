import os
from typing import TypedDict, Dict
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langchain_core.tools import tool
from langchain_core.language_models import BaseLLM
from langchain_google_genai import ChatGoogleGenerativeAI
import re

GOOGLE_API_KEY = "AIzaSyDbh0mLOlOMwOb5ft9i63ol7KZIg4iBXGQ"

# Function to read file content
def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        # Removing unnecessary whitespace and empty lines
        return "\n".join([line.strip() for line in file if line.strip()])


# Custom tool for summing marks
@tool
def sum_marks(marks: str) -> float:
    """Sums a comma-separated list of marks"""
    total = 0.0
    for mark in marks.split(','):
        mark = mark.strip()
        if mark:  # This will skip empty strings
            try:
                total += float(mark)
            except ValueError:
                print(f"Warning: Invalid mark found: '{mark}'")
    return total


# State class for managing workflow state
class EvaluationState(TypedDict):
    problem_description: str
    model_solution: str
    rubric: str
    student_code: str
    extracted_classes: Dict[str, str]
    extracted_rubrics: Dict[str, str]
    initial_evaluations: Dict[str, str]
    final_evaluations: Dict[str, str]
    extracted_marks: Dict[str, str]
    total_marks: float


# LangGraph nodes
def class_extraction(state: EvaluationState, llm: BaseLLM) -> EvaluationState:
    prompt = "Extract individual Java classes from the following code:\n\n{code}\n\nFor each class, provide the class name and its code."
    
    # Extract classes from student code
    result = llm.invoke(prompt.format(code=state['student_code']))
    classes = parse_extracted_classes(result.content)
    state['extracted_classes'] = classes
    
    return state


def rubric_extraction(state: EvaluationState, llm: BaseLLM) -> EvaluationState:
    prompt = "Given the following rubric:\n\n{rubric}\n\nExtract the relevant rubric details for the Java class named {class_name}."
    
    for class_name in state['extracted_classes'].keys():
        result = llm.invoke(prompt.format(rubric=state['rubric'], class_name=class_name))
        state['extracted_rubrics'][class_name] = result.content
    
    return state


def initial_evaluation(state: EvaluationState, llm: BaseLLM) -> EvaluationState:
    prompt = (
        "Evaluate the following student code based on the rubric and model solution:\n\n"
        "Student Code:\n{student_code}\n\nModel Solution:\n{model_solution}\n\n"
        "Rubric:\n{rubric}\n\nProvide a detailed evaluation including scores for each criterion, "
        "comments on correctness, errors, and suggestions for improvement."
    )
    
    for class_name, class_code in state['extracted_classes'].items():
        result = llm.invoke(
            prompt.format(
                student_code=class_code,
                model_solution=state['model_solution'],
                rubric=state['extracted_rubrics'].get(class_name, "")
            )
        )
        state['initial_evaluations'][class_name] = result.content
    
    return state


def review_evaluation(state: EvaluationState, llm: BaseLLM) -> EvaluationState:
    prompt = (
        "Review and correct if necessary the following evaluation:\n\n{initial_evaluation}\n\n"
        "Provide a final assessment ensuring all evaluations are accurate and complete."
    )
    
    for class_name, initial_eval in state['initial_evaluations'].items():
        result = llm.invoke(prompt.format(initial_evaluation=initial_eval))
        state['final_evaluations'][class_name] = result.content
    
    return state


def marks_extraction(state: EvaluationState, llm: BaseLLM) -> EvaluationState:
    prompt = "From the following evaluation, extract a comma-separated list of marks awarded for each criterion:\n\n{evaluation}"
    
    for class_name, evaluation in state['final_evaluations'].items():
        result = llm.invoke(prompt.format(evaluation=evaluation))
        # Use regex to extract only valid numeric values
        numeric_marks =  re.findall(r'([\d]+)', result.content)
        
        # Filter out any empty or malformed values
        if numeric_marks:
            state['extracted_marks'][class_name] = ",".join(numeric_marks)
        else:
            state['extracted_marks'][class_name] = "0"
    
    return state


def total_marks_calculation(state: EvaluationState) -> EvaluationState:
    all_marks = ",".join(state['extracted_marks'].values())
    state['total_marks'] = sum_marks.invoke(all_marks)
    return state


def save_final_evaluation(state: EvaluationState):
    with open('final_evaluations.txt', 'w') as f:
        for class_name, evaluation in state['final_evaluations'].items():
            f.write(f"Evaluation for {class_name}:\n")
            f.write(evaluation)
            f.write("\n\n")
        f.write(f"Total Marks: {state['total_marks']}\n")


# Helper function to parse extracted classes
def parse_extracted_classes(extraction_result: str) -> Dict[str, str]:
    """Helper function to parse the extracted classes from LLM output."""
    classes = {}
    current_class = ""
    current_code = []
    
    for line in extraction_result.splitlines():
        if len(line.strip().split()) > 1 and line.strip().split()[1] == 'class':
            if current_class:
                classes[current_class] = "\n".join(current_code)
            current_class = line.split()[1].split('(')[0].split('{')[0]
            current_code = [line]
        elif current_class:
            current_code.append(line)
    
    if current_class:
        classes[current_class] = "\n".join(current_code)
    
    return classes

# Main application
def main():
    # Initialize LLM with hardcoded API key
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=GOOGLE_API_KEY)

    # Initialize state
    initial_state = EvaluationState(
        problem_description=read_file("D:\\llm_exam\\input_2\\problem_description.txt"),
        model_solution=read_file("D:\\llm_exam\\input_2\\model_solution.java"),
        rubric=read_file("D:\\llm_exam\\input_2\\rubric.txt"),
        marking_scheme=read_file("D:\\llm_exam\\input_2\\rubric.txt"),
        student_code=read_file("D:\\llm_exam\\input_2\\student_solution.java"),
        extracted_classes={},
        extracted_rubrics={},
        initial_evaluations={},
        final_evaluations={},
        extracted_marks={},
        total_marks=0.0
    )

    # Create StateGraph
    workflow = StateGraph(EvaluationState)

    # Add nodes
    workflow.add_node("class_extraction", lambda x: class_extraction(x, llm))
    workflow.add_node("rubric_extraction", lambda x: rubric_extraction(x, llm))
    workflow.add_node("initial_evaluation", lambda x: initial_evaluation(x, llm))
    workflow.add_node("review_evaluation", lambda x: review_evaluation(x, llm))
    workflow.add_node("marks_extraction", lambda x: marks_extraction(x, llm))
    workflow.add_node("total_marks_calculation", total_marks_calculation)

    # Add edges
    workflow.add_edge("class_extraction", "rubric_extraction")
    workflow.add_edge("rubric_extraction", "initial_evaluation")
    workflow.add_edge("initial_evaluation", "review_evaluation")
    workflow.add_edge("review_evaluation", "marks_extraction")
    workflow.add_edge("marks_extraction", "total_marks_calculation")

    # Set entry point
    workflow.set_entry_point("class_extraction")

    # Compile the graph
    app = workflow.compile()

    # Run the workflow
    end_state = app.invoke(initial_state)

    # Save final evaluation
    save_final_evaluation(end_state)

    with open('workflow.png', 'wb') as f:
        f.write(app.get_graph().draw_mermaid_png())

    print("Evaluation complete. Results saved in 'final_evaluations.txt'")

if __name__ == "__main__":
    main()