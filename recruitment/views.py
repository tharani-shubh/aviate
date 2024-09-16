from django.db.models import Q, Value, IntegerField, Case, When

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from recruitment.decorators import validate_candidate
from recruitment.models import Candidate
from recruitment.serializers import CandidateSerializer


class CandidateView(APIView):

    def get(self, request):
        query = request.GET.get('q', '')
        search_terms = query.split()

        filters = Q()
        for term in search_terms:
            filters |= Q(name__icontains=term)
        annotations = {
            'relevancy_score': sum(
                Case(
                    When(Q(name__icontains=term), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                ) for term in search_terms
            )
        }

        candidates = Candidate.objects.annotate(**annotations).filter(filters).order_by('-relevancy_score')
        candidates_serializer = CandidateSerializer(candidates, many=True)
        return Response(candidates_serializer.data)


    def post(self, request):
        candidate_serializer = CandidateSerializer(data=request.data)
        if candidate_serializer.is_valid():
            candidate_serializer.save()
            return Response(candidate_serializer.data)
        return Response(candidate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @validate_candidate
    def put(self, request, candidate):
        candidate_serializer = CandidateSerializer(data=request.data,
                                                   instance=candidate,
                                                   partial=False)
        if candidate_serializer.is_valid():
            candidate_serializer.save()
            return Response(candidate_serializer.data)
        return Response(candidate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @validate_candidate
    def patch(self, request, candidate):
        candidate_serializer = CandidateSerializer(data=request.data,
                                                   instance=candidate,
                                                   partial=True)
        if candidate_serializer.is_valid():
            candidate_serializer.save()
            return Response(candidate_serializer.data)
        return Response(candidate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @validate_candidate
    def delete(self, request, candidate):
        candidate.delete()
        return Response({"message": "Candidate deleted"})
