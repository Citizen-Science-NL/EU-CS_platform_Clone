from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_summernote.widgets import SummernoteWidget
from django.forms import ModelForm
from django_select2.forms import Select2MultipleWidget
from .models import Resource, Keyword, Category, Audience, Theme, ResourceGroup, ResourcesGrouped, EducationLevel, LearningResourceType
from authors.models import Author
from PIL import Image
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _
from organisations.models import Organisation


class ResourceForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(),
        help_text=_('Insert here the title or name of the resource'))

    url = forms.CharField(widget=forms.TextInput(),\
        help_text=_('URL to where the document is hosted by the publisher, \
        or in a permanent repository such as Zenodo, OSF, the RIO Journal, or similar'))

    abstract = forms.CharField(widget=CKEditorWidget(config_name='frontpage'),\
        help_text=_('Please briefly describe the resource (ideally in 500 words or less)'), max_length = 3000)

    category = forms.ModelChoiceField(queryset=Category.objects.filter(parent__isnull=True),\
        help_text=_('Select one of the proposed categories'))
    choices = forms.CharField(widget=forms.HiddenInput(),required=False, initial=())
    categorySelected = forms.CharField(widget=forms.HiddenInput(),required=False)

    audience = forms.ModelMultipleChoiceField(queryset=Audience.objects.all(), widget=Select2MultipleWidget(),\
        help_text=_('Select the audience(s) for which the resource is intended. Multiple options can be selected'))

    keywords = forms.MultipleChoiceField(choices=(), widget=Select2MultipleWidget(),\
        help_text=_('Please write or select keywords to describe the resource, separated by commas or pressing enter'), required=False)

    theme = forms.ModelMultipleChoiceField(queryset=Theme.objects.all(), widget=Select2MultipleWidget(),\
        help_text=_('The thematic content of the resource (select as many as apply)'))


    resource_DOI = forms.CharField(max_length=100, required=False, widget=forms.TextInput(),\
        help_text=_('Please provide the Digital Object Signifier that is unique to your resource,\
        generated by the Publisher, Zenodo...'),label=_('Resource DOI'))

    authorsCollection = forms.CharField(widget=forms.HiddenInput(),required=False, initial=())
    authors = forms.MultipleChoiceField(choices=(), widget=Select2MultipleWidget(),\
        help_text=_('Author(s) of the resource. Enter <i>FirstInitial LastName</i> and close with a comma or pressing enter to add an author,\
        or multiple authors. If not known, name the project within the resource was created.'), \
        required=False,label=_("Authors"))

    license = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'nope'}),\
        help_text=_('Indicate the resource license, such as Creative Commons CC-BY.\
         Enter a URL link to the license if available.'), required=False)

    organisation = forms.ModelMultipleChoiceField(queryset=Organisation.objects.all(), widget=Select2MultipleWidget(),\
        help_text=_('Organisation(s) contributing the resource (multiple selection separated by comma or pressing enter). \
        If not listed, please add them <a href="/new_organisation">here</a > before submitting'), required=False,label=_("Organisation(s)"))

    publisher = forms.CharField(max_length=100, widget=forms.TextInput(),\
        help_text=_('The publisher of the resource (or the project name, or the lead institution).'), required=False )

    year_of_publication = forms.IntegerField(required=False, widget=forms.TextInput(),\
        help_text=_('Enter the year (YYYY) that this version of the resource was published'))



    image1 = forms.ImageField(required=False, widget=forms.FileInput)
    image_credit1 = forms.CharField(max_length=300, required=False, label=_("Image 1 credit"))
    x1 = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width1 = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    withImage1 = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=False)
    image2 = forms.ImageField(required=False, widget=forms.FileInput)
    image_credit2 = forms.CharField(max_length=300, required=False, label=_("Image 2 credit"))
    x2 = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y2 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width2 = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height2 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    withImage2 = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=False)
    curatedList = forms.ModelMultipleChoiceField(queryset=ResourceGroup.objects.all(), widget=Select2MultipleWidget, required=False,label=_("Curated lists"))


    #Training resources fields
    education_level = forms.ModelMultipleChoiceField(queryset=EducationLevel.objects.all(),\
        widget=Select2MultipleWidget(), required=False, label=_("Education level"),\
        help_text= _('Insert education level needed, end using comma or pressing enter'))
    educationLevelSelected = forms.CharField(widget=forms.HiddenInput(), max_length=100, required=False)
    learning_resource_type =forms.ModelMultipleChoiceField(queryset=LearningResourceType.objects.all(),\
        widget=Select2MultipleWidget(),\
        required=False, label=_("Learning resource type"),
        help_text=_('Help text here'))
    learningResourceTypeSelected = forms.CharField(widget=forms.HiddenInput(), max_length=100, required=False)
    time_required = forms.FloatField(required=False,help_text=_('Aproximate hours required to finish the training'))
    conditions_of_access = forms.CharField(required=False, help_text=_('Help text here'))

    class Meta:
        model = Resource
        fields = ["name", "abstract", "url", "audience", "theme","keywords", "license", "publisher", "curatedList",
         "category", "authors", "image1", "x1", "y1", "width1", "height1", "resource_DOI", "year_of_publication", 'image_credit1', 'image_credit2']

    def save(self, args, images):
        pk = self.data.get('resourceID', '')
        publication_date = datetime.now()
        rsc = super(ResourceForm, self).save(commit=False)
        category = get_object_or_404(Category, id=self.data['categorySelected'])

        if pk:
            rsc = get_object_or_404(Resource, id=pk)
            if rsc.hidden:
                rsc.hidden = False
            rsc.name = self.data['name']
            rsc.abstract = self.data['abstract']
            rsc.url = self.data['url']
            rsc.license = self.data['license']
            rsc.publisher = self.data['publisher']
            rsc.dateLastModification = datetime.now()
        else:
            rsc.dateUploaded = publication_date
            rsc.creator = args.user

        rsc.inLanguage = self.data['language']
        rsc.resourceDOI = self.data['resource_DOI']
        if self.data['year_of_publication'] != '':
            rsc.datePublished = self.data['year_of_publication']
        else:
            rsc.datePublished = None
        rsc.category = category

        if(images[0] != '/'):
            rsc.image1 = images[0]
        if(images[1] != '/'):
            rsc.image2 = images[1]

        rsc.imageCredit1 = self.data['image_credit1']
        rsc.imageCredit2 = self.data['image_credit2']

        #Training resource fields
        isTrainingResource = self.data.get('trainingResource', False)
        if(isTrainingResource):
            rsc.isTrainingResource = True
            educationLevelSelected = self.data['educationLevelSelected']
            if(educationLevelSelected != ''):
                educationLevel, exist = EducationLevel.objects.get_or_create(educationLevel=educationLevelSelected)
                rsc.educationLevel = educationLevel
            learningResourceTypeSelected = self.data['learningResourceTypeSelected']
            if(learningResourceTypeSelected != ''):
                learning_resource_type, exist = LearningResourceType.objects.get_or_create(learningResourceType=learningResourceTypeSelected)
                rsc.learningResourceType = learning_resource_type
            if(self.data['time_required']!=''):
                rsc.timeRequired = self.data['time_required']
            rsc.conditionsOfAccess = self.data['conditions_of_access']
        #End training resource fields

        rsc.save()

        rsc.audience.set(self.data.getlist('audience'))
        rsc.theme.set(self.data.getlist('theme'))
        rsc.organisation.set(self.data.getlist('organisation'))

        curatedList = self.data.getlist('curatedList')

        if args.user.is_staff:
            objs = ResourcesGrouped.objects.filter(resource=rsc)
            if objs:
                for obj in objs:
                    obj.delete()
            for clist in curatedList:
                rscGroup = get_object_or_404(ResourceGroup, id=clist)
                ResourcesGrouped.objects.get_or_create(group=rscGroup,resource=rsc)

        # Keywords
        choices = self.data['choices']
        choices = choices.split(',')
        for choice in choices:
            if(choice != ''):
                keyword = Keyword.objects.get_or_create(keyword=choice)
        keywords = Keyword.objects.all()
        keywords = keywords.filter(keyword__in = choices)
        rsc.keywords.set(keywords)

        # Authors
        authors = self.data['authorsCollection']
        authors = authors.split(',')
        for author in authors:
            if(author != ''):
                Author.objects.get_or_create(author=author)
        authorsCollection = Author.objects.all()
        authors = authorsCollection.filter(author__in = authors)
        rsc.authors.set(authors)

        return 'success'


class ResourcePermissionForm(forms.Form):
    selectedUsers = forms.CharField(widget=forms.HiddenInput(),required=False, initial=())
    usersCollection = forms.CharField(widget=forms.HiddenInput(),required=False, initial=())
    usersAllowed =   forms.MultipleChoiceField(choices=(), widget=Select2MultipleWidget, required=False, label=_("Give additional users permission to edit"))
