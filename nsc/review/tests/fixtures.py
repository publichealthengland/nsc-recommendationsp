import pytest
from dateutil.relativedelta import relativedelta
from model_bakery import baker

from nsc.policy.models import Policy

from ..models import Review
from ...utils.datetime import get_today


@pytest.fixture
def make_review():
    def _make_review(**kwargs):
        policy = baker.make(Policy, name="condition", ages="{child}")
        review = baker.make(Review, **kwargs)
        review.policies.add(policy)
        return review

    return _make_review


@pytest.fixture
def review_in_pre_consultation(make_review):
    review_start = get_today() - relativedelta(months=2)
    return make_review(
        name="review",
        status=Review.STATUS.draft,
        phase=Review.PHASE.pre_consultation,
        review_start=review_start,
    )


@pytest.fixture
def review_in_consultation(make_review):
    review_start = get_today() - relativedelta(months=2)
    consultation_start = review_start + relativedelta(months=2)
    consultation_end = consultation_start + relativedelta(months=3)
    return make_review(
        name="review",
        status=Review.STATUS.draft,
        phase=Review.PHASE.consultation,
        review_start=review_start,
        consultation_start=consultation_start,
        consultation_end=consultation_end,
    )


@pytest.fixture
def review_in_post_consultation(make_review):
    review_start = get_today() - relativedelta(months=6)
    consultation_start = review_start + relativedelta(months=2)
    consultation_end = consultation_start + relativedelta(months=3)
    return make_review(
        name="review",
        status=Review.STATUS.draft,
        phase=Review.PHASE.post_consultation,
        review_start=review_start,
        consultation_start=consultation_start,
        consultation_end=consultation_end,
    )


@pytest.fixture
def review_completed(make_review):
    review_start = get_today() - relativedelta(months=6)
    consultation_start = review_start + relativedelta(months=2)
    consultation_end = consultation_start + relativedelta(months=3)
    return make_review(
        name="review",
        status=Review.STATUS.draft,
        phase=Review.PHASE.completed,
        review_start=review_start,
        consultation_start=consultation_start,
        consultation_end=consultation_end,
    )


@pytest.fixture
def review_published(make_review):
    review_start = get_today() - relativedelta(months=8)
    consultation_start = review_start + relativedelta(months=2)
    consultation_end = consultation_start + relativedelta(months=3)
    review_end = consultation_start + relativedelta(months=1)
    return make_review(
        name="review",
        status=Review.STATUS.published,
        phase=Review.PHASE.completed,
        review_start=review_start,
        review_end=review_end,
        consultation_start=consultation_start,
        consultation_end=consultation_end,
    )
