from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, OrderItem, Order, BillingAddress
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm
# Create your views here.


def items_list(request):
    items = Item.objects.all()
    return render(request, 'core/items-list.html', {'items': items})


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'core/home.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            context = {
                'object': order
            }
            return render(self.request, 'core/order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not an active order")
            return redirect('/')


class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/product.html'


class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'core/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            if form.is_valid():
                street_address = form.cleaned_data('')
                apartment_address = form.cleaned_data('')
                country = form.cleaned_data('')
                zip = form.cleaned_data('')
                # TODO: add functionality for these fields
                # same_billing_address = form.cleaned_data('')
                # save_info = form.cleaned_data('')
                # payment_option = form.cleaned_data('')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect to the selected payment option
            messages.warning(self.request, "Failed Checkout")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('core:order-summary')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered = False)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "this item quantity was updated")
            return redirect('core:order-summary')
        else:
            order.items.add(order_item)
            messages.info(request, "this item was added to your cart")
            return redirect('core:order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "this item was added to your cart")
    return redirect('core:order-summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "this item was removed from your cart")
            return redirect('core:order-summary')
        else:
            messages.info(request, "this item was not in your cart")
            return redirect('core:product', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('core:product', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "this quantity was updated")
            return redirect('core:order-summary')
        else:
            messages.info(request, "this item was not in your cart")
            return redirect('core:product', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('core:product', slug=slug)
