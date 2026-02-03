from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service
from .forms import ServiceForm


def dashboard(request):
    """Main dashboard view with dynamic routing logic"""
    
    # Get the current host (IP:port or just IP)
    current_host = request.get_host()
    
    # Extract just the IP/hostname for status checks
    host_ip = current_host.split(':')[0]
    
    # Determine connection type
    connection_type = 'Tailscale' if host_ip.startswith('100.') else 'Local LAN'
    
    # Get all active services
    services = Service.objects.filter(is_active=True)
    
    # Group services by category
    services_by_category = {}
    online_count = 0
    offline_count = 0
    
    for service in services:
        is_online = service.check_status(host_ip)
        
        if service.category not in services_by_category:
            services_by_category[service.category] = {
                'name': service.get_category_display(),
                'services': []
            }
        
        services_by_category[service.category]['services'].append({
            'service': service,
            'url': service.get_url(current_host),
            'is_online': is_online,
        })
        
        if is_online:
            online_count += 1
        else:
            offline_count += 1
    
    # Create form instance
    form = ServiceForm()
    
    context = {
        'services_by_category': services_by_category,
        'current_host': current_host,
        'host_ip': host_ip,
        'connection_type': connection_type,
        'online_count': online_count,
        'offline_count': offline_count,
        'total_count': services.count(),
        'form': form,
    }
    
    return render(request, 'dashboard/index.html', context)


def add_service(request):
    """Handle adding new services via frontend form"""
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service "{form.cleaned_data["name"]}" added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error adding service. Please check the form.')
    
    return redirect('dashboard')


def edit_service(request, service_id):
    """Handle editing existing services"""
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        messages.error(request, 'Service not found.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service "{form.cleaned_data["name"]}" updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error updating service. Please check the form.')
    
    return redirect('dashboard')


def delete_service(request, service_id):
    """Handle deleting services"""
    try:
        service = Service.objects.get(id=service_id)
        service_name = service.name
        service.delete()
        messages.success(request, f'Service "{service_name}" deleted successfully!')
    except Service.DoesNotExist:
        messages.error(request, 'Service not found.')
    
    return redirect('dashboard')


