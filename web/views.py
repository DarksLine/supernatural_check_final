from django.http.response import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render, redirect
from .models import *
from .storage import StorageFactory
from django.views.generic import View


class InitialView(View):
    def get(self, request):

        request.session.create()

        return render(request, 'initial.html')

    def post(self, request):
        count_psychics = int(request.POST['count'])

        gamer = User()
        the_list_psychics = PsychicList()
        the_list_psychics.create_list_psychics(count_psychics)

        storage = StorageFactory.create_storage(session_key=request.session.session_key)
        storage.save(the_list_psychics)
        storage.save_user(gamer)

        return HttpResponseRedirect(reverse('testing_url'))


class TestingView(View):
    def get(self, request):
        storage = StorageFactory.create_storage(session_key=request.session.session_key)
        the_list_psychics = storage.load()

        view_list = []
        for psy in the_list_psychics.list_psychics:
            psy.try_predict_number()
            view_list.append({
                'name': psy.name,
                'guess': psy.predict_number[-1]
            })

        storage.save(the_list_psychics)

        return render(request, 'testing.html', {'list_res': view_list})

    def post(self, request):
        number = int(request.POST['answer'])
        storage = StorageFactory.create_storage(session_key=request.session.session_key)
        the_list_psychics = storage.load()
        gamer = storage.load_user()

        for psy in the_list_psychics.list_psychics:
            psy.result_predict(number)

        gamer.get_conceived_numbers(number)

        storage.save(the_list_psychics)
        storage.save_user(gamer)
        return redirect('/result')


class ResultView(View):
    def get(self, request):
        storage = StorageFactory.create_storage(session_key=request.session.session_key)
        the_list_psychics = storage.load()
        gamer = storage.load_user()

        conceived_numbers = gamer.conceived_numbers
        view_list = the_list_psychics.get_complete_dict()

        return render(request, 'result.html', {
            'dict_psy': view_list,
            'user_list': conceived_numbers
        })
