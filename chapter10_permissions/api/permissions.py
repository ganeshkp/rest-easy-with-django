from rest_framework import permissions
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import DjangoObjectPermissions

class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)


class IsReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            #Check permission for read-only request
            return True
        else:
            # Check permission for write request
            return obj.review_user == request.user or request.user.is_staff
        

class MultiplePermissionsRequired(permissions.BasePermission):
    """
    allows authenticated users which have permissions listed in permissions dictionary
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return self.check_permissions(request, view)
    
    def check_permissions(self, request, view):
        permissions = self.get_required_permissions(view)
        
        perms_all = permissions.get("all") or None
        perms_any = permissions.get("any") or None
        perms_get = permissions.get("get") or None
        perms_post = permissions.get("post") or None
        perms_put = permissions.get("put") or None
        perms_patch = permissions.get("patch") or None
        perms_delete = permissions.get("delete") or None
        
        #if all in permissions dict, check the user has all permissions in the tuple
        if perms_all:
            if not request.user.has_perms(perms_all):
                return False
            
        #if any in permissions dict, check the user has atleast one permissions in the tuple
        if perms_any:
            for perm in perms_any:
                if request.user.has_perm(perm):
                    return True

            return False
        
        if perms_get and request.method=="GET":
            return self._check_method_permission(request, perms_get)
                    
        if perms_post and request.method=="POST":
            return self._check_method_permission(request, perms_post)
                
        if perms_put and request.method=="PUT":
            return self._check_method_permission(request, perms_put)
                
        if perms_patch and request.method=="PATCH":
            return self._check_method_permission(request, perms_patch)
        
        if perms_delete and request.method=="DELETE":
            return self._check_method_permission(request, perms_delete)
        
        return True                
                
    def _check_method_permission(self, request, permissions):
        status=True
        for perm in permissions:
            if not request.user.has_perm(perm):
                status = False
        return status
        
    def get_required_permissions(self, view):
        self._check_permissions_attr(view)
        return view.permissions
    
    def _check_permissions_attr(self, view):
        """
        check whether permissions attribute is set and it is dict format
        """
        if not hasattr(view, "permissions") or not isinstance(view.permissions, dict):
            raise ImproperlyConfigured(f'{self.__class__.__name__} requires "permissions" attribute to be set as a dict.' )


class CustomDjangoObjectPermissions(DjangoObjectPermissions):
    """
    Custom permissions class that uses custom permissions from the model's Meta class.
    Overrides the default `perms_map` to map custom permissions based on the request method.
    """

    # Override the perms_map with your custom permissions
    perms_map = {
        'GET': ['chapter3_project_setup.can_view_watchlist'],
        'POST': ['chapter3_project_setup.can_create_watchlist'],
        'PUT': ['chapter3_project_setup.can_update_watchlist'],
        'PATCH': ['chapter3_project_setup.can_partially_update_watchlist'],
        'DELETE': ['chapter3_project_setup.can_delete_watchlist'],
    }
    
    def has_object_permission(self, request, view, obj):
        # Bypass object-level checks for 'GET' requests, only use model-level
        if request.method == 'GET':
            return request.user.has_perm('chapter3_project_setup.can_view_watchlist')
        return super().has_object_permission(request, view, obj)
