from django.db import transaction, models
from django.utils import timezone
from datetime import timedelta

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# 모델과 시리얼라이저 임포트는 한 번만 정리해서 사용합니다.
from .models import Book, Loan, Notice, Member # Member 모델도 필요합니다.
from .serializers import BookSerializer, LoanSerializer, NoticeSerializer

# 1. BookViewSet: 순수하게 도서 정보(CRUD)만 관리합니다.
class BookViewSet(viewsets.ModelViewSet):
    """
    도서 정보 관리를 위한 ViewSet
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 2. LoanViewSet: 대출/반납과 관련된 모든 로직을 관리합니다.
class LoanViewSet(viewsets.ModelViewSet):
    """
    대출 기록 관리를 위한 ViewSet.
    대출(checkout) 및 반납(checkin) 액션을 포함합니다.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    # '대출'은 새로운 대출 기록을 만드는 것이므로 LoanViewSet에 위치합니다.
    # detail=False는 /loans/checkout/ 과 같은 URL 경로를 생성합니다.
    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout_book(self, request):
        book_id = request.data.get('book_id')
        # custom user model을 사용하신다면 request.user가 Member 객체입니다.
        member = request.user 

        if not book_id:
            return Response({'error': '책의 QR코드를 스캔해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 로그인한 사용자인지 먼저 확인
        if not member.is_authenticated:
            return Response({'error': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            with transaction.atomic():
                # select_for_update()로 동시 대출 요청을 방지합니다.
                book = Book.objects.select_for_update().get(book_id=book_id)

                if book.status == Book.Status.ON_LOAN:
                    return Response({'error': '이미 대출 중인 도서입니다.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # 책 상태를 '대출 중'으로 변경
                book.status = Book.Status.ON_LOAN
                book.save()

                # 대출 기록 생성
                due_date = timezone.now() + timedelta(days=14)
                loan = Loan.objects.create(
                    book=book,
                    member=member,
                    due_date=due_date
                )
                
                # self.get_serializer()는 LoanSerializer를 반환하므로 정상 동작합니다.
                serializer = self.get_serializer(loan)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({'error': '존재하지 않는 도서입니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'대출 처리 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # '반납'은 특정 대출 기록(pk)을 수정하는 것이므로 detail=True로 설정합니다.
    # /loans/{loan_pk}/checkin/ 과 같은 URL 경로를 생성합니다.
    @action(detail=True, methods=['post'], url_path='checkin')
    def checkin_book(self, request, pk=None):
        try:
            with transaction.atomic():
                # self.get_object()는 pk에 해당하는 Loan 객체를 가져옵니다.
                loan = self.get_object() 

                if loan.return_date is not None:
                    return Response({'error': '이미 반납 처리된 대출입니다.'}, status=status.HTTP_400_BAD_REQUEST)

                # 책 상태를 '대출 가능'으로 변경
                book = loan.book
                book.status = Book.Status.AVAILABLE
                book.save()

                # 대출 기록에 반납일 업데이트
                loan.return_date = timezone.now()
                
                loan.save()

                serializer = self.get_serializer(loan)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({'error': '존재하지 않는 대출 기록입니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'반납 처리 중 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 3. NoticeViewSet: 공지사항 정보(CRUD)만 관리합니다.
class NoticeViewSet(viewsets.ModelViewSet):
    """
    공지사항 정보 관리를 위한 ViewSet
    """
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    # retrieve 메소드를 오버라이드하여 조회수 증가 로직을 추가합니다.
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # F() 표현식을 사용하여 race condition 없이 안전하게 조회수를 1 증가시킵니다.
        instance.view_count = models.F('view_count') + 1
        instance.save(update_fields=['view_count']) # view_count 필드만 업데이트
        instance.refresh_from_db() # DB에서 업데이트된 값을 다시 불러옵니다.
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)