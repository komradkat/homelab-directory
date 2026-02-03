from django.db import models
import socket


class Service(models.Model):
    """Model representing a homelab service"""
    
    PROTOCOL_CHOICES = [
        ('http', 'HTTP'),
        ('https', 'HTTPS'),
    ]
    
    name = models.CharField(max_length=100, help_text="Service name (e.g., Portainer)")
    description = models.TextField(help_text="Brief description of the service")
    port = models.IntegerField(help_text="Port number (e.g., 9443)")
    protocol = models.CharField(
        max_length=5,
        choices=PROTOCOL_CHOICES,
        default='http',
        help_text="Protocol (HTTP or HTTPS)"
    )
    icon_name = models.CharField(
        max_length=50,
        help_text="Bootstrap Icons class name (e.g., 'bi-server')",
        default='bi-globe'
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('services', 'Services'),
            ('projects', 'Projects'),
            ('tools', 'Tools'),
            ('other', 'Other'),
        ],
        default='services',
        help_text="Category for organizing services"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether to display this service on the dashboard"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    
    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return f"{self.name} ({self.protocol}://{self.port})"
    
    def get_url(self, host):
        """Generate the service URL based on the current host"""
        # Extract just the IP/hostname without port
        if ':' in host:
            host = host.split(':')[0]
        return f"{self.protocol}://{host}:{self.port}"
    
    def check_status(self, host):
        """Check if the service port is accessible"""
        # Extract just the IP/hostname without port
        if ':' in host:
            host = host.split(':')[0]
        
        try:
            # Create a socket and try to connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # 2 second timeout
            result = sock.connect_ex((host, self.port))
            sock.close()
            return result == 0  # 0 means success
        except Exception:
            return False
