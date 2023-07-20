from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# def entry(request):
#     return render(request, "entries/{title}.md", {
#         "entries": util.get_entry()
#     })