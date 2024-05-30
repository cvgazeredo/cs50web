from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from random import choice
from markdown2 import Markdown
from . import util

conversor = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    print(content)
    if not content:
        return HttpResponse("Page not found")

    return render(request, "encyclopedia/entry.html", {
        "content": conversor.convert(content),
        "title": title
    })

def search(request):
    #The request object contains information about the user's request (what data was sent to the page)
    #request.GET contains the GET variables - what you see in your browser's address bar
    #.get() methos is used for dictionaries
    #Like "Get the value of a GET variable with name q, and if it doesnt exist, return empty"
    entry_search = str(request.GET.get('q'))
    
    print(entry_search)

    if util.get_entry(entry_search) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={"title": entry_search}))
    #**kwargs allows you to handle named arguments that you have not defined in advance.
    else:
        SubstringCheck = []
        for entry in util.list_entries():
            if entry_search.lower() in entry.lower():
                SubstringCheck.append(entry)
                print(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": SubstringCheck
        })


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(title)
        print(content)

        for entry in util.list_entries():
            if title in entry:
                return HttpResponse("This entry already exist")

        util.save_entry(title, content)
        
        return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    content = util.get_entry(title)
    conversor.convert(content)
    if request.method == 'POST':
        new_content = request.POST.get('new_content')
        print(new_content)
        util.save_entry(title, new_content)
        
        print(title)

        return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
        # return render(request, "encyclopedia/entry.html", {
        #     "content": new_content,
        #     "title": title
        # })

    return render(request, "encyclopedia/edit.html", {
        "content": content,
        "title": title
    })

def random(request):
    entries_list = util.list_entries()
    print(entries_list)

    title = choice(entries_list) 
    print(title)
    return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))





