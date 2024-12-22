from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import GoodsSerializer
from goods.models import Goods
@api_view(['GET', 'POST'])
def goods_list(request):
    if request.method == 'GET':
        goods = Goods.objects.all()                   # 获取了所有的对象
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
@api_view(['GET', 'POST', 'DELETE'])
def goods_detail_byid(request, id):
    try:
        goods = Goods.objects.get(id=id)          # 获取具体的内容对象
    except Goods.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = GoodsSerializer(goods)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = GoodsSerializer(goods, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        goods.delete()
        return Response(status=status.HTTP_200_OK)