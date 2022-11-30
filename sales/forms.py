from django import forms
from sales.models import Product, SalesInfo

class ProductForm(forms.ModelForm): # ModelForm 은 장고 모델 폼
    class Meta: # 장고 모델 폼은 반드시 내부에 Meta 클래스 가져야 함
        model = Product
        fields = ['pcode', 'pname', 'unitprice', 'discountrate', 'mainfunc', 'detailfunc', 'imgfile']
        labels = {
            'pcode': '제품 코드 ',
            'pname': '제 품 명 ',
            'unitprice': '단    가 ',
            'discountrate': '할 인 율 ',
            'mainfunc': '주요 기능',
            'detailfunc': '상세 기능',
            'imgfile': '이 미 지'
        }

class SalesInfoForm(forms.ModelForm):
    class Meta:
        model = SalesInfo
        fields = ['scode', 'sale_date', 'qty', 'amt', 'main_inst', 'detail_inst']
        labels = {
            'scode': '판매 제품 코드',
            'sale_date': '판매 일자',
            'qty': '판매 수량',
            'amt': '판매 금액',
            'main_inst': '구매처 분류',
            'detail_inst': '상세 주소',
        }