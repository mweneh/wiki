from django.shortcuts import render, redirect
from django import forms
import random
from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label= 'Title')
    content = forms.CharField(label= 'Content here',widget=forms.Textarea(attrs={"maxlength": None}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry( title)
    if content is None: 
        return render(request, "encyclopedia/error.html", {"message": "Entry not found."})
    htmlcontent =util.markdown_to_html(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": htmlcontent
    })
def search(request):
    query = request.GET.get('q', '')  # Get the query from the request's GET parameters
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    if len(matching_entries) == 1:
        # If there's an exact match, redirect to the entry page
        return redirect('entry', title=matching_entries[0])
    else:
        return render(request, "encyclopedia/search.html", {"query": query, "entries": matching_entries})

def add(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if an entry with the same title already exists
            if util.get_entry(title):
                error_message = f"An encyclopedia entry already exists with the title '{title}'."
                return render(request, "encyclopedia/error.html", {"message": error_message})
            # Save the new entry to disk using the util function
            util.save_entry(title, content)

            # Redirect to the new entry's page
            return redirect("entry", title=title)
    else:
        form = NewPageForm()

    return render(request, "encyclopedia/add.html", {"form": form})
def edit(request,title):
    content = util.get_entry(title)
    if content is None: 
        return render(request, "error.html", {"message": "Entry not found."})
    if request.method =="POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['content']
            util.save_entry(title, new_content)
            return redirect('entry',title=title)
    else:
        form = NewPageForm(initial={"title":title, "content":content})
    return render(request,"encyclopedia/edit.html",{'form':form, "title":title})

def random_page(request):
    entries = util.list_entries()
    if entries:
        random_title = random.choice(entries)
        return redirect("entry" , title=random_title)  
