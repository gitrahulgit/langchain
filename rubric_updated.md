**Rubric \[Total Marks \= 37\]**

1. Extract Class Method \[5 marks\]  
2. Extract Rubric Method \[5 marks\]  
3. Initial Evaluation \[5 marks\]  
4. Review Evaluation \[5 marks\]  
5. Marks Extraction \[5 marks\]  
6. Total Marks Calculation \[5 marks\]  
7. Graph construction \[7 marks\]
   
---

**Rubric Details (Total Marks \= 37\)**

- Do not deduct any marks for error handling or type checking.  
- Please do not give any marks or comments on compilation as that will be done manually separately.  
- Strictly adhere to the rubric mentioned below.  
- If any portion of the rubric is not applicable or not found in the solution, strictly do not give any marks for that portion.  
- Strictly use the provided model_solution as the reference for correctly invoking the LLM, for correctly parsing the output of the LLM invocation, and for correctly saving the LLM output as part of the state for the subsequent use.

---

**1\. Extract Class Method \[5 marks\]:** Successfully extract individual Java classes from the student code and the model solution. This is further broken down into the following items:

* **Prompt Design (2 marks)**: Proper LLM prompt should be used to ensure appropriate input elements are passed. Either there should be separate prompts for student code and model solution or a single prompt containing both.  
  * 2 marks: Prompts ensure proper input.  
  * 1 mark: Prompts are reasonable but incomplete.  
  * 0 marks: Prompts lack critical details.  
* **Parsing/Output Extraction (2 marks)**: LLM output should correctly extract the individual classes.  
  * 2 marks: Correct parsing and accurate class extraction.  
  * 1 mark: Partial parsing or missed classes.  
  * 0 marks: Parsing not effective.  
* **State Saving (1 mark)**: Saves extracted class information to state variables for subsequent use.  
  * 1 mark: Correct use of state variables.  
  * 0 marks: Information not saved properly.

---

**2\. Extract Rubric Method \[5 marks\]:** Successfully extracts rubric details for each class. This is further broken down into the following items:

* **Prompt Design (2 marks)**: Prompt efficiently passes relevant rubric elements to the LLM.  
  * 2 marks: Prompt includes all necessary details.  
  * 1 mark: Prompt is partially complete.  
  * 0 marks: Prompt design is poor.  
* **Parsing/Output Extraction (2 marks)**: Correctly extracts rubric details from the LLM.  
  * 2 marks: Full extraction.  
  * 1 mark: Partial extraction.  
  * 0 marks: Extraction fails.  
* **State Saving (1 mark)**: Rubric details are saved for later nodes.  
  * 1 mark: Saved correctly.  
  * 0 marks: Not saved or improperly stored.

---

**3\. Initial Evaluation Method \[5 marks\]:** Accurately evaluates classes in the student code based on rubric and model solution. This is further broken down into the following items:

* **Prompt Design (2 marks)**: Prompt includes class code, relevant rubric, and model solution for accurate assessment.  
  * 2 marks: Properly structured prompt.  
  * 1 marks: Incomplete prompt.  
  * 0 marks: Poor prompt design.  
* **Parsing/Output Extraction (2 marks)**: Proper extraction of detailed evaluation and numeric scores.  
  * 2 marks: Complete extraction of scores and comments.  
  * 1 mark: Incomplete extraction.  
  * 0 marks: Incorrect or no extraction.  
* **State Saving (1 mark)**: Evaluation results are correctly saved for future nodes.  
  * 1 mark: Correct state management.  
  * 0 marks: Improper or missing state saving.

---

**4\. Review Evaluation Method \[5 marks\]:** Correctly reviews and corrects initial evaluations using the LLM. This is further broken down into the following items:

* **Prompt Design (2 marks)**: Effective prompt for reviewing evaluation and making corrections.  
  * 2 marks: Well-structured prompt.  
  * 1 mark: Incomplete or vague prompt.  
  * 0 marks: Poor prompt.  
* **Parsing/Output Extraction (2 marks)**: Correctly extracts the reviewed evaluation and adjustments.  
  * 2 marks: Complete and correct.  
  * 1 mark: Partial extraction.  
  * 0 marks: Incorrect or no extraction.  
* **State Saving (1 mark)**: Correctly saves reviewed evaluation for further use.  
  * 1 mark: Saves correctly.  
  * 0 marks: Incorrect or no state saving.

---

**5\. Marks Extraction Method \[5 marks\]:** Correctly extracts comma-separated marks for each class. This is further broken down into the following items:

* **Prompt Design (2 marks)**: Ensures proper prompting for marks extraction.  
  * 2 marks: Prompt is complete and effective.  
  * 1 mark: Incomplete prompt.  
  * 0 marks: Poor prompt.  
* **Parsing/Output Extraction (2 marks)**: Proper extraction of marks from LLM response.  
  * 2 marks: All marks extracted.  
  * 1 mark: Partial extraction.  
  * 0 marks: No or incorrect extraction.  
* **State Saving (1 mark)**: Correct state saving of marks for final calculation.  
  * 1 mark: State saved correctly.  
  * 0 marks: Incorrect or missing state.

---

**6\. Total Marks Calculation Method \[5 marks\]:** Correctly sums marks for all classes using the sum_marks tool. This is further broken down into the following items:

* **Prompt Design (2 marks)**: Prompt strictly uses the `sum_marks` tool.  
  * 2 marks: Proper prompt.  
  * 1 mark: Incomplete prompt.  
  * 0 marks: Ineffective prompt.  
* **Parsing/Output Extraction (2 marks)**: Correct extraction of the final sum.  
  * 2 marks: Fully correct.  
  * 1 mark: Partially correct.  
  * 0 marks: Incorrect or no extraction.  
* **State Saving (1 mark)**: Final total is saved in the correct state.  
  * 1 mark: State saved.  
  * 0 marks: Incorrect or missing state.

---

**7\. Graph Construction (7 marks):** Proper LangGraph workflow with nodes for each module and edges connected one module to next.

* **Correct addition of nodes to the graph (3 marks)**: All the modules are correctly added as nodes in the graph.  
  * 3 marks: All the modules are corrected and added.  
  * 1.5 marks: Some of the modules are not correctly added.  
  * 0 marks: None of the modules are correctly added.  
* **Correct addition of edges to the graph (3 marks)**: All the edges between the modules are correctly added as nodes in the graph.  
  * 3 marks: All the edges are corrected and added.  
  * 1.5 marks: Some of the edges are not correctly added.  
  * 0 marks: None of the edges are correctly added.  
* **Correct compilation of graph (1 mark):** The graph is correctly compiled using a suitable method call.  
  * 1 mark: The graph is correctly compiled.  
  * 0 mark: The graph is not correctly compiled.
