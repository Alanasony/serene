from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from host.models import *



def admin_dashboard(request):
    return render(request,'admin_dashboard.html')



def admin_pending(request):
    pending_hosts = tbl_host.objects.filter(status='pending')
    print(pending_hosts)
    return render(request, 'admin_pending.html', {'hosts': pending_hosts})

def admin_approve(request):
    approved_hosts = tbl_host.objects.filter(status='approved')
    return render(request, 'admin_approve.html', {'hosts': approved_hosts})

def admin_reject(request):
    rejected_hosts = tbl_host.objects.filter(status='rejected')
    return render(request, 'admin_reject.html', {'hosts': rejected_hosts})




def admin_approve(request):
    host_id = request.GET.get('id')
    if host_id:
        try:
            host = tbl_host.objects.get(id=host_id)
            host.status = 'approved'  # Update status to 'approved'
            host.save()
        except tbl_host.DoesNotExist:
            return HttpResponse("Host not found", status=404)
    return render(request,'admin_approve.html')  # Redirect to pending hosts list

def admin_reject(request):
    host_id = request.GET.get('id')
    if host_id:
        try:
            host = tbl_host.objects.get(id=host_id)
            host.status = 'rejected'  # Update status to 'rejected'
            host.save()
        except tbl_host.DoesNotExist:
            return HttpResponse("Host not found", status=404)
    return render(request,'admin_reject.html')# Redirect to pending hosts list
