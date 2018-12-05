from django import forms
from .models import (
    word,
    meaning,
    example,
)



class WordCreateForm(forms.ModelForm):
    CHOICES = (
        ('.n', 'Noun'),
        ('.v', 'Verb'),
        ('.adj', 'Adjective'),
        ('.adv', 'Adverb')
    )

    CHOICES_2 = (
        ('formal', 'Formal'),
        ('informal', 'Informal'),
        ('spoken', 'Spoken'),
        ('academic', 'Academic'),
        ('polite', 'Polite'),
        ('impolite', 'Impolite'),
        (None, 'None of the above')
    )
    mood = forms.ChoiceField(choices = CHOICES, required = True, widget = forms.RadioSelect)
    note = forms.ChoiceField(choices=CHOICES_2, widget=forms.RadioSelect, required = False)
    class Meta:
        model = word
        fields = ['spell', 'mood', 'note']
    
    def clean(self):
        spell = self.cleaned_data.get('spell')
        mood = self.cleaned_data.get('mood')
        qs = word.objects.filter(spell__exact = spell, mood__exact = mood)
        if qs.exists():
            raise forms.ValidationError("This word already exists")
        qs = word.objects.filter(spell__exact=spell.capitalize(), mood__exact=mood)
        if qs.exists():
            raise forms.ValidationError("This word already exists")
        xs = [39, 59, 46, 44, 32] + [y for y in range(97, 123)] + [y for y in range(65, 91)]
        for char in spell:
            if not ord(char) in xs:
                raise forms.ValidationError("spell cannot contain " + str(char))
        return self.cleaned_data


class WordEditForm(forms.ModelForm):
    CHOICES = (
        ('.n', 'Noun'),
        ('.v', 'Verb'),
        ('.adj', 'Adjective'),
        ('.adv', 'Adverb')
    )

    CHOICES_2 = (
        ('formal', 'Formal'),
        ('informal', 'Informal'),
        ('spoken', 'Spoken'),
        ('academic', 'Academic'),
        ('polite', 'Polite'),
        ('impolite', 'Impolite'),
        (None, 'None of the above')
    )
    mood = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect)
    note = forms.ChoiceField(choices=CHOICES_2, widget=forms.RadioSelect, required=False)
    id = forms.IntegerField(widget = forms.HiddenInput) #since it's being called from an update view, the id will be filled itself and is hidden so that i can get it from the cleaned data
    class Meta:
        model = word
        fields = ['id', 'spell', 'mood', 'note']
    def clean(self):
        id = self.cleaned_data.get('id')
        spell = self.cleaned_data.get('spell')
        mood = self.cleaned_data.get('mood')
        qs = word.objects.filter(spell__exact=spell, mood__exact=mood)
        if qs.exists() and qs.first().id != id:
            raise forms.ValidationError("This word already exists")
        qs = word.objects.filter(spell__exact=spell.capitalize(), mood__exact=mood)
        if qs.exists() and qs.first().id != id:
            raise forms.ValidationError("This word already exists")
        xs = [39, 59, 46, 44, 32] + [y for y in range(97, 123)] + [y for y in range(65, 91)]
        for char in spell:
            if not ord(char) in xs:
                raise forms.ValidationError("spell cannot contain " + str(char))
        return self.cleaned_data


class MeaningCreateForm(forms.ModelForm):
    syn = forms.CharField(max_length=30, required = False)
    opp = forms.CharField(max_length=30, required=False)
    class Meta:
        model = meaning
        fields = ['meaning', 'syn', 'opp']


    def clean(self):
        slug = self.data.get('hidden') #we did't use the cleaned data cause hidden variable is not mentioned in the form and is a variable passed by the html. check out the html code
        text = self.cleaned_data.get('meaning')
        instance = word.objects.get(slug=slug)
        lst = instance.meanings.all()
        for element in lst:
            if element.meaning.capitalize() == text.capitalize():
                raise forms.ValidationError("This meaning already exists")
        xs = [39, 59, 46, 44, 32, 10, 13] + [y for y in range(97, 123)] + [y for y in range(65, 91)]
        for char in text:
            if not ord(char) in xs:
                raise forms.ValidationError("Meaning cannot contain "+ str(char))
        if self.cleaned_data.get('opp') == '':
            self.cleaned_data['opp'] = None
        if self.cleaned_data.get('syn') == '':
            self.cleaned_data['syn'] = None
        return self.cleaned_data


class SelectMeaningForm(forms.ModelForm):
    class Meta:
        model = word
        fields = ['meanings']
        widgets = {
            'meanings': forms.RadioSelect()
        }


    def __init__(self, instance = None, *args, **kwargs):
        super(SelectMeaningForm, self).__init__(*args, **kwargs)
        #print(kwargs)
        #the name insatnce must be the name of the key containing the value in the dict that view is passing the form(in this case is instance and is provided by update view)
        if instance:
            self.fields['meanings'].queryset = meaning.objects.filter(parent__exact = instance) #instance.meanings.all() (this could also be correct for the case we did not have the parent field)
            #to narrow down the meanings to the ones belonging to that word
            self.fields['meanings'].widget.attrs = {'required':'True'}




class AddExamleForm(forms.ModelForm):
    class Meta:
        model = example
        fields = ['exp']


    def clean(self):
        pk = self.data.get('hidden')
        instance = meaning.objects.get(id=pk)
        text = self.cleaned_data.get('exp')
        for element in instance.examples.all():
            if element.exp.capitalize() == text.capitalize():
                raise forms.ValidationError('This Example Already Exists')
        xs = [39, 59, 46, 44, 32, 10, 13] + [y for y in range(97, 123)] + [y for y in range(65, 91)]
        for char in text:
            if not ord(char) in xs:
                raise forms.ValidationError("Meaning cannot contain " + str(char))
        return self.cleaned_data               


class EditMeaningForm(MeaningCreateForm):

    def clean(self):
        # we did't use the cleaned data cause hidden variable is not mentioned in the form and is a variable passed by the html. check out the html code
        slug = self.data.get('hidden')
        text = self.cleaned_data.get('meaning')
        instance = word.objects.get(slug=slug)
        lst = instance.meanings.all()
        for element in lst:
            if element.meaning == text:
                raise forms.ValidationError("This meaning already exists")
        xs = [39, 59, 46, 44, 32, 10, 13] + \
            [y for y in range(97, 123)] + [y for y in range(65, 91)]
        for char in text:
            if not ord(char) in xs:
                raise forms.ValidationError(
                    "Meaning cannot contain " + str(char))
        if self.cleaned_data.get('opp') == '':
            self.cleaned_data['opp'] = None
        if self.cleaned_data.get('syn') == '':
            self.cleaned_data['syn'] = None
        return self.cleaned_data
