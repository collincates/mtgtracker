from django.core.paginator import Paginator


def paginator(request, object_list, items_per_page, mid_size=7):
    paginator = Paginator(object_list, items_per_page)
    page = request.GET.get('page')
    if not page:
        page = 1
    page_obj = paginator.get_page(page)

    # If list fits on number of pages larger than number of visible links
    if page_obj.paginator.num_pages > mid_size:
        # If at beginning of list
        if int(page) <= ((mid_size // 2)):
            visible_page_links = [i for i in range(1, (mid_size + 1))]
        # If at end of list
        elif int(page) >= page_obj.paginator.num_pages - (mid_size // 2):
            visible_page_links = [
                i for i in range(
                    (page_obj.paginator.num_pages - (mid_size - 1)),
                    page_obj.paginator.num_pages + 1
                )
            ]
        # If in middle of list
        else:
            visible_page_links = [
                i for i in range(
                    (int(page) - ((mid_size // 2) - 1)),
                    (int(page) + ((mid_size // 2) + 1))
                )
            ]
    # If list fits on > one page, but < number of visible page links
    elif page_obj.paginator.num_pages > 1:
        visible_page_links = [
            i for i in range(1, page_obj.paginator.num_pages + 1)
        ]
    # If list fits on one page or less
    else:
        visible_page_links = None

    return page_obj, visible_page_links
