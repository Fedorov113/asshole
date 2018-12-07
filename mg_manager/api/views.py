from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from django.http import HttpResponse
import json
from .serializers import *
from django.db.models import Q


class SampleSourceList(APIView):
    def get(self, request):
        sources_dict = {}
        # sources = SampleSource.objects.filter(real_samples__mgsample__dataset_hard=pk).distinct()
        sources = SampleSource.objects.all().prefetch_related('real_samples')

        for source in sources:
            rsamps = [rs.id for rs in source.real_samples.all()]
            sources_dict[source.id] = {'id': source.id,
                                       'name': source.name,
                                       'description': source.description,
                                       'real_samples': rsamps}

        return HttpResponse(json.dumps(sources_dict), content_type='application/json')

    def post(self, request):
        data = request.data
        source = SampleSource(name=data['name'], description=data['description'], meta_info=data['meta_info'])
        source.save()
        return HttpResponse(json.dumps('created'), content_type='application/json')


class RealSampleList(APIView):
    def get(self, request):
        samples_dict = {}
        rsamples = RealSample.objects.all().prefetch_related('mg_samples')
        print(len(rsamples))
        for sample in rsamples:
            mgsamps = [rs.id for rs in sample.mg_samples.all()]
            samples_dict[sample.id] = {
                'id': sample.id,
                'source':sample.source_id,
                'name': sample.name,
                'description': sample.description,
                'mg_samples': mgsamps
            }

        return HttpResponse(json.dumps(samples_dict), content_type='application/json')

    def post(self, request):
        data = request.data
        real_sample = RealSample(**data)
        real_sample.save()
        return HttpResponse(json.dumps('created'), content_type='application/json')

class MgSampleNewList(APIView):
    def get(self, request):
        samples_dict = {}
        hdf = request.query_params.get('hdf', None)
        sdf = request.query_params.get('sdf', None)
        run = request.query_params.get('run', None)
        lib = request.query_params.get('lib', None)
        dtype = request.query_params.get('dtype', None)

        mg_samples = []
        if hdf is not None:
            mg_samples = MgSample.objects.filter(dataset_hard=hdf) \
                .prefetch_related('containers') \
                .prefetch_related('containers__files') \
                .prefetch_related('containers__files__profile').select_related('real_sample__source')
        if run is not None:
            mg_samples = MgSample.objects.filter(sequencing_run=run) \
                .prefetch_related('containers') \
                .prefetch_related('containers__files') \
                .prefetch_related('containers__files__profile').select_related('real_sample__source')


        for sample in mg_samples:
            containers = []
            for container in sample.containers.all():
                files = []
                for file in container.files.all():
                    profile = {}
                    for profile in file.profile.all():
                        profile = [{
                            'id': profile.id,
                            'bp': profile.bp,
                            'reads': profile.reads,
                        }]
                    files.append({'profile': profile,'id':file.id, 'strand': file.strand,})
                containers.append({'files': files, 'id':container.id, 'preprocessing': container.preprocessing, })
            print(sample.__dict__)
            samples_dict[sample.id] = {
                'containers': containers,
                'id': sample.id,
                'name': sample.name,
                'name_on_fs':sample.name_on_fs,
                "dataset_hard": sample.dataset_hard_id,
                "real_sample": sample.real_sample_id,
                "source": sample.source_id,
                "library": sample.library_id,
                "sequencing_run": sample.sequencing_run_id,
            }
            if sample.real_sample is not None:
                samples_dict[sample.id]['source'] = sample.real_sample.source.id
            else: pass

        return HttpResponse(json.dumps(samples_dict), content_type='application/json')

class MgSampleOther(APIView):
    def get(self, request, pk):
        samples_dict = {}
        mg_samples = MgSample.objects.filter(dataset_hard=pk).prefetch_related('containers').only('id')
        for sample in mg_samples:
            conts = [rs.id for rs in sample.containers.all()]
            samples_dict[sample.id] = {
                'id': sample.id,
                'name_on_fs':sample.name_on_fs,
                'containers': conts
            }

        return HttpResponse(json.dumps(samples_dict), content_type='application/json')

# class SampleSourceList(generics.ListCreateAPIView):  # Detail View
#     queryset = SampleSource.objects.all()
#     serializer_class = SampleSourceSerializer
#     print('SampleSourceList')
#     def get_queryset(self):
#         qs = SampleSource.objects.all()
#         if 'pk' in self.kwargs:
#             hard_df_pk = self.kwargs['pk']
#             if hard_df_pk is not None:
#                 qs = qs.filter(real_samples__mgsample__dataset_hard=hard_df_pk).distinct()
#         return qs


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
    serializer_class = MgSampleSerializer

# class RealSampleAPIView(mixins.CreateModelMixin, generics.ListAPIView):
#     lookup_field = 'pk'
#     serializer_class = RealSampleSerializer
#
#     def get_queryset(self):
#         qs = RealSample.objects.all()
#         query = self.request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(
#                 Q(df_name__icontains=query) |
#                 Q(df_description__icontains=query)
#             ).distinct()
#         return qs
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class MgSampleFileContainerList(generics.ListCreateAPIView):  # Detail View
#     queryset = MgSampleFileContainer.objects.all()
#     serializer_class = MgSampleFileContainerSerializer