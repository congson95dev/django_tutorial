from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


"""
Manager for TaggedItem Model

With this, we can custom the function inside "objects" of TaggedItem model
As in this example, we've add a new function called get_tags_for()
And we can use it like TaggedItem.objects.get_tags_for()
"""


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        # this query will search in table "django_content_type" for the value of table `obj_type`
        # for example, we'll search for table "product"
        content_type = ContentType.objects.get_for_model(obj_type)

        # get list of tags by product
        # for filter(content_type=content_type, object_id=1),
        # we'll need to transfer 2 params: content_type and object_id
        # content_type is for "product" table
        # object_id is for "product.id"
        return TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=obj_id)


class Tag(models.Model):
    label = models.CharField(max_length=255)


"""
Set TaggedItem as Re-use-able
We can do that by set this model as Generic Relationship
"""


class TaggedItem(models.Model):
    # to use TaggedItemManager(), we need to rewrite objects variable
    objects = TaggedItemManager()

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # handle "generic relationship"
    # we can simple call product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # but we don't want this app to have any depend on the "store" app
    # so we need to use "generic relationship"
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
