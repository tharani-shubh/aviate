from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from recruitment.models import Candidate


def validate_candidate(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        pk = kwargs.pop('pk', None)
        if not pk:
            return Response({"message": "pk is required for the request"},
                            status=status.HTTP_400_BAD_REQUEST)
        candidate = Candidate.objects.filter(id=pk)
        if not candidate.exists():
            return Response({"message": "Candidate not found"},
                            status=status.HTTP_404_NOT_FOUND)

        return view_func(candidate=candidate.first(), *args, **kwargs)

    return _wrapped_view