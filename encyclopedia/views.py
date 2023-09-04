from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry( title)
    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": content
    })
def search(self, request, title):
    content = util.get_entry(self)
    return render(request, "encyclopedia/search.html",{
        "title": title, "content": content
    })