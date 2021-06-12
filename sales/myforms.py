from sales import models
from django import forms

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field_name, field in self.fields.items():
            # print(type(field))
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field,MultiSelectFormField):
                field.widget.attrs.update({'class':'form-control'})
        #     for filed in self.fields.values():
        #         filed.widget.attrs.update({'class': 'form-control'})