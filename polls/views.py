import datetime
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from polls.models import Question, Choice

from django.template import loader

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.views import generic
from django.utils import timezone
#polls관련 4가지 뷰 만들기
'''
색인페이지->최근 질문들을 표시
세부페이지->질문 내용과 투표할 수 있는 서식 표시
결과 페이지 -> 특정 질문에 대한 결과를 표시
투표기능->특정 질문에 대해 특정 선택을 할 수 있는 투표 기능 제공
'''

"""
def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    output=', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
# loader 방식?
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template=loader.get_template('index.html')
    #polls/index가 아니라 index바로 쓰기 (윗줄)
    context={'latest_question_list':latest_question_list}
    return HttpResponse(template.render(context,request))
# return render(request, 'polls/index.html',context)

def results(request,question_id):
    response="You're looking at the results of question %s."
    return HttpResponse(response%question_id)

"""




"""
def detail(request,question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render (request,'detail.html',{'question':question})

def results (request,question_id):
    question= get_object_or_404(Question,pk=question_id)
    return render(request,'results.html',{'question':question})

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice= question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'detail.html',{'question':question,'error_message':"You didn't select a choice."})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
"""

class IndexView(generic.ListView):
    template_name='index.html'
    context_object_name='latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date_lte=timezone.now().order_by('-pub_date')[:5])
#return Question.objects.order_by('-pub_date')[:5]

#contexxt_object_name이 가리켜는 부분이 return 값? > ListView

class DetailView(generic.DetailView):
    model=Question
    template_name='detail.html'

class ResultsView(generic.DetailView):
    model=Question
    template_name='results.html'
#pk로 인수를 사용하니깐 pk=question.id 안하고 바로 속성 pk 값으로 이동?

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice= question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'detail.html',{'question':question,'error_message':"You didn't select a choice."})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

def create_question(question_text,days):
    time=timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    def test_past_question(self):
        create_question(question_text="Past question.",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question:Past question.>']
        )
    def test_future_question(self):
        create_question(question_text='Past question.',days=-30)
        create_question(question_text="Future question.",days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.",days=-30)
        create_question(question_text="Future question",days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],['<Question: Past question.>']
        )
    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],['<Question: Past question 2.>','<Question: Past question 1.>']
        )
