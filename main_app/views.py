from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Toy
from .forms import FeedingForm
# Add this cats list below the imports

# Create your views here.
class FinchUpdate(UpdateView):
    model = Finch
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['species', 'description', 'migration_patterns', 'habitat']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'

class FinchCreate(CreateView):
    model = Finch
    fields = ['species', 'description', 'migration_patterns', 'habitat']

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# cats/<int:cat_id>/assoc_toy/<int:toy_id>/
def assoc_toy(request, finch_id, toy_id):
    print(finch_id, toy_id)
    finch = Finch.objects.get(id=finch_id)
    finch.toys.add(toy_id)  # adding a row to our through table the one with 2 foreign keys in sql
    return redirect('detail', finch_id=finch_id)

def finches_index(request):
    # tell the model to find all the rows in the cats table
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {
        'finches': finches
        # 'cats' becomes a variable name in 'cats/index.html'
        # just like express 
        # res.render('cats/index', {'cats': cats})
    })

# cat_id comes from the path in the urls.py 
# path('cats/<int:cat_id>/', views.cats_detail, name='detail'),
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    # We want to search for all the toys that cat does not have!
    # 1. create a list of ids of the toys the cat does have!
    id_list = finch.toys.all().values_list('id')
    # Now we can query the toys table for the toys 
    # that are not in the id_list! field lookups in django (google this)
    toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)
    # instantiate FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {
        # include the cat and feeding_form in the context
        'finch': finch, 'feeding_form': feeding_form, 'toys': toys_finch_doesnt_have
    })

def add_feeding(request, cat_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('detail', cat_id=cat_id)

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
