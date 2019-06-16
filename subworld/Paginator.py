import collections.abc

from django.core.paginator import PageNotAnInteger, EmptyPage
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class Paginator:
    def __init__(self, object_lists, total_pages, total_results, per_page=20, allow_empty_first_page=True):
        self.object_lists = object_lists
        self.total_pages = total_pages
        self.total_results = total_results
        self.per_page = per_page
        self.allow_empty_first_page = allow_empty_first_page

    def validate_number(self, number):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_('That page number is not an integer'))
        if number < 1:
            raise EmptyPage(_('That page number is less than 1'))
        if number > self.total_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage(_('That page contains no results'))
        return number

    def get_page(self, number):
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages
        return Page(self.object_lists, number, self)

    @staticmethod
    def _get_page(*args, **kwargs):

        return Page(*args, **kwargs)

    @cached_property
    def count(self):
        return self.validate_number(self.total_results)

    @cached_property
    def num_pages(self):
        return self.validate_number(self.total_pages)

    @property
    def page_range(self):
        return range(1, self.num_pages + 1)


class Page(collections.abc.Sequence):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __getitem__(self, index):
        if not isinstance(index, (int, slice)):
            raise TypeError

        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def __repr__(self):
        return '<Pae %s of %s>' % (self.number, self.paginator.num_pages)

    def __len__(self):
        return self.paginator.total_results

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)

    def start_display_page_number(self):

        if self.number == 1:
            return 1
        if self.number - 5 < 1:
            return 1
        return self.number - 5

    def end_display_page_number(self):

        if self.number + 5 > self.paginator.num_pages:
            return self.paginator.num_pages
        return self.number + 5
