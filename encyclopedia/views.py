import string
import random

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util

import markdown2


class NewSearchForm(forms.Form):
    search_parameter = forms.CharField(label="New Search")


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    entry_text = forms.CharField(widget=forms.Textarea(attrs={"rows": "5", "cols": "5"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })


def display_entry(request, name):
    entry = util.get_entry(name)

    if entry is not None:
        html_entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": string.capwords(name),
            "content": html_entry,
            "form": NewSearchForm
        })
    else:
        article_list = util.list_entries()
        return render(request, "encyclopedia/entry.html", {
            "title": "Nonexistent",
            "content": "<h1>This article does not exist. Please double check your spelling.</h1>"
                       "<h2>Check out the articles we have:</h2>",
            "article_list": article_list,
            "form": NewSearchForm
        })


def search(request):
    form = NewSearchForm(request.POST)

    if form.is_valid():
        results = util.get_entries(form.cleaned_data["search_parameter"])
        if len(results) != 0:
            return render(request, "encyclopedia/search.html", {
                "search_result": True,
                "entries": results,
                "form": NewSearchForm
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "search_result": False,
                "entries": util.list_entries(),
                "form": NewSearchForm
            })

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": form
        })


def create_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            if not util.list_entries().__contains__(form.cleaned_data["title"]):
                title = form.cleaned_data["title"]
                entry_text = form.cleaned_data["entry_text"]

                util.save_entry(title, entry_text)

                return HttpResponseRedirect(reverse("encyclopedia:displayEntry", kwargs={"name": title}))
            else:
                return render(request, "encyclopedia/create.html", {
                    "createForm": form,
                    "form": NewSearchForm(),
                    "createCollision": True
                })
        else:
            return render(request, "encyclopedia/create.html", {
                "createForm": form,
                "form": NewSearchForm(),
                "createCollision": False
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "createForm": NewEntryForm(),
            "form": NewSearchForm(),
            "createCollision": False
        })


def edit_entry(request, name):
    if request.method == "GET":
        entry_text = util.get_entry(name)
        return render(request, "encyclopedia/edit.html",{
            "text": entry_text,
            "name": name
        })
    else:
        util.save_entry(name, request.POST["text"])

        return HttpResponseRedirect(reverse("encyclopedia:displayEntry", kwargs={"name": name}))


def random_entry(request):
    entry = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html",{
        "title": entry,
        "content": markdown2.markdown(util.get_entry(entry)),
        "form": NewSearchForm()
    })