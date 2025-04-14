from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from .models import *
import random
import string

def generate_unique_id(prefix="id_", length=16, include_uppercase=True, include_lowercase=True, include_numbers=True, include_special=True):
    if length <= len(prefix):
        raise ValueError("Length must be greater than prefix length.")

    characters = ""

    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character set must be included.")

    remaining_length = length - len(prefix)
    random_part = ''.join(random.choice(characters) for _ in range(remaining_length))

    return prefix + random_part

def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        text = request.POST.get("text")

        Query.objects.create(name=name, email=email, text=text)
        messages.success(request, "Query received, we will contact soon!")
        return redirect("home")


    return render(request,"nutsu_app/index.html")

def projects(request):
    return render(request,"nutsu_app/projects.html")

def newsletter(request):
    query = request.GET.get('search_text','')
    newsletters = Newsletter.objects.all()
    categories = Category.objects.all()

    if query:
        newsletters = newsletters.filter(title__icontains=query)

    if request.method == "POST":
        selected_filters = request.POST.getlist("search_news")

        if "last_week" in selected_filters:
            last_week = now() - timedelta(days=7)
            newsletters = newsletters.filter(published_at__gte=last_week)

        if "last_month" in selected_filters:
            last_month = now() - timedelta(days=30)
            newsletters = newsletters.filter(published_at__gte=last_month)

        category_names = [name for name in selected_filters if name not in ["last_week", "last_month"]]
        if category_names:
            newsletters = newsletters.filter(categories__name__in=category_names).distinct()
        
        context = {
            'newsletters': newsletters,
            'categories': categories,
        }
        return render(request,"nutsu_app/newsletter.html",context)

    context = {
        'newsletters': newsletters,
        'categories': categories,
    }
    return render(request,"nutsu_app/newsletter.html",context)

def news(request,pk):
    newsletter = Newsletter.objects.get(id=pk)
    context = {
        'news': newsletter,
    }
    return render(request,"nutsu_app/news.html",context)

def about(request):
    return render(request,"nutsu_app/about.html")

@login_required
def create_newsletter(request):
    if request.method == "POST":
        id = generate_unique_id(prefix="newsletter_",include_special=False)
        title = request.POST.get("title",'')
        description = request.POST.get("description",'')
        categories = request.POST.get("categories",'')
        author_name = request.POST.get("authors",'')
        banner = request.FILES["banner"]
        read_time = request.POST.get("read_time",'')

        newsletter = Newsletter.objects.create(id=id,title=title,description=description,author=Author.objects.get(user=User.objects.get(id=author_name)),banner=banner,read_time=read_time)
        newsletter.categories.set(Category.objects.filter(name__in=categories))
        return redirect("create_newsletter")
    categories = Category.objects.all()
    authors = Author.objects.all()

    context = {
        'categories':categories,
        'authors':authors,
    }
    return render(request,"nutsu_app/create_newsletter.html",context)

@login_required
def create_newsletter_block(request):
    if request.method == "POST":
        id = request.POST.get("id",'')
        description = request.POST.get("description",'')

        try:
            image = request.FILES['image']
            image_source = request.POST.get("image_source",'')
            NewsletterBlock.objects.create(parent=Newsletter.objects.get(id=id),text=description,image=image,image_source_text=image_source)
        except:
             NewsletterBlock.objects.create(parent=Newsletter.objects.get(id=id),text=description)

    return render(request,"nutsu_app/create_newsletter_block.html")

def query_list(request):
    latest_queries = Query.objects.order_by('-id')[:10]
    return render(request, 'nutsu_app/query_list.html', {'latest_queries': latest_queries})

def load_more_queries(request):
    all_queries = list(Query.objects.order_by('-id').values())
    return JsonResponse({'queries': all_queries})