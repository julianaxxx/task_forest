# pet/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Pet, Species


def welcome(request):
    if request.method == 'POST':
        # Create a new pet and save it to the database
        name = request.POST['pet_name']
        species_id = request.POST['pet_species']
        species = Species.objects.get(id=species_id)
        pet = Pet.objects.create(name=name, user=request.user, species=species)
        return redirect('tasks')

    # Pass the list of available species to the template
    species_list = Species.objects.all()
    return render(request, 'pet/welcome.html', {'species_list': species_list})


