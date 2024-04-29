from rest_framework.routers import DefaultRouter
from vote.api.views import VoteApiViewSet

voteRouter = DefaultRouter()

voteRouter.register(
    prefix='vote',
    basename='vote',
    viewset=VoteApiViewSet
)