from django.contrib.contenttypes.models import ContentType
from django.db import transaction, connection
from django.db.models import Q, F, Count, Max, Min, Avg, Sum, Value, Func, ExpressionWrapper, DecimalField
from django.http import HttpResponse
from django.shortcuts import render

from store.models import Product, OrderItem, Order, Category, Customer
from tags.models import TaggedItem


def learn_get_query(request):
    """
    Filter

    about params inside function filter(), you can find it in here:
    https://docs.djangoproject.com/en/4.1/ref/models/querysets/
    search for "Field lookups" section
    """

    # gt, gte, lt, lte, it's short for greater than, greater than or equal, lower than, lower than or equal
    queryset = Product.objects.filter(unit_price__gt=20)

    # range
    queryset = Product.objects.filter(unit_price__range=(20, 30))

    # filter by category_id in range
    queryset = Product.objects.filter(category__id__in=(8, 9, 10))

    # get product by title, using "contains", which will render query "LIKE %Some String%"
    # we could also use "icontains", which will render query "ILIKE %Some String%"
    # with "contains", we can not search by uppercase and lowercase, but by exact same string
    # opposide of that, we have "icontains", which support us to search by both uppercase and lowercase
    queryset = Product.objects.filter(title__contains="Some String")

    # filter title = null
    queryset = Product.objects.filter(title__isnull=True)

    # filter AND
    queryset = Product.objects.filter(unit_price__lt=20, inventory__lt=30)

    # filter OR
    # in django, when we try to do filter OR or filter NOT, we need to use "Q" filter of django
    queryset = Product.objects.filter(Q(unit_price__lt=20) | Q(inventory__lt=30))

    # filter NOT
    # in django, when we try to do filter OR or filter NOT, we need to use "Q" filter of django
    queryset = Product.objects.filter(~Q(unit_price__lt=20))

    # to compare between 2 column of table, we need to use "F" filter of django
    # so in the sql query, it will render something like:
    # "WHERE 'store_product'.'unit_price' = 'store_product'.'inventory'"
    queryset = Product.objects.filter(unit_price=F('inventory'))

    """
    Order by
    """

    # asc
    queryset = Product.objects.order_by('title')

    # desc
    queryset = Product.objects.order_by('-title')
    # or you can use
    queryset = Product.objects.order_by('title').reverse()

    """
    Get first or get last item
    """

    # get first product
    # this will render query:
    # SELECT ••• FROM "store_product" ORDER BY "store_product"."id" DESC LIMIT 1
    product = Product.objects.earliest('id')

    # get last product
    # this will render query:
    # SELECT ••• FROM "store_product" ORDER BY "store_product"."id" ASC LIMIT 1
    product = Product.objects.latest('id')

    """
    Render the result by using values() and values_list()
    """

    # get records from 5 to 10
    queryset = Product.objects.all()[5:10]

    # get specific columns
    # with values(), it return a {key: value} format
    queryset = Product.objects.values('id', 'title', 'category__title')
    # with values_list(), it return only (value) format
    queryset = Product.objects.values_list('id', 'title', 'category__title')

    """
    Join with related table using select_related() and prefetch_related()
    """

    # With the bad example, django will run a lot of query to get product.category.title
    # It's because we didn't fetch the "category" first
    # That's not good
    # Instead, we should use select_related() or prefetch_related() to fetch the "category" before we called it
    # Same thing happen with the 2nd bad example below, which try to access many to many relationship

    # Bad example:
    # fetch 1 to many relationship by normal method
    # With this non-prefetch call, it will create tons of query and will slow the page
    # queryset = Product.objects.all()
    # for product in queryset:
    #     result = product.category.title

    # Good example:
    # use select_related() to fetch the "category" so we can use later
    # with this, it just run 1 single query
    # Note: the select_related() method only work for 1 to 1, 1 to many relationship,
    # it doesn't work with many to 1, many to many
    queryset = Product.objects.select_related('category')
    for product in queryset:
        result = product.category.title

    # Bad example:
    # fetch many to many relationship by normal method
    # With this non-prefetch call, it will create tons of query and will slow the page
    # queryset = Product.objects.all()
    # for product in queryset:
    #     for promotion in product.promotion.all():
    #         promotion_description = promotion.description

    # Good example:
    # fetch many to many relationship by prefetch_related() method
    # with this, it just run 1 single query
    # Note: the prefetch_related() method only work for many to 1, many to many relationship,
    # it doesn't work for 1 to 1, 1 to many
    queryset = Product.objects.prefetch_related('promotion').all()
    for product in queryset:
        for promotion in product.promotion.all():
            promotion_description = promotion.description

    """
    Aggregate
    
    This aggregate provided us some common function that we can use
    Such as count, max, min, avg, sum
    """

    # we could define a name, or it will automatically created name for us
    count = Product.objects.aggregate(Count('id'))
    count = Product.objects.aggregate(count=Count('id'))

    # same as above
    max = Product.objects.aggregate(max=Max('unit_price'))
    min = Product.objects.aggregate(min=Min('unit_price'))
    avg = Product.objects.aggregate(avg=Avg('unit_price'))
    sum = Product.objects.aggregate(sum=Sum('unit_price'))

    """
    Annotate
    
    This function allow us to create another dummy column in the result of table
    
    for value of annotate(), we can use 5 function below as variable:
    "Value": to transfer some simple value, such as True/False, string, number
    "F": to transfer column name of a table
    "Aggregate": to use aggregate function
    "Func": to use SQL function
    "ExpressionWrapper": to handle case between decimal and float
    """

    # use "Value"
    queryset = Product.objects.annotate(is_new=Value(True))
    queryset = Product.objects.annotate(some_string=Value("some_string"))
    queryset = Product.objects.annotate(Pi=Value(3.14))

    # use "F"
    queryset = Product.objects.annotate(next_id=F("id") + 1)

    # use "Aggregate"
    queryset = Category.objects.annotate(product_count=Count('product'))
    queryset = Category.objects.annotate(product_min_price=Min('product__unit_price'))

    # use "Func"
    # This will not work with db sqlite, because CONCAT doesn't exists in sqlite, they use "||" instead
    # But this gonna work in other db such as postgresql or mysql
    # queryset = Customer.objects.annotate(fullname=Func(F('firstname'), Value(' '), F('lastname'), function='CONCAT'))

    # use "ExpressionWrapper"
    # normally, when we transfer "F('unit_price') * 0.8" as a new column in annotate()
    # it will throw error, because it doesn't allow us to combine decimal field with float field
    # to avoid that, we will use ExpressionWrapper to combine them
    # about the output_field=DecimalField(), we should always use that when combine decimal and float field
    discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    queryset = Product.objects.annotate(discounted_price=discounted_price)

    """
    Get "Content Type" Value From "Generic Relationship"
    
    In "tags" module, we've already set TaggedItem as Content Type in tags/models.py
    which will allow us to re-use "tags" module in not just "store" module, but can also use in other module as well
    In this example, 1 product will have multiple tags
    So how to get list of tags related to that product?
    Lets follow this instruction
    """

    # First way:
    # In this 1st way, we will do by write code directly in store module

    # get content type of "product" table
    # this query will search in table "django_content_type" for the value of table "product"
    content_type = ContentType.objects.get_for_model(Product)

    # get list of tags by product
    # for filter(content_type=content_type, object_id=1),
    # we'll need to transfer 2 params: content_type and object_id
    # content_type is for "product" table
    # object_id is for "product.id"
    queryset = TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=1)

    for taggeditem in queryset:
        tag_label = taggeditem.tag.label

    # Second way:
    # In this 2nd way, we will do by write code in tags module
    # It might look like it's shorter the code, but actually, it's the same
    # We just move all the previous code from store module to tags module
    # But if tags is called in other place as well,
    # then this 2nd way is gonna be better because it can help us to re-use the code

    # for this 2nd way, please check code in tags/models.py

    queryset = TaggedItem.objects.get_tags_for(Product, 1)

    for taggeditem in queryset:
        tag_label = taggeditem.tag.label

    """
    Render the result
    """

    # convert from queryset to list so it easier to read
    list_queryset = list(queryset)

    print(queryset)
    print(list_queryset)

    return render(request, "index.html")


