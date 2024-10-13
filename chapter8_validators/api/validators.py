from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

       
def validate_watchlist_title(value):
    if len(value)<5 or len(value)>30:
        raise ValidationError("Movie title shall be meaningful")    

def validate_watchlist_type(attrs):
    try:
        if attrs["category"]=="MOVIE" and attrs["episodes"]>0:
            raise ValidationError("Movie cannot have episodes")
        
        if attrs["category"]=="SERIES" and attrs["episodes"]==0:
            raise ValidationError("Series shall have number of episodes")
    except Exception as e:
        raise ValidationError(f"{str(e)} field is missing.")

class RequiredTogetherValidator(object):
    
    message = _("The fields {field_names} are required together.")
    missing_message = _("This field is required.")
    requires_context = True
    
    def __init__(self, fields, message=None, missing_message=None):
        self.fields = fields
        self.message = message or self.message
        self.missing_message = missing_message or self.missing_message
        
    def enforce_required_fields(self, attrs):
        raise NotImplementedError

    def __call__(self, attrs, serializer):
        self.instance = getattr(serializer, "instance", None)
        self.enforce_required_fields(attrs)
        
class CreateRequiredTogetherValidator(RequiredTogetherValidator):
    def enforce_required_fields(self, attrs):
        filled = 0
        
        number_of_fields = len(self.fields)
        fields_filled = []
        if self.instance is not None:
            for field_name in self.fields:
                try:
                    if attrs[field_name]:
                        filled +=1
                        fields_filled.append(field_name)
                except:
                    pass
        
        missing_items = {
            field_name: self.missing_message
            for field_name in self.fields
            if filled > 0
            and filled > number_of_fields
            and field_name not in fields_filled
        }
        
        if missing_items:
            raise ValidationError(missing_items, code="required")
      
        
    