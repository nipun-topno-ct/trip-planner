from django.shortcuts import render

import json
import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Expense
from django.db.models import Sum
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def get_tip(request, text=None):
    if text:
        expenses = Expense.objects.filter(text__icontains=text)
    else:
        # If no text is provided, fetch all expenses
        expenses = Expense.objects.all()

    # Serialize the expenses data
    locations = [
        {
            'location': expense.location,
        }
        for expense in expenses
    ]

    

    return Response(locations)


@api_view(['POST'])
def expense(request):
    request_body = json.loads(request.body)

    text = request_body['text']
    amount = request_body['amount']
    category=request_body['category']
    print("REACHED\n\n")

    

    openai.api_type = "azure"
    openai.api_base = "https://openai-hack-3.openai.azure.com/"
    openai.api_version = "2023-07-01-preview"
    openai.api_key = "f0b2edade75a4379902455ad926ad5c1"

    location_prompt = f'i went to {text} bangalore hotel where I spent {amount} on {category}, provide a budget-friendly and comparatively equal rating alternative in the same area along with specific details (e.g., name of the place, type of activity, potential cost savings). , give me just 20 words output'
    print(location_prompt)

    message_text = [
        {
            "role": "system",
            "content": location_prompt
        }
    ]
    location_response = openai.ChatCompletion.create(
        engine = "openai-Hack-key3",
        messages = message_text,
        temperature = 0.7,
        max_tokens = 800,
        top_p = 0.95,
        frequency_penalty = 0,
        presence_penalty = 0,
        stop = None
    )
    print(location_response)
    location = location_response['choices'][0]['message']['content']
    print(location)
    expense = Expense.objects.create(
        text=text,
        amount=amount,
        category=category,
        location=location  # Assuming 'location' is the result from your OpenAI logic
    )

    return Response(location)


@api_view(['GET'])
def get_expenses(request, category=None):
    # If a category is provided, filter expenses by category
    if category:
        expenses = Expense.objects.filter(category=category)
    else:
        # If no category is provided, fetch all expenses
        expenses = Expense.objects.all()

    # Calculate the sum of expenses for each category
    expense_sum_by_category = (
        Expense.objects.values('category')
                      .annotate(total_amount=Sum('amount'))
                      .order_by('category')
    )

    # Serialize the expenses data with the sum for each category
    serialized_expenses = [
        {
            'id': expense.id,
            'text': expense.text,
            'amount': str(expense.amount),
            'category': expense.category,
            'location': expense.location,
            'created_at': expense.created_at.isoformat(),
        }
        for expense in expenses
    ]

    response_data = {
        'expenses': serialized_expenses,
        'total_amount_by_category': list(expense_sum_by_category),
    }

    return Response(response_data)


@api_view(['DELETE'])
def delete_expense(request, expense_id):
    # Get the expense object or return 404 if not found
    expense = get_object_or_404(Expense, id=expense_id)

    # Delete the expense
    expense.delete()
 

    return Response({'message': 'Expense deleted successfully'})