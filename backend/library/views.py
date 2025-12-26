from django.db import transaction, models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Loan, Notice, Member 
from .serializers import BookSerializer, LoanSerializer, NoticeSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    도서 정보 관리를 위한 ViewSet
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        검색어에 독일어 움라우트 변환 기능을 추가한 커스텀 쿼리셋
        """
        queryset = super().get_queryset()
        search_keyword = self.request.query_params.get("search", "")

        if search_keyword:
            german_keyword = search_keyword.replace('ae', 'ä')\
                                           .replace('oe', 'ö')\
                                           .replace('ue', 'ü')\
                                           .replace('ss', 'ß')
            queryset = queryset.filter(
                Q(title__icontains=search_keyword) | 
                Q(title__icontains=german_keyword) |
                Q(author__icontains=search_keyword) |
                Q(author__icontains=german_keyword) |
                Q(language__icontains=search_keyword) |      
                Q(call_number__icontains=search_keyword) |   
                Q(category__icontains=search_keyword) |      
                Q(location__icontains=search_keyword)        
            )

        language_filter = self.request.query_params.get("language")
        if language_filter:
            queryset = queryset.filter(language=language_filter)

        category_filter = self.request.query_params.get("category")
        if category_filter:
            queryset = queryset.filter(category=category_filter)

        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

class LoanViewSet(viewsets.ModelViewSet):
    """
    대출 기록 관리를 위한 ViewSet.
    대출(checkout) 및 반납(checkin) 액션을 포함합니다.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout_book(self, request):
        book_id = request.data.get('book_id')
        member = request.user 

        if not book_id:
            return Response({'error': '책의 QR코드를 스캔해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        if not member.is_authenticated:
            return Response({'error': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(book_id=book_id)

                if book.status == Book.Status.ON_LOAN:
                    return Response({'error': '이미 대출 중인 도서입니다.'}, status=status.HTTP_400_BAD_REQUEST)
                
                book.status = Book.Status.ON_LOAN
                book.save()
                due_date = timezone.now() + timedelta(days=14)
                loan = Loan.objects.create(
                    book=book,
                    member=member,
                    due_date=due_date
                )
                serializer = self.get_serializer(loan)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({'error': '존재하지 않는 도서입니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'대출 처리 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='checkin')
    def checkin_book(self, request, pk=None):
        try:
            with transaction.atomic():
                loan = self.get_object() 

                if loan.return_date is not None:
                    return Response({'error': '이미 반납 처리된 대출입니다.'}, status=status.HTTP_400_BAD_REQUEST)
                book = loan.book
                book.status = Book.Status.AVAILABLE
                book.save()
                loan.return_date = timezone.now()
                
                loan.save()

                serializer = self.get_serializer(loan)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({'error': '존재하지 않는 대출 기록입니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'반납 처리 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NoticeViewSet(viewsets.ModelViewSet):
    """
    공지사항 정보 관리를 위한 ViewSet
    """
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Notice.objects.filter(pk=instance.pk).update(view_count=models.F('view_count') + 1)
        instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)