from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.mixins import GetDetailSerializerClassMixin
from api.models import Contributors, Projects, Issues, Comments
from api.permissions import ProjectsPermissions, IssuesPermissions, CommentsPermissions, ContributorsPermissions
from api.serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer, \
    UserSignupSerializer, ProjectsDetailsSerializer, UserSerializer, IssuesDetailsSerializer

User = get_user_model()


class SignupViewset(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectsAdminViewset(ModelViewSet):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()


class ContributorsViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [ContributorsPermissions, IsAuthenticated]

    def get_queryset(self):
        contributors_id = [contributor.user_id for contributor in
                           Contributors.objects.filter(project_id=self.kwargs['projects_pk'])]
        return User.objects.filter(id__in=contributors_id)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            user_to_add = User.objects.filter(email=request.data['email']).first()
            if user_to_add:
                contributor = Contributors.objects.create(
                    user_id=user_to_add.id,
                    project_id=Projects.objects.filter(id=self.kwargs['projects_pk']).first().id
                )
                contributor.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(data={'error': 'User does not exist !'})
        except IntegrityError:
            return Response(data={'error': 'User already added !'})

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        user_to_delete = User.objects.filter(id=self.kwargs['pk']).first()
        if user_to_delete == request.user:
            return Response(data={'error': 'You cannot delete yourself !'})
        if user_to_delete:
            contributor = Contributors.objects.filter(user_id=self.kwargs['pk'],
                                                      project_id=self.kwargs['projects_pk']).first()
            if contributor:
                contributor.delete()
                return Response()
            return Response(data={'error': 'Contributor not assigned to project !'})
        else:
            return Response(data={'error': 'User does not exist !'})


class ProjectsViewset(GetDetailSerializerClassMixin, ModelViewSet):
    serializer_class = ProjectsSerializer
    detail_serializer_class = ProjectsDetailsSerializer

    permission_classes = [ProjectsPermissions]

    def get_queryset(self):
        id_projects = [contributor.project_id for contributor in
                       Contributors.objects.filter(user_id=self.request.user.id).all()]
        return Projects.objects.filter(author_user_id__in=id_projects)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.POST._mutable = False
        project = super(ProjectsViewset, self).create(request, *args, **kwargs)
        contributor = Contributors.objects.create(
            user_id=request.user.id,
            project_id=Projects.objects.filter(id=project.data['id']).first().id
        )
        contributor.save()
        return Response(project.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectsViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(ProjectsViewset, self).destroy(request, *args, **kwargs)


class IssuesViewset(ModelViewSet):
    serializer_class = IssuesSerializer
    detail_serializer_class = IssuesDetailsSerializer

    permission_classes = [IssuesPermissions]

    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs['projects_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        if not request.data['assignee_user_id']:
            request.data["assignee_user_id"] = request.user.pk
        request.data["project_id"] = self.kwargs['projects_pk']
        request.POST._mutable = False
        return super(IssuesViewset, self).create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        if not request.data['assignee_user_id']:
            request.data["assignee_user_id"] = request.user.pk
        request.data["project_id"] = self.kwargs['projects_pk']
        request.POST._mutable = False
        return super(IssuesViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(IssuesViewset, self).destroy(request, *args, **kwargs)


class CommentsViewset(ModelViewSet):
    permission_classes = [CommentsPermissions]

    serializer_class = CommentsSerializer
    detail_serializer_class = CommentsSerializer

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs['issues_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author_user_id'] = request.user.pk
        request.data['issue_id'] = self.kwargs['issues_pk']
        request.POST._mutable = False
        return super(CommentsViewset, self).create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author_user_id'] = request.user.pk
        request.data['issue_id'] = self.kwargs['issues_pk']
        request.POST._mutable = False
        return super(CommentsViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(CommentsViewset, self).destroy(request, *args, **kwargs)