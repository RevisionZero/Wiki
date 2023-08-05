import string

from django.shortcuts import render
from django.http import HttpResponse

from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def display_entry(request, name):
    entry = util.get_entry(name)

    if entry is not None:
        html_entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": string.capwords(name),
            "content": html_entry
        })
    else:
        article_list = util.list_entries()
        return render(request, "encyclopedia/entry.html", {
            "title": "Nonexistent",
            "content": "<h1>This article does not exit. Please double check your spelling.</h1>"
                       "<h2>Check out the articles we have:</h2>",
            "article_list": article_list
        })
