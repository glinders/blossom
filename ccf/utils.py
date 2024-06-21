from django.core.paginator import (
    Paginator, Page,
)


class MyPaginator(Paginator):
    # override _get_page to insert our version of class Page
    # I've copied the original docstring of _get_page as a reference
    # that this is the intended way to do this
    def _get_page(self, *args, **kwargs):
        """
        Return an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return MyPage(*args, **kwargs)


class MyPage(Page):
    def current_page_number(self):
        return self.paginator.validate_number(self.number)