def learn_create_update_delete_query(request):
    """
    Sample of create a record in "category" table
    """
    category = Category()
    category.title = "New Cat"
    category.featured_product = Product(pk=10)
    # category.save()

    """
    Sample of update a record in "category" table
    """
    category = Category.objects.get(pk=14)
    category.featured_product = Product(pk=11)
    # category.save()

    """
    Sample of delete a record or multiple records in "category" table
    """

    # delete 1
    category = Category.objects.get(pk=15)
    # category.delete()

    # delete multiple
    category = Category.objects.filter(id__gt=15)
    # category.delete()

    """
    Transaction
    
    With this, if anything happen, it will automatic rollback for us
    """
    with transaction.atomic():
        order = Order()
        order.customer = Customer(pk=1)
        order.save()

        order_item = OrderItem()
        order_item.order = order
        # there's no product with id = -1
        # so in here, it will throw an error and transaction will rollback the previous create "order" action
        order_item.product = Product(pk=-1)
        order_item.quantity = 1
        order_item.unit_price = 1
        # order_item.save()

    """
    Raw SQL
    """

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_product')

    return render(request, "index.html")


""" Exercise """


def show_product_ordered(request):
    """ Get product list that has been ordered, then sort by title """

    queryset = OrderItem.objects\
        .values('product__title', 'product__category__title')\
        .order_by('product__title').distinct()

    return render(request, "index.html")


def get_last_5_ordered(request):
    """
    Get last 5 order with their customer info and items info

    This is example for how to use select_related() and prefetch_related() method
    """

    # take a look at prefetch_related('orderitem_set__product')
    # in here, "orderitem_set" is automatic name django created for relationship between "orderitem" and "order" table
    # so we can simply use prefetch_related('orderitem_set') is enough to prefetch the "orderitem" table
    # but in this case, we need to fetch the "product" too, because we need to get product.title,
    # and the "product" is inside "orderitem" table
    # so we will use prefetch_related('orderitem_set__product') to fetch "product" table as well.
    # after that, we can get product.title without getting any extra query
    queryset = Order.objects.order_by('-id')[:5].select_related('customer').prefetch_related('orderitem_set__product')
    for order in queryset:
        # get customer.firstname and customer.lastname without getting any extra query
        customer_title = order.customer.firstname + ' ' + order.customer.lastname

        # get product.title without getting any extra query
        for orderitem in order.orderitem_set.all():
            product_title = orderitem.product.title

    return render(request, "index.html")
