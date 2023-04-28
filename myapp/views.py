
import os
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Candidates
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .serializer import CandidateSerializer
import traceback
from django.core.files import File
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings

class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class List_Candidates(ListAPIView):
    pagination_class = BasicPagination
    serializer_class = CandidateSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = Candidates.objects.all()
            location = self.request.query_params.get("location", None)
            if location:
                queryset = Candidates.objects.filter(location=location)

            # output = {
            #     "Candidates": CandidateSerializer(queryset, many=True).data
            # }

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_paginated_response(
                    self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

            # return Response(output, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            print(traceback.format_exc())


class AddCandidateData(APIView):
    def post(self, request):
        try:
            data = request.data
            candidate_record = []
            for item in data["candidates"]:
                each_record = Candidates(
                    name=item.get("name"),
                    address=item.get("address"),
                    contact=item.get("contact"),
                    location=item.get("location"),
                    skills=item.get("skills"),
                )
                candidate_record.append(each_record)
            Candidates.objects.bulk_create(candidate_record)
            return Response(
                {"success": "Data inserted successfully"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(e)
            print(traceback.format_exc())


class CreateResume(APIView):

    def render_to_pdf(self, template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

    def post(self, request):
        try:
            data = request.data

            obj = Candidates.objects.get(id=data['id'])
            # print("obj.......", obj)
            templ = os.path.join(str(settings.BASE_DIR), 'templates','template.html')
            context = {'instance': obj}
            pdf = self.render_to_pdf(templ, context)
            id = "{}.pdf" % (obj.id)
            obj.pdf_file.save(id, File(BytesIO(pdf.content)))
            return Response(
                {"success": "PDF Saved successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
