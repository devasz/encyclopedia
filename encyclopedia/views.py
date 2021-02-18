import markdown2
import random
from django.shortcuts import redirect, render
from django.urls import reverse
from . import util
from encyclopedia.forms import NewEntryForm, EditEntryForm
from django.contrib import messages
from django.http.response import HttpResponseRedirect


def index(request):
    entries = util.list_entries()
    entry = util.get_entry(request.GET.get("q"))

    if entry is not None:
        return HttpResponseRedirect("/wiki/" + request.GET.get("q"))
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })


def new(request):
    entries = util.list_entries()

    if request.method == "POST":
        form = NewEntryForm(request.POST or None)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            content = content.replace('\r', '')
            md = markdown2.markdown(content)
            md = md.replace('\r', '')
            if title in entries:
                messages.info(
                    request, 'ERROR: A file with this title already exists.')
                return redirect('encyclopedia:new')
            else:
                util.save_entry(title, content)
                return redirect('encyclopedia:entry', title=title)
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })


def edit(request, title=None):
    if request.method == "POST":
        form = EditEntryForm(request.POST or None)
        if not title:
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                content = content.replace('\r', '')
            else:
                return render(request, "encyclopedia/edit.html", {
                    "form": form
                })
        elif title == form.data['title']:
            title = form.data['title']
            content = form.data['content']
            content = content.replace('\r', '')
            util.save_entry(title, content)
        return HttpResponseRedirect(reverse('encyclopedia:entry', args=[title]))
    if not title:
        return render(request, "encyclopedia/edit.html", {
            "form": EditEntryForm()
        })
    data = {'title': title, 'content': util.get_entry(title)}
    populated_form = EditEntryForm(initial=data)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": populated_form,
        # "edit": True
    })


def entry(request, title):
    entry = util.get_entry(title)

    try:
        title = title
        md_content = entry
        output = markdown2.markdown(md_content, extras=['fenced-code-blocks'])
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": output
        })

    except TypeError:
        error = "ERROR: Page was not found."
        return render(request, "encyclopedia/error.html", {
            "error": error
        })


def search(request):
    search_input = request.GET['q'].strip()
    entries = util.list_entries()
    results = []
    entry2 = []

    if request.method == "GET":  # and search_input:
        if search_input in entries:
            return HttpResponseRedirect("/wiki/" + request.GET.get("q"))
        else:
            for entry in entries:
                if search_input in entry:
                    results.append(entry)
                    return render(request, "encyclopedia/search.html", {
                        "results": results
                    })
            else:
                error = "ERROR: Page was not found."
                return render(request, "encyclopedia/error.html", {
                    "error": error})
    else:
        return redirect('encyclopedia:index')


def randompage(request):
    entries = util.list_entries()
    rand = random.choice(entries)
    # NOTE
    # if rand = random.choice(entries) ==> Python
    # if rand = random.choices(entries) ==> ['Python']
    return render(request, "encyclopedia/randompage.html", {
        "entries": rand,
    })
