from django.db import transaction, models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework import filters
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

    def get_queryset(self):
        """
        검색어에 독일어 움라우트 변환 기능을 추가한 커스텀 쿼리셋
        """
        queryset = super().get_queryset()
        
        # 1. 프론트엔드에서 보낸 검색어('search') 가져오기
        search_keyword = self.request.query_params.get("search", "")

        if search_keyword:
            # 2. 독일어 변환 로직 (ae -> ä, oe -> ö, ue -> ü, ss -> ß)
            german_keyword = search_keyword.replace('ae', 'ä')\
                                           .replace('oe', 'ö')\
                                           .replace('ue', 'ü')\
                                           .replace('ss', 'ß')
            
            # 3. 원래 검색어(ae) OR 독일어 변환 검색어(ä) 둘 중 하나라도 포함되면 찾기
            # title(제목) 또는 author(저자)에서 찾습니다.
            queryset = queryset.filter(
                Q(title__icontains=search_keyword) | 
                Q(title__icontains=german_keyword) |
                Q(author__icontains=search_keyword) |
                Q(author__icontains=german_keyword) |
                Q(language__icontains=search_keyword) |      # 언어
                Q(call_number__icontains=search_keyword) |   # 청구기호
                Q(category__icontains=search_keyword) |      # 분야
                Q(location__icontains=search_keyword)        # 위치
            )

        language_filter = self.request.query_params.get("language")
        if language_filter:
            queryset = queryset.filter(language=language_filter)

        # 2) 분야(카테고리) 필터
        category_filter = self.request.query_params.get("category")
        if category_filter:
            queryset = queryset.filter(category=category_filter)

        # 3) 상태(대출가능 여부) 필터
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

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
        # update() 메서드를 사용하여 DB 레벨에서 직접 증가시킵니다.
        Notice.objects.filter(pk=instance.pk).update(view_count=models.F('view_count') + 1)
        instance.refresh_from_db() # DB에서 업데이트된 값을 다시 불러옵니다.
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)