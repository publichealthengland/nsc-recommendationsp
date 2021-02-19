# All tests require the database
from datetime import timedelta

from django.conf import settings
from django.test import override_settings

import pytest

from nsc.contact.models import Contact
from nsc.notify.models import Email
from nsc.review.tasks import (
    send_open_review_notifications,
    send_published_notifications,
)
from nsc.utils.datetime import get_today


pytestmark = pytest.mark.django_db


def test_no_reviews_have_open_consultation_time_in_the_past_no_emails_are_not_created(
    make_review,
):
    make_review(
        consultation_start=get_today() + timedelta(days=1), dates_confirmed=True
    )
    make_review(
        consultation_start=get_today() + timedelta(days=2), dates_confirmed=True
    )

    send_open_review_notifications()

    assert not Email.objects.exists()


def test_no_reviews_have_confirmed_dates_emails_are_not_created(make_review):
    make_review(
        consultation_start=get_today() - timedelta(days=1), dates_confirmed=False
    )
    make_review(
        consultation_start=get_today() - timedelta(days=2), dates_confirmed=False
    )

    send_open_review_notifications()

    assert not Email.objects.exists()


@override_settings(
    PHE_COMMUNICATIONS_EMAIL="comms@example.com",
    NOTIFY_TEMPLATE_CONSULTATION_OPEN="open template",
)
def test_reviews_have_confirmed_dates_in_the_past_emails_are_created(make_review):
    target = make_review(
        consultation_start=get_today() - timedelta(days=1),
        dates_confirmed=True,
        add_stakeholders=True,
    )
    make_review(
        consultation_start=get_today() + timedelta(days=1),
        dates_confirmed=True,
        add_stakeholders=True,
    )

    send_open_review_notifications()

    target_contact_emails = (
        Contact.objects.filter(stakeholder__reviews=target)
        .distinct()
        .values_list("email", flat=True)
    )

    assert (
        Email.objects.count() == len(target_contact_emails) + 1
    )  # add 1 for the phe comms notification
    assert Email.objects.filter(
        address__in=target_contact_emails,
        status=Email.STATUS.pending,
        context=target.get_email_context(),
        template_id=settings.NOTIFY_TEMPLATE_CONSULTATION_OPEN,
    ).count() == len(target_contact_emails)
    assert Email.objects.filter(
        address=settings.PHE_COMMUNICATIONS_EMAIL,
        status=Email.STATUS.pending,
        context=target.get_email_context(),
        template_id=settings.NOTIFY_TEMPLATE_CONSULTATION_OPEN,
    ).exists()


@override_settings(
    PHE_COMMUNICATIONS_EMAIL="comms@example.com",
    NOTIFY_TEMPLATE_SUBSCRIBER_CONSULTATION_OPEN="sub open template",
)
def test_open_review_conditions_have_subscribers_subs_receive_emails(
    make_review, make_policy, make_subscription
):
    open_policy, closed_policy = make_policy(_quantity=2)
    expected = make_subscription(policies=[open_policy])
    make_subscription(policies=[closed_policy])

    make_review(
        consultation_start=get_today() - timedelta(days=1),
        dates_confirmed=True,
        add_stakeholders=True,
        policies=[open_policy],
    )
    make_review(
        consultation_start=get_today() + timedelta(days=1),
        dates_confirmed=True,
        add_stakeholders=True,
        policies=[closed_policy],
    )

    send_open_review_notifications()

    assert Email.objects.filter(
        address=expected.email,
        status=Email.STATUS.pending,
        context=open_policy.get_email_context(),
        template_id=settings.NOTIFY_TEMPLATE_SUBSCRIBER_CONSULTATION_OPEN,
    ).exists()


def test_no_reviews_have_been_published_no_emails_are_not_created(make_review,):
    make_review(published=False)
    make_review(published=False)

    send_published_notifications()

    assert not Email.objects.exists()


@override_settings(
    PHE_COMMUNICATIONS_EMAIL="comms@example.com",
    NOTIFY_TEMPLATE_DECISION_PUBLISHED="decision template",
)
def test_reviews_published_emails_are_created(make_review):
    target = make_review(published=True)
    make_review(published=False)

    send_published_notifications()

    target_contact_emails = (
        Contact.objects.filter(stakeholder__reviews=target)
        .distinct()
        .values_list("email", flat=True)
    )

    assert (
        Email.objects.count() == len(target_contact_emails) + 1
    )  # add 1 for the phe comms notification
    assert Email.objects.filter(
        address__in=target_contact_emails,
        status=Email.STATUS.pending,
        context=target.get_email_context(),
        template_id=settings.NOTIFY_TEMPLATE_DECISION_PUBLISHED,
    ).count() == len(target_contact_emails)
    assert Email.objects.filter(
        address=settings.PHE_COMMUNICATIONS_EMAIL,
        status=Email.STATUS.pending,
        context=target.get_email_context(),
        template_id=settings.NOTIFY_TEMPLATE_DECISION_PUBLISHED,
    ).exists()


@override_settings(
    PHE_COMMUNICATIONS_EMAIL="comms@example.com",
    NOTIFY_TEMPLATE_SUBSCRIBER_DECISION_PUBLISHED="sub decision template",
)
def test_decided_review_conditions_have_subscribers_subs_receive_emails(
    make_review, make_policy, make_subscription
):
    published_policy, unpublished_policy = make_policy(_quantity=2)
    expected = make_subscription(policies=[published_policy])
    make_subscription(policies=[unpublished_policy])

    make_review(published=True, policies=[published_policy])
    make_review(published=False, policies=[unpublished_policy])

    send_published_notifications()

    assert Email.objects.filter(
        address=expected.email,
        status=Email.STATUS.pending,
        context=published_policy.get_email_context(),
        template_id=settings.NOTIFY_TEMPLATE_SUBSCRIBER_DECISION_PUBLISHED,
    ).exists()
