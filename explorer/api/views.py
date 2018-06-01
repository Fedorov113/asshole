from rest_framework import generics, mixins
from explorer.models import Dataset
from .serializers import *
from django.db.models import Q

class DatasetAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # Detail View
    lookup_field = 'pk'
    serializer_class = DatasetSerializer

    def get_queryset(self):
        qs = Dataset.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                    Q(df_name__icontains=query)|
                    Q(df_description__icontains=query)
                ).distinct()
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ActualShitAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = ActualShitSerializer

    def get_queryset(self):
        qs = ActualShitSample.objects.all()
        subject = self.request.GET.get('subject', None)
        if subject is not None:
            qs = qs.filter(subject=subject)

        return qs

class SubjectAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # Detail View
    lookup_field = 'pk'
    serializer_class = SubjectSerializer

    def get_queryset(self):
        qs = Subject.objects.all()
        return qs

class SubjectRUDView(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    lookup_field = 'pk'
    serializer_class = SubjectSerializer
    def get_queryset(self):
        return Subject.objects.all()

class DatasetRUDView(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    lookup_field = 'pk'
    serializer_class = DatasetSerializer

    # queryset = Dataset.objects.all()

    def get_queryset(self):
        return Dataset.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #     return Dataset.objects.get(pk=pk)
