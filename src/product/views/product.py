from django.views import generic
from django.db.models import Q

from product.models import Variant, Product, ProductVariant


class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        if self.request.GET:
            if not self.request.GET.get('page'):
                data = self.request.GET
                title = data.get('title')
                variant = data.get('variant')
                pf = data.get('price_from')
                if not pf:
                    pf = 0
                pt = data.get('price_to')
                if not pt:
                    pt = 0
                date = data.get('date')
                self.request.session['title'] = title
                self.request.session['variant'] = variant
                self.request.session['pf'] = pf
                self.request.session['pt'] = pt
                self.request.session['date'] = date
                print(dict(self.request.session))
                return Product.objects.filter(
                    (Q(productvariantprice__price__gte=pf) & Q(productvariantprice__price__lte=pt)),
                    # productvariantprice__product_variant_one__variant__title=variant,
                    title=title)
            else:
                if len(dict(self.request.session)):
                    return Product.objects.filter(
                        (Q(productvariantprice__price__gte=self.request.session['pf']) &
                         Q(productvariantprice__price__lte=self.request.session['pt'])),
                        title=self.request.session['title'],
                        # productvariant__variant__title=self.request.session['variant']
                    )
                else:
                    return Product.objects.all()
        else:
            self.request.session.clear()
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = ProductVariant.objects.all().distinct()
        return context


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
