from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import json
from .serializers import *
from django.db.models import Q

from rest_framework.exceptions import ErrorDetail, ValidationError


class ImportFromAsshole(APIView):
    """
    Used to import data from another asshole system.
    """
    def post(self, request):
        """
        Accept dataset folder
        :param request:
        :return:
        """
        data = request.data
        print(data)

        # Find all samples in shortest folder
        # Construct model objects for samples (container, files, profile)
        # Repeat for all preprocessings

        return HttpResponse('import view', content_type='application/json')


class SampleSourceList(APIView):
    def get(self, request):
        sources_dict = {}
        # sources = SampleSource.objects.filter(real_samples__mgsample__dataset_hard=pk).distinct()
        sources = SampleSource.objects.all().prefetch_related('real_samples')

        for source in sources:
            rsamps = [rs.id for rs in source.real_samples.all()]
            meta = {}
            try:
                meta = json.loads(source.meta_info)
            except:
                meta = None
            sources_dict[source.id] = {'id': source.id,
                                       'name': source.name,
                                       'description': source.description,
                                       'meta_info': meta,
                                       'meta_schema': source.meta_schema_id,
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
            meta = {}
            try:
                meta = json.loads(sample.meta_info)
            except:
                meta = None
            mgsamps = [rs.id for rs in sample.mg_samples.all()]
            samples_dict[sample.id] = {
                'id': sample.id,
                'source': sample.source_id,
                'time_point': sample.time_point,
                'name': sample.name,
                'description': sample.description,
                'meta_info': meta,
                'mg_samples': mgsamps,

            }
        return HttpResponse(json.dumps(samples_dict), content_type='application/json')

    def post(self, request):
        data = request.data
        real_sample = RealSample(**data)
        real_sample.save()
        return HttpResponse(json.dumps('created'), content_type='application/json')


class SchemaList(APIView):
    def get(self, request):
        schemas_dict = {}
        schemas = MetaSchema.objects.all()
        for schema in schemas:
            schemas_dict[schema.id] = {
                'id': schema.id,
                'name': schema.name,
                'schema': schema.schema
            }

        return HttpResponse(json.dumps(schemas_dict), content_type='application/json')


class MgSampleNewList(APIView):
    def get(self, request):
        resp = {}
        samples_dict = {}
        hdf = request.query_params.get('hdf', None)
        sdf = request.query_params.get('sdf', None)
        run = request.query_params.get('run', None)
        lib = request.query_params.get('lib', None)
        dtype = request.query_params.get('dtype', None)
        source = request.query_params.get('source', None)

        mg_samples = []
        mg_sample_ids = []
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
        if source is not None:
            mg_samples = MgSample.objects.filter(source=source) \
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
                    files.append({'profile': profile, 'id': file.id, 'strand': file.strand, })
                containers.append({'files': files, 'id': container.id, 'preprocessing': container.preprocessing, })
            samples_dict[sample.id] = {
                'containers': containers,
                'id': sample.id,
                'name': sample.name,
                'name_on_fs': sample.name_on_fs,
                "dataset_hard": sample.dataset_hard_id,
                "real_sample": sample.real_sample_id,
                "source": sample.source_id,
                "library": sample.library_id,
                "sequencing_run": sample.sequencing_run_id,
                # "full_name": sample.full_name
            }
            mg_sample_ids.append(sample.id)
            if sample.real_sample is not None:
                samples_dict[sample.id]['source'] = sample.real_sample.source.id
            else:
                pass

        resp = {'ids': mg_sample_ids, 'data': samples_dict, }
        return HttpResponse(json.dumps(resp), content_type='application/json')


class MgSampleUpdate(APIView):
    def put(self, request):
        data = request.data
        print(data)
        for key in data.keys():
            s, created = MgSample.objects.update_or_create(defaults=data[key], pk=key)

        return HttpResponse(json.dumps('update'), content_type='application/json')


class RealSampleUpdate(APIView):
    def put(self, request):
        data = request.data
        print(data)
        for key in data.keys():
            s, created = RealSample.objects.update_or_create(defaults=data[key], pk=key)

        return HttpResponse(json.dumps('update'), content_type='application/json')


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
        print('getting serializer')
        if isinstance(kwargs.get('data', {}), list):
            print('many')
            kwargs['many'] = True
        return super(MgSampleFullList, self).get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            print('check valid')
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            print('not valid....')
            print(ValidationError.detail)
        print('checked valid')
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        print('getting sample list queryset')

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
