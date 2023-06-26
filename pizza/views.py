from django.shortcuts import render
from .forms import PizzaForm,MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza
# Create your views here.
def home(request):
    return render(request,'pizza/home.html')

def order(request):
    other_form=MultiplePizzaForm()
    if request.method=='POST':
        filled_data=PizzaForm(request.POST)
        if filled_data.is_valid():
            created_pizza=filled_data.save()
            created_pizza_pk=created_pizza.id
            note=f'Thaanks for ordering {filled_data.cleaned_data["size"]} sized with {filled_data.cleaned_data["topping1"]} and {filled_data.cleaned_data["topping2"]} toppings'
            new_form=PizzaForm()
            return render(request,'pizza/order.html',{'created_pizza_pk':created_pizza_pk,'PizzaForm':new_form,'note':note,'anotherform':other_form})
    else:
        form=PizzaForm()
        return render(request,'pizza/order.html',{'PizzaForm':form,'anotherform':other_form})
    
def pizzas(request):
    number_of_pizzas=2
    filled_multiple_pizza_form=MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas=filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet=formset_factory(PizzaForm,extra=number_of_pizzas)
    formset=PizzaFormSet()
    if request.method=="POST":
        filled_formset=PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note="pizzas have been ordered"
        else:
            note="Order was not created.please order again!"
        return render(request,'pizza/pizzas.html',{'note':note,'formset':formset})
    else:
        return render(request,'pizza/pizzas.html',{'formset':formset})
    
def edit_order(request,pk):
    pizza=Pizza.objects.get(pk=pk)
    form=PizzaForm(instance=pizza)
    if request.method=="POST":
        form=PizzaForm(request.POST,instance=pizza)
        if form.is_valid():
            form.save()
            note="you have edited the order"
            return render(request,'pizza/edit_order.html',{'pizzaform':form,'pizza':pizza,'note':note})

    return render(request,'pizza/edit_order.html',{'pizzaform':form,'pizza':pizza})

