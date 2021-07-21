from django.db.models.query_utils import check_rel_lookup_compatibility
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, FormView, ListView

from .forms import *
from .models import *

import time
import numpy as np
from exif import Image

# Create your views here.
class UploadView(FormView):
    template_name = 'isbs/upload.html'
    form_class = UploadImageForm
    
    def form_valid(self, form):
        image = ImageData()
        image.image = form.cleaned_data["image"]
        
        checks_values = request.POST.get('checks[]')
            
            
        print('hoge', checks_values)
        
        with open('media/img/' + str(image.image), 'rb') as img_file:
            img = Image(img_file)
        
        lat_list = img.gps_latitude
        lon_list = img.gps_longitude
        
        image.latitude = lat_list[0] + (lat_list[1]/60) + (lat_list[2]/3600)
        image.longitude = lon_list[0] + (lon_list[1]/60) + (lon_list[2]/3600)
        
        image.save()
        
        return redirect("isbs:upload_list")
    
class UploadListView(ListView):
    template_name = 'isbs/upload_list.html'
    model = ImageData
    
    def post(self, request, *args, **kwargs):
        checks_value = request.POST.getlist('checks[]')
        
        # 選択した画像をdbから呼び出す
        for i in range(len(checks_value)):
            if i == 0:
                location_s = ImageData.objects.get(pk=int(checks_value[i]))
            else:
                location_g = ImageData.objects.get(pk=int(checks_value[i]))
        
        lat_s = location_s.latitude
        lon_s = location_s.longitude
        lat_g = location_g.latitude
        lon_g = location_g.longitude
        
        # お借りしたコード(https://qiita.com/damyarou/items/9cb633e844c78307134a)
        def cal_rho(lon_s, lat_s, lon_g, lat_g):
            ra=6378.140  # equatorial radius (km)
            rb=6356.755  # polar radius (km)
            F=(ra-rb)/ra # flattening of the earth
            rad_lat_a=np.radians(lat_s)
            rad_lon_a=np.radians(lon_s)
            rad_lat_b=np.radians(lat_g)
            rad_lon_b=np.radians(lon_g)
            pa=np.arctan(rb/ra*np.tan(rad_lat_a))
            pb=np.arctan(rb/ra*np.tan(rad_lat_b))
            xx=np.arccos(np.sin(pa)*np.sin(pb)+np.cos(pa)*np.cos(pb)*np.cos(rad_lon_a-rad_lon_b))
            c1=(np.sin(xx)-xx)*(np.sin(pa)+np.sin(pb))**2/np.cos(xx/2)**2
            c2=(np.sin(xx)+xx)*(np.sin(pa)-np.sin(pb))**2/np.sin(xx/2)**2
            dr=F/8*(c1-c2)
            rho=ra*(xx+dr)
            
            return rho
        
        context = {
            "location_s": location_s.id,
            "location_g": location_g.id,
            "image_path_s": location_s.image,
            "image_path_g": location_g.image,
            "rho": cal_rho(lon_s, lat_s, lon_g, lat_g),
        }

        return render(request, 'isbs/col_distance.html', context)
        
class DeleteView(DeleteView):
    template_name = 'isbs/delete.html'
    model = ImageData
    success_url = '/isbs/upload_list'