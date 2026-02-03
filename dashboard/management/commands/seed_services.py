from django.core.management.base import BaseCommand
from dashboard.models import Service


class Command(BaseCommand):
    help = 'Seed the database with initial homelab services'

    def handle(self, *args, **options):
        self.stdout.write('Seeding services...')
        
        services = [
            {
                'name': 'Nginx Proxy Manager',
                'description': 'Reverse proxy manager with SSL support. Manage your proxy hosts, SSL certificates, and access lists.',
                'port': 81,
                'protocol': 'http',
                'icon_name': 'bi-shield-lock',
                'category': 'services',
                'order': 1,
            },
            {
                'name': 'Portainer',
                'description': 'Docker container management platform. Monitor and manage your Docker containers, images, and networks.',
                'port': 9443,
                'protocol': 'https',
                'icon_name': 'bi-box-seam',
                'category': 'tools',
                'order': 2,
            },
            {
                'name': 'AdGuard Home',
                'description': 'Network-wide ad blocker and DNS server. Block ads and trackers across all your devices.',
                'port': 3000,
                'protocol': 'http',
                'icon_name': 'bi-shield-check',
                'category': 'services',
                'order': 3,
            },
            {
                'name': 'Uptime Kuma',
                'description': 'Self-hosted monitoring tool. Track uptime and performance of your services with beautiful dashboards.',
                'port': 3001,
                'protocol': 'http',
                'icon_name': 'bi-activity',
                'category': 'tools',
                'order': 4,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for service_data in services:
            service, created = Service.objects.update_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {service.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated: {service.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeding complete! Created: {created_count}, Updated: {updated_count}'
            )
        )
