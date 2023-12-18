import uuid
from finalapp.models import Fee

def fee_id(request):
    if 'fee_id' not in request.session:
        request.session['fee_id']=str(uuid.uuid4())
    return request.session['fee_id']



def get_fee(request):
    return Fee.objects.filter(fee_id=fee_id(request))

def total_(request):
    fees=get_fee(request)
    t=0
    for i in fees:
        t+=i.total()
    return t
