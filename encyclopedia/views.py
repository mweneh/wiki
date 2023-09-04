from django.shortcuts import render, redirect

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
def search(request):
    query = request.GET.get('q', '')  # Get the query from the request's GET parameters
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    if len(matching_entries) == 1:
        # If there's an exact match, redirect to the entry page
        return redirect('entry', title=matching_entries[0])
    else:
        return render(request, "encyclopedia/search.html", {"query":query, "entries":matching_entries})