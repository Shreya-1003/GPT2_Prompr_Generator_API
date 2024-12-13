from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from transformers import pipeline
from .models import Recipe

# Initialize GPT-2 model pipeline
generator = pipeline("text-generation", model="gpt2")

# Function to generate GPT-2 response
def generate_gpt2_response(prompt, max_length=200):
    try:
        response = generator(
            prompt,
            max_length=max_length,
        )
        return response[0]['generated_text'].strip()
    except Exception as e:
        return f"Error: {e}"

# Django REST Framework view to handle API requests
@api_view(['POST', 'PUT'])
def generate_text(request):
    try:
         # Check if request.data is a dictionary or list
        if isinstance(request.data, dict):
            prompt_data = request.data.get("prompts", [])
        elif isinstance(request.data, list):  # Direct list case
            prompt_data = request.data
        else:
            return Response(
                {"error": "Invalid request format. Expected JSON object or array."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate input type
        if not isinstance(prompt_data, list):
            return Response(
                {"error": "The 'prompts' field must be a list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate individual prompt objects
        if not all(isinstance(obj, dict) for obj in prompt_data):
            return Response(
                {"error": "Each item in the 'prompts' list must be a dictionary."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure each dictionary contains 'prompt_1' and 'prompt_2'
        for obj in prompt_data:
            if 'prompt_1' not in obj or 'prompt_2' not in obj:
                return Response(
                    {"error": "Each dictionary must contain 'prompt_1' and 'prompt_2' keys."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Process each prompt and generate responses
        responses = []
        for obj in prompt_data:
            prompt_1 = obj.get("prompt_1", "").strip()
            prompt_2 = obj.get("prompt_2", "").strip()

            # Validate that 'prompt_1' and 'prompt_2' are non-empty strings
            if not prompt_1 or not prompt_2:
                return Response(
                    {"error": "Both 'prompt_1' and 'prompt_2' must be non-empty strings."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the individual prompt
            user_message = f"Write a detailed recipe for {prompt_1} for a quantity of {prompt_2}."

            # Generate GPT-2 response for the prompt
            gpt2_output = generate_gpt2_response(user_message, max_length=300)

            # Check if GPT-2 returned an error
            if gpt2_output.startswith("Error:"):
                return Response(
                    {"error": f"GPT-2 encountered an error: {gpt2_output}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Save the response in the database
            recipe = Recipe.objects.create(
                prompt_1=prompt_1,
                prompt_2=prompt_2,
                gpt2_response=gpt2_output
            )

            # Append the result to the responses list
            responses.append({
                "id": recipe.id,
                "prompt_1": recipe.prompt_1,
                "prompt_2": recipe.prompt_2,
                "gpt2_response": recipe.gpt2_response,
                "created_at": recipe.created_at
            })

        # Return the responses based on the HTTP method
        if request.method == 'POST':
            return Response(
                {"message": "Recipes created successfully.", "response": responses},
                status=status.HTTP_201_CREATED
            )
        elif request.method == 'PUT':
            return Response(
                {"message": "Recipes updated successfully.", "response": responses},
                status=status.HTTP_200_OK
            )

    except Exception as e:
        # Catch any unexpected errors
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        




































































# from transformers import T5ForConditionalGeneration, T5Tokenizer
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# # Initialize T5 model and tokenizer
# model_name = "t5-large"
# t5_model = T5ForConditionalGeneration.from_pretrained(model_name)
# t5_tokenizer = T5Tokenizer.from_pretrained(model_name)

# # Function to generate T5 response
# def generate_t5_response(prompt, max_length=150):
#     try:
#         # Use a clearer instruction in the prompt to avoid repetition
#         input_text = f"Provide a detailed answer to the question: {prompt}"
        
#         # Tokenize and generate response
#         inputs = t5_tokenizer(input_text, return_tensors="pt")
#         outputs = t5_model.generate(
#             inputs.input_ids, 
#             max_length=max_length, 
#             num_beams=5,    #search setting for diverse outputs
       
#             repetition_penalty=2.5,  # Penalizes repetitive sequences
#             temperature=0.7  # Adds randomness for less repetitive outputs-gives unique response
#         )
#         response = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return response.strip()
#     except Exception as e:
#         return f"Error: {e}"

# # Django REST Framework view to handle API requests
# @api_view(['GET', 'POST', 'PUT'])
# def generate_text(request):
#     if request.method == 'GET':
#         return Response({"message": "Welcome to the enhanced T5 text generation API.."}, status=status.HTTP_200_OK)

#     prompt_1 = request.data.get("prompt_1", "")
#     prompt_2 = request.data.get("prompt_2", "")

#     if not prompt_1:
#         return Response({"error": "'prompt_1' is required"}, status=status.HTTP_400_BAD_REQUEST)

#     # Combine prompts into one clear prompt if both are present
#     user_message = f"{prompt_1}. {prompt_2}" if prompt_2 else prompt_1

#     if request.method == 'POST':
#         output_t5 = generate_t5_response(user_message, max_length=150)
#         return Response({"response": output_t5}, status=status.HTTP_200_OK)

#     elif request.method == 'PUT':
#         updated_output_t5 = generate_t5_response(f"Updated: {user_message}", max_length=150)
#         return Response({"response": updated_output_t5}, status=status.HTTP_200_OK)
