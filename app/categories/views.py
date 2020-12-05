from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser


from .models import Category
from .serializers import CategorySerializer, CategoriesSerializer


class CategoriesList(APIView):
    """ Save categories to db. """

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'ok': True}, status=201)

        return JsonResponse(serializer.errors, status=400)


class CategoryDetail(APIView):
    """ Retrive category name, parents, children and siblings. """

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return HttpResponse(status=404)

        serializer = CategoriesSerializer(category)
        return JsonResponse(serializer.data)
