from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, SalesInfo, Sales_History
from .forms import ProductForm, SalesInfoForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import re
from django.db.models import Q

# Create your views here.
def map(request):
    """
        map 조회
        """
    return render(request, 'sales/map.html')

@login_required(login_url='common:login')
def index(request):
    """
    product 목록 출력
    """
    try:
        # 입력 인자
        page = request.GET.get('page', '1') # GET 방식 요청 URL에서 페이지 값 가져옴. 페이지 번호 할당됨. 페이지 파라미터가 없는 URL은 기본값 1 지정
        product_list = Product.objects.order_by('pcode')
        # 페이징 처리
        paginator = Paginator(product_list, 10) # 페이지당 10개씩 보여주기
        page_obj = paginator.get_page(page)

        context = {'product_list':page_obj}
    except EmptyPage: # ?page=1000 같이 페이지 크게 입력할 경우, 마지막 페이지로 이동하도록 대비
        page = paginator.num_pages
        page_obj = paginator.page(page)
    return render(request, 'sales/product_list.html', context) # context의 product 데이터 product_list를
                                                              # sales/product_list.html 파일에 적용
@login_required(login_url='common:login')
def salesinfo_index(request):
    """
    sales 목록 출력
    """
    try:
        # 입력 인자
        page = request.GET.get('page', '1')
        search_mode = request.GET.get('search_mode')
        print(search_mode)
        if search_mode :
            if search_mode == '무상a/s불가':
                sales_list = Sales_History.objects.order_by('udate')
            else:
                sales_list = SalesInfo.objects.filter(main_inst=search_mode).order_by('sale_date')
        else:
            sales_list = SalesInfo.objects.order_by('sale_date')
        # 페이징 처리
        paginator = Paginator(sales_list, 10)
        page_obj = paginator.get_page(page)
        context = {'sales_list':page_obj}
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
    return render(request, 'sales/sales_list.html', context)


@login_required(login_url='common:login')
def detail(request, product_id):
    """
    sales 내용 출력
    """
    product = get_object_or_404(Product, pk=product_id)
    context = {'product':product}
    return render(request, 'sales/product_detail.html', context)

@login_required(login_url='common:login')
def salesinfo_detail(request, salesinfo_id):
    """
    sales 판매 내용 출력
    """
    salesinfo = get_object_or_404(SalesInfo, pk=salesinfo_id)
    context = {'salesinfo': salesinfo}
    return render(request, 'sales/salesinfo_detail.html', context)


@login_required(login_url='common:login') # 자동으로 로그인 화면으로 이동
def product_create(request):
    """
    sales 제품 등록
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # 꼭 !!!! files는 따로 request의 FILES로 속성을 지정해줘야 함
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.detailfunc = product.detailfunc.replace("'", "").replace("[", "").replace("]", "")
            product.save()
            return redirect('sales:index')
    else:
        form = ProductForm() # request.method 가 'GET'인 경우
    context = {'form':form}
    return render(request, 'sales/product_form.html', context)

@login_required(login_url='common:login') # 자동으로 로그인 화면으로 이동
def salesinfo_create(request):
    """
    sales 판매 등록
    """
    if request.method == 'POST':
        form = SalesInfoForm(request.POST)
        if form.is_valid():
            salesinfo = form.save(commit=False)
            salesinfo.author = request.user
            salesinfo.save()
            return redirect('sales:salesinfo_index')
    else:
        form = ProductForm() # request.method 가 'GET'인 경우
    context = {'form':form}
    return render(request, 'sales/salesinfo_form.html', context)

@login_required(login_url='common:login')
def product_modify(request, product_id):
    """
    sales 제품 수정
    """
    product = get_object_or_404(Product, pk=product_id)
    if request.user != product.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('sales:detail', product_id=product.id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product) # instance는 기존 값을 폼에 채움. imgfile도 있어서 request.FILES 추가
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.detailfunc = product.detailfunc.replace("'", "").replace("[","").replace("]","")
            product.modify_date = timezone.now()
            product.save()
            return redirect('sales:detail', product_id=product.id)

    else:
        form = ProductForm(instance=product)
    context = {'form': form}
    return render(request, 'sales/product_form.html', context)

@login_required(login_url='common:login')
def salesinfo_modify(request, salesinfo_id):
    """
    sales 판매 수정
    """
    salesinfo = get_object_or_404(SalesInfo, pk=salesinfo_id)
    if request.user != salesinfo.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('sales:salesinfo_detail', salesinfo_id=salesinfo.id)

    if request.method == "POST":
        form = SalesInfoForm(request.POST, instance=salesinfo) # instance는 기존 값을 폼에 채움. imgfile도 있어서 request.FILES 추가
        if form.is_valid():
            salesinfo = form.save(commit=False)
            salesinfo.author = request.user
            salesinfo.modify_date = timezone.now()
            salesinfo.save()
            return redirect('sales:salesinfo_detail', salesinfo_id=salesinfo.id)

    else:
        form = SalesInfoForm(instance=salesinfo)
    context = {'form': form}
    return render(request, 'sales/salesinfo_form.html', context)

@login_required(login_url='common:login')
def product_delete(request, product_id):
    """
    sales 제품 삭제
    """
    product = get_object_or_404(Product, pk=product_id)
    if request.user != product.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('sales:detail', product_id=product.id)
    product.delete()
    return redirect('sales:index')

@login_required(login_url='common:login')
def salesinfo_delete(request, salesinfo_id):
    """
    sales 판매 삭제
    """
    salesinfo = get_object_or_404(SalesInfo, pk=salesinfo_id)
    if request.user != salesinfo.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('sales:salesinfo_detail', salesinfo_id=salesinfo.id)
    salesinfo.delete()
    return redirect('sales:salesinfo_index')