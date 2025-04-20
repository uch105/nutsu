from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now, timedelta
from .models import *
from .payment import *
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

def generate_invoice():
    while True:
        invoice_no = generate_unique_id(prefix="INV",include_special=False)
        if not Payment.objects.filter(invoice_no=invoice_no).exists():
            return invoice_no

def generate_transactionID():
    while True:
        tran_id = generate_unique_id(prefix="TRX-",include_special=False,include_lowercase=False)
        if not Payment.objects.filter(trxID=tran_id).exists():
            return tran_id

def maintainance_view(request):
    return render(request, 'nutsu_app/maintainance.html')

def maintainance_view_all(request,path):
    return render(request, 'nutsu_app/maintainance.html')

def get_customer_info(service,username):
    if service=='consultancy':
        customer = ConsultedCustomer.objects.get(username=username)
        customer_info = {
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
        }
    return customer_info

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
        'newsletters': newsletters.order_by('-published_at'),
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

@login_required
def query_list(request):
    latest_queries = Query.objects.order_by('-id')[:10]
    return render(request, 'nutsu_app/query_list.html', {'latest_queries': latest_queries})

def load_more_queries(request):
    all_queries = list(Query.objects.order_by('-id').values())
    return JsonResponse({'queries': all_queries})

def terms_privacy(request):
    return render(request,'nutsu_app/terms_privacy.html')

def create_invoice(request):
    return render(request,"nutsu_app/create_invoice.html")

def checkout(request):
    service = request.GET.get('service','')
    username = request.GET.get('username','')
    amount = request.GET.get('amount','')
    invoice_no = generate_invoice()
    if service and username and amount:
        try:
            payment_instance = Payment.objects.create(invoice_no=invoice_no,service=Service.objects.get(name=service),username=username,amount=amount)
            context = {
                'invoice_no': invoice_no,
                'service': service,
                'username': username,
                'amount': amount,
            }
        except:
            messages.warning(request, "Sorry! The service you are going to make payment is no longer available. Please contact us for more information!")
            context = {
                'invoice_no': '',
                'service': service,
                'username': username,
                'amount': amount,
            }
    else:
        messages.warning(request, "Bad payment link! Please make sure you have typed the correct url or contact us ASAP!")
        context = {
            'invoice_no': '',
            'service': service,
            'username': username,
            'amount': amount,
        }
    return render(request, "nutsu_app/checkout.html", context)

def create_payment(request,pk0,pk1,pk2,pk3):
    service, username, amount, invoice_no = pk0, pk1, pk2, pk3

    customer_info = get_customer_info(service=service,username=username)

    tran_id = generate_transactionID()

    payment_url,sessionkey = create_get_session(tran_id=tran_id,service=service,username=username,amount=amount,name=customer_info["name"],email=customer_info["email"],phone=customer_info["phone"])

    payment_instance = Payment.objects.get(invoice_no=invoice_no)
    payment_instance.trxID = tran_id
    payment_instance.sessionkey = sessionkey
    payment_instance.save()

    return redirect(payment_url)

@csrf_exempt
def checkoutsuccess(request):
    service, username, amount, trxID = request.GET.get("service"), request.GET.get("username"), request.GET.get("amount"), request.GET.get("tran_id")
    payment_instance = Payment.objects.get(trxID=trxID)
    payment_instance.status = True
    payment_instance.save()
    customer_info = get_customer_info(service=service,username=username)
    redirection_url = Service.objects.get(name=service).redirection_url
    messages.success(request,"Payment Successful!")
    context = {
        'service': service,
        'amount': amount,
        'name': customer_info["name"],
        'redirection_url': redirection_url,
    }
    return render(request,"nutsu_main/checkoutsuccess.html",context)

@csrf_exempt
def checkoutfail(request):
    messages.error(request,"Payment Failed")
    service, username, amount, trxID = request.GET.get("service"), request.GET.get("username"), request.GET.get("amount"), request.GET.get("tran_id")
    payment_instance = Payment.objects.get(trxID=trxID)
    payment_instance.delete()
    customer_info = get_customer_info(service=service,username=username)
    logdetails = f"User {customer_info['name']} has failed the payment of {amount} BDT.\nE-mail: {customer_info['email']}\nPhone no: {customer_info['phone']}"
    BadPayment.objects.create(logdetails=logdetails)
    redirection_url = Service.objects.get(name=service).redirection_url
    context = {
        'service': service,
        'amount': amount,
        'name': customer_info["name"],
        'redirection_url': redirection_url,
    }
    return render(request,"nutsu_app/checkoutfail.html",context)

@csrf_exempt
def checkoutcancel(request):
    messages.error(request,"Payment Failed")
    service, username, amount, trxID = request.GET.get("service"), request.GET.get("username"), request.GET.get("amount"), request.GET.get("tran_id")
    payment_instance = Payment.objects.get(trxID=trxID)
    payment_instance.delete()
    customer_info = get_customer_info(service=service,username=username)
    logdetails = f"User {customer_info['name']} has cancelled the payment of {amount} BDT.\nE-mail: {customer_info['email']}\nPhone no: {customer_info['phone']}"
    BadPayment.objects.create(logdetails=logdetails)
    redirection_url = Service.objects.get(name=service).redirection_url
    context = {
        'service': service,
        'amount': amount,
        'name': customer_info["name"],
        'redirection_url': redirection_url,
    }
    return render(request,"nutsu_app/checkoutcancel.html",context)