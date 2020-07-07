from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from .forms import QuestionForm, ChoiceFormSet


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    ordering = ["-pub_date"]

    def get_queryset(self):
        """Return last 5 recently published questions.

        Returns:
            Question
        """
        return Question.objects.filter(is_approved=True, pub_date__lte=timezone.now())[
            :5
        ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Exclude questions that aren't published yet.

        Returns:
            Question
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """Exclude questions that aren't published yet.

        Returns:
            Question
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def create(request):
    template_name = "polls/create.html"

    if request.method == "POST":
        question_form = QuestionForm(request.POST or None)
        choices_formset = ChoiceFormSet(request.POST or None)
        if question_form.is_valid() and choices_formset.is_valid():
            question = question_form.save()
            for choice_form in choices_formset:
                if choice_form.has_changed():
                    choice_form.empty_permitted = False
                    choice = choice_form.save(commit=False)
                    choice.question = question
                    choice.save()
            return HttpResponseRedirect(reverse("polls:index"))
    else:
        question_form = QuestionForm()
        choices_formset = ChoiceFormSet()
    context = {"question": question_form, "choices": choices_formset}
    return render(request, "polls/create.html", context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        context = {"question": question, "error_message": "No selected choice."}
        return render(request, "polls/detail.html", context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
