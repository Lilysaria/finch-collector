from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch
from .forms import FeedingForm
# Add this cats list below the imports

# Create your views here.
class FinchUpdate(UpdateView):
  model = Finch
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = [ 'species', 'description', 'migration_patterns', 'habitat']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches'

class FinchCreate(CreateView):
  model = Finch
  fields = '__all__'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finches_index(request):
    # tell the model to find all the rows in the cats table
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {
        'finches': finches
        #'cats' becomes a variable name in 'cats/index.html'
        # just like express 
        # res.render('cats/index', {'cats': cats})
    })

# cat_id comes from the path in the urls.py 
# path('cats/<int:cat_id>/', views.cats_detail, name='detail'),
def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()
  return render(request, 'finches/detail.html', {
    # include the cat and feeding_form in the context
    'finch': finch, 'feeding_form': feeding_form
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
