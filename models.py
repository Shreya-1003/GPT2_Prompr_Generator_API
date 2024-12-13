from django.db import models

class Recipe(models.Model):
    prompt_1 = models.TextField(default="default prompt 1")
    prompt_2 = models.TextField(default="default prompt 2")
    gpt2_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prompt_1} | {self.prompt_2}"


