import string

from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util

import markdown2


class NewSearchForm(forms.Form):
    search_parameter = forms.CharField(label="New Search")


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

