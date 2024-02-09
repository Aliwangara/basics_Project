from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from _ast import Pass
from main_app.app_forms import Employee_form
from main_app.models import Employee, Contacts
from main_app.users import people
from django.template import RequestContext


# Create your views here.
def home_page(request):
    # name = "Ali Wangara"
    # age = 18
    #
    # data = {
    #     "Name": name,
    #     "Age": age
    #
    # }
    return render(request, "index.html", )


# def data(request):
#     name = "Wangara"
#     age = 21
#     users = people
#
#     data = {
#         "name" : name,
#         "age" : age,
#         "users":people
#     }
#
#     return render(request, "data.html" , context=data)
def about(request):
    return render(request, "about.html")


@login_required
def donate(request):
    return render(request, "charity.html")


def contact(request):
    if request.method=="POST":
        fname =request.POST.get('name')
        femail = request.POST.get('email')
        fphoneno = request.POST.get('num')
        fsubj = request.POST.get('subject')
        fdescription = request.POST.get('desc')
        query = Contacts(name =fname, email=femail, number=fphoneno, subject=fsubj, details=fdescription)
        query.save()
        messages.success(request, "Thanks for contacting. I will get back to you soon!")
        return redirect('/contact')
    return render(request, "contact.html")


@login_required
@permission_required('main_app.add_employee', raise_exception=True)
def team(request):
    if request.method == "POST":
        form = Employee_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Added successfully")
            return redirect("home")

    else:
        form = Employee_form()
    return render(request, 'employee.html', {"form": form})


# All employees
# one employee


def employee(request):
    employees = Employee.objects.all()
    # employees = Employee.objects.all().order_by("-salary")
    # employees = Employee.objects.filter(name__istartswith= "Al", salary__gt = 45000).order_by("dob")
    # employees = Employee.objects.filter(Q(name__contains="Al") | Q(salary__gt = 70000))
    # today = datetime.today()
    # day = today.day
    # month = today.month
    # employees = Employee.objects.filter(dob__day=day, dob__month= month)
    paginator = Paginator(employees, 30)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    return render(request, "all_employees.html", {"employees": data})


def employee_details(request, emp_id):
    employee = Employee.objects.get(pk=emp_id)  # SELECT * FROM employees
    return render(request, 'employee_details.html', {"employee": employee})


@login_required
@permission_required('main_app.delete_employee')
def employee_delete(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)
    employee.delete()
    messages.warning(request, 'Deleted successfully')
    return redirect("all")


@login_required
@permission_required('main_app.view_employee')
def search_employees(request):
    search_word = request.GET["search_word"]
    employees = Employee.objects.filter(Q(name__icontains=search_word) | Q(email__icontains=search_word)
                                        )
    paginator = Paginator(employees, 30)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    # Elastic search
    return render(request, "all_employees.html", {"employees": data})


@login_required
@permission_required('main_app.change_employee')
def employee_update(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)  # SELECT *FROM employees WHERE id = 1
    if request.method == "POST":
        form = Employee_form(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "updated successfully")
            return redirect('details', emp_id)
    else:
        form = Employee_form(instance=employee)

    return render(request, 'update.html', {'form': form})


def signin(request):
    if request.method == "POST":
        get_email = request.POST.get('email')
        get_password = request.POST.get('pass1')
        myuser = authenticate(username=get_email, password=get_password)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")

    return render(request, 'login.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


# TODO add one to one again
def signup(request):
    if request.method == "POST":
        get_first_name = request.POST.get('first')
        get_last_name = request.POST.get('last')
        get_email = request.POST.get('email')
        get_date = request.POST.get('date')
        get_number = request.POST.get('number')
        get_address = request.POST.get('address')
        get_password = request.POST.get('pass1')
        get_confirm_password = request.POST.get('pass2')
        if get_password != get_confirm_password:
            messages.info(request, 'Password not matching')
            return redirect('/signup')

        try:
            if User.objects.get(username=get_email):
                messages.warning(request, "Email is already Taken")
                return redirect('/signup')


        except Exception as identifier:
            Pass

        myuser = User.objects.create_user(  get_email,get_email, get_password)
        myuser.save()
        messages.success(request, "user created please login")
        return redirect('signin')

    return render(request, 'Sign up.html')
