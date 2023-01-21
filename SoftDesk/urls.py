from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import ContributorsViewset, ProjectsViewset, IssuesViewset, CommentsViewset, ProjectsAdminViewset, \
    SignupViewset
from django.urls import path, include
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register('projects', ProjectsViewset, basename='projects')

user_router = routers.NestedSimpleRouter(router, 'projects', lookup='projects')
user_router.register('users', ContributorsViewset, basename='users')

issue_router = routers.NestedSimpleRouter(router, 'projects', lookup='projects')
issue_router.register('issues', IssuesViewset, basename='issues')

comment_router = routers.NestedSimpleRouter(issue_router, 'issues', lookup='issues')
comment_router.register('comments', CommentsViewset, basename='comments')

router.register('admin/projects', ProjectsAdminViewset, basename="admin-projects")

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(user_router.urls)),
    path('api/', include(issue_router.urls)),
    path('api/', include(comment_router.urls)),
    path('admin/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/signup/', SignupViewset.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
