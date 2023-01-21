from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Contributors, Projects, Issues, Comments

User = get_user_model()


class UserSignupSerializer(ModelSerializer):
    tokens = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'tokens']

    @staticmethod
    def validate_email(value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise ValidationError("User already exists")
        return value

    @staticmethod
    def validate_password(value: str) -> str:
        if value is not None:
            return make_password(value)
        raise ValidationError("Password is empty")

    @staticmethod
    def get_tokens(user: User) -> dict:
        tokens = RefreshToken.for_user(user)
        data = {
            "refresh": str(tokens),
            "access": str(tokens.access_token)
        }
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id', 'user_id', 'project_id', 'permission', 'role']


class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'type', 'author_user_id']


class ProjectsDetailsSerializer(ModelSerializer):
    issues = SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'issues']

    @staticmethod
    def get_issues(instance):
        queryset = Issues.objects.filter(project_id=instance.id)
        return IssuesSerializer(queryset, many=True).data


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = ['title', 'tag', 'priority', 'project_id', 'status', 'created_time']


class IssuesDetailsSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issues
        fields = ['id', 'created_time', 'title', 'desc', 'priority', 'tag', 'status', 'author_user_id',
                  'assignee_user_id', 'project_id', 'comments']

    @staticmethod
    def get_comments(instance):
        queryset = Comments.objects.filter(issue_id=instance.id)
        return CommentsSerializer(queryset, many=True).data


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']
