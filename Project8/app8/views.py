from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import EmployeeModel
from .forms import EmployeeForm

@method_decorator(csrf_exempt,name="dispatch")
class UpdateOneEmployee(View):
    def put(self,request,emp_idno):
        try:
            old_data = EmployeeModel.objects.get(idno = emp_idno)
        except EmployeeModel.DoesNotExist:
            json_mess = json.dumps({"error_message":"Given IDNO is Invalid"})
            return HttpResponse(json_mess,content_type="application/json")
        else:
            # old_data is in object Format but we need in dict format
            # Converting object to dict
            old_data_dict ={"idno":old_data.idno,"name":old_data.name,"salary":old_data.salary}

            data = request.body
            new_data = json.loads(data)

            # updating old_data with new_data
            old_data_dict.update(new_data)

            ef = EmployeeForm(old_data_dict)

            if ef.is_valid():
                ef.update()
                json_mess = json.dumps({"message": "Employee Record is Updated"})
                return HttpResponse(json_mess, content_type="application/json")
            if ef.errors:
                json_mess = json.dumps(ef.errors)
                return HttpResponse(json_mess, content_type="application/json")




