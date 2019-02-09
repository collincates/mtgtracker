from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SignUpForm
from collection.models import Collection


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_collection = Collection.objects.create(
                owner=request.user,
                name=f'{username}\'s Collection'
                )
            return redirect(reverse(
                'collection:collection_view',
                kwargs={
                    'collection_slug': user_collection.slug,
                    'user_name': user_collection.owner.username,
                }
            ))
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
