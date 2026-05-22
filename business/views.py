  
# business/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import BusinessIdea, SavedIdea

import random
@login_required
def ideas_view(request):
    business_ideas = BusinessIdea.objects.filter(is_active=True)[:10]
    saved_ideas = SavedIdea.objects.filter(user=request.user)
    return render(request, 'business/ideas.html', {
        'business_ideas': business_ideas,
        'saved_ideas': saved_ideas
    })

@login_required
def generate_ideas_api(request):
    if request.method == 'POST':
        budget = request.POST.get('budget')
        skill_area = request.POST.get('skill_area')
        risk_level = request.POST.get('risk_level')
        
        ideas = BusinessIdea.objects.filter(
            skill_area=skill_area,
            risk_level=risk_level
        ).order_by('?')[:5]
        
        data = [{
            'id': idea.id,
            'title': idea.title,
            'description': idea.description,
            'category': idea.category,
            'investment_level': idea.investment_level,
            'time_to_profit': idea.time_to_profit,
            'difficulty': idea.difficulty,
            'market_size': idea.market_size,
            'profit_margin': idea.profit_margin,
            'scalability_score': idea.scalability_score,
            'competition_level': idea.competition_level,
        } for idea in ideas]
        
        return JsonResponse({'ideas': data})