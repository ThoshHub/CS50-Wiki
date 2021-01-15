from django.shortcuts import render

from . import util
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    # Get the 
    entry_info_markdown = util.get_entry(entry)

    if entry_info_markdown is None:
        return render(request, "encyclopedia/error.html")
    else:
        markdowner = Markdown()
        entry_info = markdowner.convert(entry_info_markdown)
        # print("Title: " + entry) # DEBUG
        # print("Info: " + entry_info) # DEBUG

        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry, "entry_info": entry_info
        })

def search(request):
    if request.method == "POST":
        search_term = str(request.POST.get('q', None))
        # print("Searched for: " + search_term)
        entry_list = util.list_entries()
        results = [entry for entry in entry_list if search_term.upper() in entry.upper()]

        print(str(results))
        return render(request, "encyclopedia/search.html", {
            "results": results, "query": search_term
        })
    else:
        return render(request, "encyclopedia/error.html") # the user should not be able to make it here as post is the only way to get to this url