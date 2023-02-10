from django.contrib import admin
from .models import Question, Choice


# set order for the fields in admin form
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']


# with this, we will have inline form for "Choice" model inside "Question" model
# we need to set this inside QuestionAdmin as well, which is inlines = [ChoiceInline]
# we can set ChoiceInline(admin.StackedInline) as well, it will show another type of inline form
class ChoiceInline(admin.TabularInline):
    model = Choice
    # extra = 3 will show 3 extra choice inside question form
    # ex:
    # if we create new question, we will see 3 choice.
    # but if question 1 already have 2 choice, and we go to the detail question page
    # we will see 2 + 3 = 5 choice.
    extra = 3


# cover fields inside fieldsets in admin form
# with this, when you come to the admin form,
# you will see that field pub_date is covered by fieldset with text "Date information"
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    # with this, we will have inline form for "Choice" model inside "Question" model
    inlines = [ChoiceInline]
    # set column display in the list in admin panel
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # show a sort filter in admin panel
    list_filter = ['pub_date']
    # show a search field in admin panel
    search_fields = ['question_text']


# add the Question model to the admin page
# which will allow you to CRUD it on the admin panel
admin.site.register(Question, QuestionAdmin)


# add the Choice model to the admin page
# which will allow you to CRUD it on the admin panel
admin.site.register(Choice)


