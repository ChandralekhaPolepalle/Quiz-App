# quiz_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, QuizResult
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
@login_required
def quiz(request):
    if request.method == 'POST':
        # Process quiz submission
        quiz_id_list = request.POST.getlist('quiz_id')
        user_answers = request.POST.getlist('user_answer')

        total_questions = len(quiz_id_list)
        correct_answers = 0

        for quiz_id, user_answer in zip(quiz_id_list, user_answers):
            quiz = Quiz.objects.get(pk=quiz_id)
            if user_answer == quiz.correct_option:
                correct_answers += 1

            # Store quiz result
            QuizResult.objects.create(user=request.user, quiz=quiz, score=correct_answers)

        percentage = (correct_answers / total_questions) * 100
        messages.success(request, f'Your score: {correct_answers}/{total_questions} ({percentage}%)')

        if percentage < 50:
            return redirect('quiz')
        else:
            return redirect('view_results')

    else:
        all_quiz_questions = Quiz.objects.all()

        # Paginate the questions
        paginator = Paginator(all_quiz_questions, 1)  # Display one question per page
        page = request.GET.get('page', 1)

        try:
            quiz_questions = paginator.page(page)
        except PageNotAnInteger:
            quiz_questions = paginator.page(1)
        except EmptyPage:
            quiz_questions = paginator.page(paginator.num_pages)

        context = {'quiz_questions': quiz_questions}
        return render(request, 'quiz.html', context)


@login_required
def view_results(request):
    # Display all quiz results, average, highest, and lowest scores
    quiz_results = QuizResult.objects.filter(user=request.user)

    total_quizzes = quiz_results.count()
    if total_quizzes > 0:
        average_score = sum(result.score for result in quiz_results) / total_quizzes
        highest_score = max(result.score for result in quiz_results)
        lowest_score = min(result.score for result in quiz_results)
    else:
        average_score = highest_score = lowest_score = 0

    context = {
        'quiz_results': quiz_results,
        'average_score': average_score,
        'highest_score': highest_score,
        'lowest_score': lowest_score,
    }

    return render(request, 'results.html', context)
