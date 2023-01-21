from rest_framework.permissions import BasePermission

from api.models import Contributors, Projects


def check_contributor(user, project):
    for contributor in Contributors.objects.filter(project_id=project.id):
        if user.id == contributor.user_id:
            return True
    return False


class ContributorsPermissions(BasePermission):
    message = 'You dont have permission to do that.'

    def has_permission(self, request, view):
        if not request.user and request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, Projects.objects.filter(id=view.kwargs['projects_pk']).first())

        elif view.action in ['update', 'partial_update', 'create', 'destroy']:
            return request.user == Projects.objects.filter(id=view.kwargs['projects_pk']).first().author_user_id


class ProjectsPermissions(BasePermission):
    message = 'You dont have permissions to do that.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, obj)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author_user_id


class IssuesPermissions(BasePermission):
    message = 'You dont have permission to do that.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list', 'create']:
            return check_contributor(request.user, obj.project_id)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author_user_id


class CommentsPermissions(BasePermission):
    message = 'You dont have permission to do that.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list', 'create']:
            return check_contributor(request.user, obj.issue_id.project_id)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author_user_id
