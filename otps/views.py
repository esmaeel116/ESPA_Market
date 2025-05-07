from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OTPRequestSerializer


class OTPRequestView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'OTP sent successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
