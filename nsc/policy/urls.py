from django.urls import include, path

from . import views


urlpatterns = []

add_urlpatterns = (
    [
        path(r"", views.PolicyAdd.as_view(), name="start"),
        path(r"summary/<slug:slug>/", views.PolicyAddSummary.as_view(), name="summary"),
        # Note - not to be used in initial version, see view docstring.
        # path(
        #     r"document/<slug:slug>/", views.PolicyAddDocument.as_view(), name="document"
        # ),
        path(
            r"recommendation/<slug:slug>/",
            views.PolicyAddRecommendation.as_view(),
            name="recommendation",
        ),
    ],
    "add",
)

urlpatterns += [
    path("add/", include(add_urlpatterns)),
]

archive_urlpatterns = (
    [
        path(r"<slug:slug>/", views.ArchiveDetail.as_view(), name="detail"),
        path(
            r"<slug:slug>/upload/",
            views.ArchiveDocumentUploadView.as_view(),
            name="upload",
        ),
        path(r"<slug:slug>/update/", views.ArchiveUpdate.as_view(), name="update"),
        path(
            r"<slug:slug>/complete/", views.ArchiveComplete.as_view(), name="complete"
        ),
    ],
    "archive",
)

urlpatterns += [
    path("archive/", include(archive_urlpatterns)),
]

urlpatterns += [
    path(r"", views.PolicyList.as_view(), name="list"),
    path(r"<slug:slug>/", views.PolicyDetail.as_view(), name="detail"),
    path(r"<slug:slug>/edit/", views.PolicyEdit.as_view(), name="edit"),
]

app_name = "policy"
