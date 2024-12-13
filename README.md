# GPT2_Prompt_Generator_API
This project is a RESTful API powered by Django and GPT-2, designed to generate creative and detailed recipes based on user-provided inputs. It utilizes the Hugging Face Transformers library to integrate a pre-trained GPT-2 language model for dynamic text generation.

--Features
Text Generation: Generates creative recipes using GPT-2 based on prompts provided by users.
Multi-Method Support: Supports POST for creating new records and PUT for both creating and updating existing records.
Validation and Error Handling: Ensures proper validation of user input and returns informative error messages for invalid requests.
Database Integration: Stores generated recipes and user inputs in a MySQL database for persistence.
Automated Responses: Dynamically processes multiple user prompts in a single request, creating recipes in bulk.

How It Works:-
1.User Input:
The user provides recipe prompts through a JSON payload containing prompt_1 (recipe name) and prompt_2 (quantity).
2.Recipe Generation:
The API processes the prompts and generates a detailed recipe using GPT-2.
3.Database Operations:
Stores the generated recipes in a MySQL database with options to create or update entries.
4.Output:
Returns the stored recipes with metadata like recipe ID, creation time, and GPT-2 output.

Tech Stack
Backend: Django REST Framework
AI Model: GPT-2 (via Hugging Face Transformers)
Database: MySQL
Language: Python
