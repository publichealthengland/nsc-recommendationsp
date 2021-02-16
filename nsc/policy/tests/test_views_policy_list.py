from django.urls import reverse
from django.utils.translation import ugettext

import pytest
from bs4 import BeautifulSoup
from model_bakery import baker

from nsc.policy.models import Policy


# All tests require the database
pytestmark = pytest.mark.django_db

policy_list_url = reverse("policy:list")


def test_list_view(erm_user, django_app):
    """
    Test that the list view returns the list of policies.
    """
    instance = baker.make(Policy)
    response = django_app.get(policy_list_url, user=erm_user)
    assert instance in response.context["object_list"]
    assert not response.context["is_paginated"]
    assert response.context["paginator"].num_pages == 1


@pytest.mark.parametrize("num_policies", [1, 9])
def test_list_view_query_count(
    erm_user, num_policies, django_app, django_assert_num_queries
):
    """
    Test that fetching the list takes a fixed number of queries.
    """
    baker.make(Policy, _quantity=num_policies)
    django_app.get("/", user=erm_user)  # process login queries first
    with django_assert_num_queries(7):  # 3 for page, 4 for login.
        django_app.get(policy_list_url, user=erm_user)


def test_list__no_user(test_access_no_user):
    test_access_no_user(url=policy_list_url)


def test_list__incorrect_permission(test_access_forbidden):
    test_access_forbidden(url=policy_list_url)


def test_list_view_is_paginated(erm_user, django_app):
    """
    Test response is paginated.
    """
    baker.make(Policy, _quantity=50)
    response = django_app.get(policy_list_url, user=erm_user)
    assert response.context["is_paginated"]
    assert response.context["paginator"].num_pages > 1


def test_search_field_blank(erm_user, django_app):
    """
    Test that search field is initially blank.
    """
    form = django_app.get(policy_list_url, user=erm_user).form
    assert form["name"].value == ""


def test_search_on_condition_name(django_app_form):
    """
    Test the list of policies can be filtered by the condition name.
    """
    baker.make(Policy, name="name")
    response = django_app_form(policy_list_url, name="other")
    assert not response.context["object_list"]


def test_search_field_shows_name_term(django_app_form):
    """
    Test when the search results are shown the search field shows the entered condition name.
    """
    form = django_app_form(policy_list_url, name="name").form
    assert form["name"].value == "name"


def test_create_review_button(erm_user, django_app):
    """
    Test that the page contains a link (button) to create a new review.
    """
    baker.make(Policy, name="name")
    response = django_app.get(policy_list_url, user=erm_user)
    nodes = BeautifulSoup(response.content, "html.parser")
    link = nodes.find("a", {"id": "create-review-link-id"})
    assert link.text.strip() == ugettext("Create a new product")
    assert link["href"] == reverse("review:add")
