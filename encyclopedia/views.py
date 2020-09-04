from django.shortcuts import render
from django.utils.safestring import mark_safe
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
import random
from . import util

class NewTaskForm(forms.Form):
    title = forms.CharField(label=('Title'))
    content = forms.CharField(label=(''), widget=forms.Textarea(attrs={'placeholder' : 'Markdown','style': 'resize:none; height: 450px; width: 700px; display: block; padding: 10px; margin-bottom: 10px'}))
    # content = forms.CharField(label="Data", widget=forms.Textarea(attrs={"style": "resize: none"}))

class EditDataForm(forms.Form):
    data = forms.CharField(label="" , widget=forms.Textarea(attrs={'style': 'resize:none; height: 500px; width: 750px;'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            page_list = util.list_entries()
            content = form.cleaned_data["content"]
            if title in page_list:
                return render(request, "encyclopedia/create.html", {
                    "form": "Page already exists"
                })
            util.save_entry(title, content)
            url = reverse('page', kwargs={'title': title})
            return HttpResponseRedirect(url)
        else: 
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
            "form": NewTaskForm()
    })

def page(request, title):
    page_list = util.list_entries()
    html = util.get_entry(title)
    if title in page_list:
        return render(request, "encyclopedia/wiki/page.html", {
            "title": title,
            "html": html
        })
    return render(request, "encyclopedia/wiki/page.html", {
        "title": "Page Not Found"
    })

def edit(request,title):
    content = util.get_entry(title)  
    if request.method == "POST":
        form = EditDataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["data"]
            util.save_entry(title, data)
            url = reverse('page', kwargs={'title': title})
            return HttpResponseRedirect(url)
    form = EditDataForm(initial={'data': content})
    return render(request, "encyclopedia/wiki/edit.html", {
        "title": title,
        "content": content,
        "form": form
    })
    
def search(request):
    title = request.POST["title"]
    page_list = util.list_entries()
    if title in page_list:
        url = reverse('page', kwargs={'title': title})
        return HttpResponseRedirect(url)
    else:
        # options = page_list.objects.filter(title_startswith="title")
        options = [s for s in page_list if str.lower(title) in str.lower(s)]
        return render(request, "encyclopedia/index.html", {
            "entries": options
        })
    
    
    
def random_page(request):
    page_list = util.list_entries()
    number = random.randint(0, len(page_list)-1)
    title = page_list[number]
    url = reverse('page', kwargs={'title': title})
    return HttpResponseRedirect(url)
    