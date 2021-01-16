from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': "form-control"}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class': "form-control"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    # Get the entry
    entry_info_markdown = util.get_entry(entry)

    if entry_info_markdown is None:
        return render(request, "encyclopedia/error.html")
    else:
        markdowner = Markdown()
        entry_info = markdowner.convert(entry_info_markdown)
        # print("Title: " + entry) # DEBUG
        # print("Info: " + entry_info) # DEBUG

        return render(request, "encyclopedia/entry.html", {
            "entry_info": entry_info
        })

def search(request):
    if request.method == "POST":
        search_term = str(request.POST.get('q', None))
        # print("Searched for: " + search_term)
        entry_list = util.list_entries()
        results = [entry for entry in entry_list if search_term.upper() in entry.upper()]

        # print(str(results))
        return render(request, "encyclopedia/search.html", {
            "results": results, "query": search_term
        })
    else:
        return render(request, "encyclopedia/error.html") # the user should not be able to make it here as post is the only way to get to this url

def create(request):

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })

def create_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entry_info_check = util.get_entry(title) # check if entry with submitted title exists (to prevent duplicates)
            
            if entry_info_check is None: # if it does not exist, then proceed (a duplicate will not be created)
                print("Title: " + title + ", Content: " + content)
                util.save_entry(title, content) # create the entry
                entry_info_markdown = util.get_entry(title)
                
                markdowner = Markdown()
                entry_info = markdowner.convert(entry_info_markdown)

                return render(request, "encyclopedia/entry.html", {
                    "entry_info": entry_info
                })
            else: # a duplicate will be created, so instead  serve an error page
                print("ERROR PAGE SERVED...")
                return render(request, "encyclopedia/entry_error.html", {
                    "title": title
                })
        else:
            return render(request, "encyclopedia/error.html") # the user should not be able to make it here as there is no authentication for invalid strings    
    else:
        return render(request, "encyclopedia/error.html") # the user should not be able to make it here as post is the only way to get to this url

