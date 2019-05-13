from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
# Create your views here.
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        return Question.objects.filter(
            pub_date_lte=timezone.now()
        ).order_by("-pub_date")[:5]
        # return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
class ResultsView(generic.DetailView):
    model = Question
    template_name = "results.html"


def vote(request , question_id):
    question = get_object_or_404(Question , pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except(KeyError , Choice.DoesNotExist):
        return render(request , "detail.html" , {
            'question' :question ,
            'error_message':"You didn't select a  Choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return  HttpResponseRedirect(reverse('polls:results',args = (question.id , ) ) )


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list" : latest_question_list ,}
#     #快捷函数render
#     return render( request , "index.html" , context)

    #结合模板 用httpresponse 来调用
    # latest_question_list = Question.objects.order_by("-pub_date" )[:5]
    # template = loader.get_template("index.html")
    # context = {
    #     "latest_question_list" : latest_question_list ,
    # }
    # return HttpResponse(template.render(context , request))


    #纯输出
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = "<br>".join([ q.question_text for q  in latest_question_list])
    # return HttpResponse(output)

    # return HttpResponse("hello cjw")

# def detail(request , question_id):
#     # try:                  #复杂代码
#     #     question = Question.objects.get( pk = question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Quetion does not exist")
#
#     #简便代码
#     question =  get_object_or_404( Question , pk = question_id)
#     return render( request , "detail.html" , {'question' : question})
    # return HttpResponse("You're looking at question %s." %question_id )
# def results(request , question_id):
#     # respones = "You ' re looking at the results of  question %s."
#     # return  HttpResponse(respones% question_id)
#     question  =get_object_or_404( Question, pk = question_id)
#     return render(request , "results.html" , {"question" :question })




