from rest_framework import generics, mixins, viewsets

from .serializers import *
from django.db.models import Q

class SampleSourceList(generics.ListCreateAPIView):  # Detail View
    # queryset = SampleSource.objects.all()
    serializer_class = SampleSourceSerializer

    def get_queryset(self):
        qs = SampleSource.objects.all()
        if 'pk' in self.kwargs:
            hard_df_pk = self.kwargs['pk']
            if hard_df_pk is not None:
                qs = qs.filter(
                    Q(df=hard_df_pk)
                ).distinct()
        return qs


class DatasetHardList(generics.ListCreateAPIView):  # Detail View
    queryset = DatasetHard.objects.all()
    serializer_class = DatasetHardSerializer

class DatasetHardDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = DatasetHard.objects.all()
    serializer_class = DatasetHardSerializer

class DatasetHardFull(generics.ListCreateAPIView):
    serializer_class = DatasetHardFullSerializer
    queryset = DatasetHard.objects.all()

class LibraryList(generics.ListCreateAPIView):  # Detail View
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class LibraryDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class SequencingRunList(generics.ListCreateAPIView):  # Detail View
    queryset = SequencingRun.objects.all()
    serializer_class = SequencingRunSerializer

class MgSampleFullList(generics.ListCreateAPIView):
    serializer_class = MgSampleFullSerializer

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(MgSampleFullList, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        qs = MgSample.objects.all()
        print('sample list queryset')
        if 'pk' in self.kwargs:
            hard_df_pk = self.kwargs['pk']
            print(hard_df_pk)
            if hard_df_pk is not None:
                qs = qs.filter(
                    Q(dataset_hard=hard_df_pk)
                ).distinct()
        return qs

class MgSampleFullLookup(generics.ListCreateAPIView):
    serializer_class = MgSampleFullSerializer

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(MgSampleFullLookup, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        qs = MgSample.objects.all()
        hdf = self.request.query_params.get('hdf', None)
        sdf = self.request.query_params.get('sdf', None)
        run = self.request.query_params.get('run', None)
        lib = self.request.query_params.get('lib', None)
        dtype = self.request.query_params.get('dtype', None)

        if hdf is not None:
            qs = qs.filter(Q(dataset_hard=hdf))
        if run is not None:
            qs = qs.filter(Q(sequencing_run=run))

        return qs

class MgSampleContainerFileList(generics.ListCreateAPIView):
    serializer_class = MgSampleContainerFileSerializer
    queryset = MgFile.objects.all()

class MgSampleContainerList(generics.ListCreateAPIView):
    serializer_class = MgSampleContainerSerializer
    queryset = MgSampleFileContainer.objects.all()

class MgSampleList(generics.ListCreateAPIView):
    serializer_class = MgSampleSerializer
    queryset = MgSample.objects.all()

class MgSampleDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = MgSample.objects.all()
    serializer_class = MgSampleFullSerializer

class RealSampleAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = RealSampleSerializer

    def get_queryset(self):
        qs = RealSample.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(df_name__icontains=query) |
                Q(df_description__icontains=query)
            ).distinct()
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# class MgSampleFileContainerList(generics.ListCreateAPIView):  # Detail View
#     queryset = MgSampleFileContainer.objects.all()
#     serializer_class = MgSampleFileContainerSerializer