from rest_framework import generics, mixins
from mis.models import Person
from .serializers import PersonSerializer


class PersonAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # Detail View
    lookup_field = 'pk'
    serializer_class = PersonSerializer

    def get_queryset(self):
        qs = Person.objects.all()
        query = self.request.GET.get('q')
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'

    serializer_class = PersonSerializer

    def get_queryset(self):
        return Person.objects.all()