"""
Scraper extracting the list of NSC policies from the legacy web site.

"""

import json
import re

import requests
from bs4 import BeautifulSoup

from nsc.policy.models import Policy
from nsc.stakeholder.models import Stakeholder


def run():
    print("Scraping...")
    index = load_index()
    for entry in index:
        print(" ", entry["name"])
        page = get_page(entry["url"])

        for stakeholder in get_stakeholders(page):
            contact, created = Stakeholder.objects.get_or_create(
                name=stakeholder["name"]
            )

            if created:
                contact.url = stakeholder["url"]
                contact.publish = True
                contact.save()

            contact.policies.add(Policy.objects.get(slug=entry["slug"]))

    print("Finished")


def load_index():
    with open("fixtures/legacy_index.json", "r") as fp:
        return json.load(fp)


def get_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def get_stakeholders(node):
    results = []
    regex = re.compile(r"^Stakeholders.*")
    node = node.find("h3", string=regex).find_next_sibling("p")
    for stakeholder in node.find_all("a"):
        results.append({"name": stakeholder.text.strip(), "url": stakeholder["href"]})
    return results
