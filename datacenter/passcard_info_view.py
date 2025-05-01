from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from datacenter.models import format_duration, is_visit_long, get_duration

def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    this_passcard_visits = []
    for visit in Visit.objects.filter(passcard=passcard):
        sec = visit.get_duration()
        str_delta_time_visit = format_duration(sec)
        is_long_visit = visit.is_visit_long()
        this_passcard_visits.append({
            'entered_at': visit.entered_at,
            'duration': str_delta_time_visit,
            'is_strange': is_long_visit, 
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
