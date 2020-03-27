from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PostPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, postList, host):
        if len(postList) > self.page_size:
            next_page = host + str(self.page_size)
        else:
            next_page = None
            previous_page = None

        return Response({
            "query": "posts",
            "count": len(postList),
            "size": self.page_size,
            "next": next_page,
            "previous": previous_page,
            "posts": postList}
        )


class CommentPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, postList, host):
        if len(postList) > self.page_size:
            next_page = host + str(self.page_size)
        else:
            next_page = None
            previous_page = None

        return Response({
            "query": "posts",
            "count": len(postList),
            "size": self.page_size,
            "next": next_page,
            "previous": previous_page,
            "posts": postList}
        )
