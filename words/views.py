from django.shortcuts import render, redirect
from .models import (
    word, 
    meaning, 
    example
)
from django.views.generic import (
    DetailView, 
    View,
    ListView,
    CreateView,
    FormView,
    UpdateView,
    TemplateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .forms import (
    WordCreateForm,
    WordEditForm,
    MeaningCreateForm,
    SelectMeaningForm,
    AddExamleForm,
    EditMeaningForm
)
from django.core.paginator import Paginator

class DteailView(DetailView):
    queryset = word.objects.all()
    template_name = 'words/detail.html'
    context_object_name = 'words'


class WordsView(ListView):
    model = word
    #queryset = word.objects.all().order_by('-date')
    template_name = 'words/list.html'
    context_object_name = 'words'
    paginate_by = 9

    def get_queryset(self):
        if self.request.GET.get('q'):
            queryset = word.objects.search(self.request.GET.get('q')).order_by('-date')
        else:
            queryset = word.objects.all().order_by('-date')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(WordsView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    

class CreateWordView(LoginRequiredMixin, CreateView):
    queryset = word.objects.all()
    login_url = 'accounting:signin'
    template_name = 'words/create.html'
    form_class = WordCreateForm
    success_url = 'words: words_list'
    def post(self, request):
        form = WordCreateForm(request.POST)
        if form.is_valid():
            instance = word()
            instance.user = request.user
            instance.spell = request.POST['spell']
            instance.mood = request.POST['mood']
            try:
                instance.note = request.POST['note']
            except:
                pass
            #the try is to check whether th note field is there or not
            instance.save()
            return redirect('words:words_list')
        else:
            return render(request, self.template_name, {'form':form})
    # clould also use the foem_valid function to assign the instance.user


class EditView(UpdateView):
    model = word
    form_class = WordEditForm
    template_name = 'words/edit.html'
    context_object_name = 'word'
    success_url = '/'


class AddMeaningView(LoginRequiredMixin, CreateView, DetailView):
    queryset = word.objects.all()  
    '''since the queryset is for the detailciew and we added that to retrive 
    the word using the slug, it's words.objects.all instead of meaning.objects.all'''
    success_url = '/'  # should be changed
    login_url = 'accounting:signin'
    form_class = MeaningCreateForm
    template_name = 'words/addmeaning.html' 
    def get_context_data(self, *args, **kwargs):
        context = super(AddMeaningView, self).get_context_data(*args, **kwargs)
        # print(context)
        # print(self.request.path)
        # print(kwargs)
        #I used Detail view inheritance to grab the slug and be able to add it to the context. Since in create view It won't get it
        #I could also use request.path to grab the slug manually
        #and also, since I'll have to do the post manually, I'll have to get slug as a prameter 
        #and if I were to set the get function manually as well, I did not have to use Detaiview since I could grab it as a prameter
        return context 

    
    def post(self, request, slug):
        form = MeaningCreateForm(data=request.POST)
        qs = word.objects.get(slug=slug)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.parent = qs
            instance.save()
            qs.meanings.add(instance)
            qs.save()
            return redirect('/words/'+str(qs.slug))
        else:
            return render(request, self.template_name, {'form':form, 'word': qs})


class SelectMeaningAddExampleView(LoginRequiredMixin, UpdateView, FormView):
    queryset = word.objects.all()
    template_name = 'words/selectmeaningfoadd.html'
    form_class = SelectMeaningForm
    context_object_name = 'word'
    login_url = 'accounting:signin'

    #i used the update view to have my instance word passed to the form so that i would use it to norrow down the list ofmeanings shown

    def post(self, request, slug):
        instance = word.objects.get(slug=slug)
        pk = request.POST.get('meanings')
        return redirect('/words/meanings/'+str(pk))



class AddExamleView(LoginRequiredMixin ,CreateView, DetailView):
    queryset = meaning.objects.all()
    form_class = AddExamleForm
    template_name = 'words/addexample.html'
    context_object_name = 'meaning'
    login_url = 'accounting:signin'

    def post(self, request, pk):
        obj = meaning.objects.get(id=pk)
        form = AddExamleForm(request.POST)  # request.POST is a key word argument now
        if form.is_valid():
            instance = form.save(commit=False)
            instance.parent = obj
            instance.save()
            obj.examples.add(instance)
            return redirect('/words/'+str(obj.parent.slug))
        else:
            return render(request, self.template_name, {'form':form, 'meaning':obj})


class SelectMeaningEditView(SelectMeaningAddExampleView):
    template_name = 'words/selectmeaningedit.html'
    def post(self, request, slug):
        pk = request.POST.get('meanings')
        return redirect('/words/meanings/'+str(pk)+'/edit')



class EditMeaningView(LoginRequiredMixin, UpdateView):
    queryset = meaning.objects.all()
    form_class = EditMeaningForm
    template_name = 'words/editmeaning.html'
    login_url = 'accounting:signin'
    
    def post(self, request, pk):
        instance = meaning.objects.get(id=pk)
        form = EditMeaningForm(data=request.POST, instance=instance) #the instance is needed to be given to the form since we are saveing using form.save 
        #thus form needs the instance to be able to update it since this is an update form
        if form.is_valid():
            form.save()
            return redirect('/words/'+str(instance.parent.slug))
        else:
            return render(request, self.template_name, {'form':form, 'meaning':instance})


class DeleteWordView(LoginRequiredMixin, DeleteView):
    login_url = 'accounting:signin'
    queryset = word.objects.all()
    success_url = '/'
    template_name = 'words/deleteword.html'
    context_object_name = 'word'


class SelectMeaningDeleteView(SelectMeaningAddExampleView):
    template_name = 'words/selecetmeaningdel.html'

    def post(self, request, slug):
        pk = request.POST.get('meanings')
        return redirect('/words/meanings/'+str(pk)+'/delete')


class DeleteMeaningView(LoginRequiredMixin, DeleteView):
    login_url = 'accounting:signin'
    queryset = meaning.objects.all()
    success_url = '/'
    context_object_name = 'meaning'
    template_name = 'words/delmeaning.html'
