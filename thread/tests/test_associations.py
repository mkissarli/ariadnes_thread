from unittest import TestCase

from thread.logic import get_associated_companies_info_by_company


class AssociationsTestCase(TestCase):
    def test_associations(self):
        self.assertListEqual(
            sorted([c['company_number'] for c in get_associated_companies_info_by_company('07798925', depth=1)]),
            sorted(["09099356", "07714634"]))

    def test_something(self):
        pass
