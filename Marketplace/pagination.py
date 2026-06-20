ELLIPSIS = "..."


def get_compact_page_range(page_obj, on_start=3, before=2, after=2, on_end=3):
    page_count = page_obj.paginator.num_pages
    current_page = page_obj.number

    visible_pages = set(range(1, min(on_start, page_count) + 1))
    visible_pages.update(range(max(1, current_page - before), min(page_count, current_page + after) + 1))
    visible_pages.update(range(max(1, page_count - on_end + 1), page_count + 1))

    compact_range = []
    last_page = None

    for page_number in sorted(visible_pages):
        if last_page is not None and page_number - last_page > 1:
            compact_range.append(ELLIPSIS)

        compact_range.append(page_number)
        last_page = page_number

    return compact_range
