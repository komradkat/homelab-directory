# Home Lab Master Directory

A lightweight, high-performance Django-based service directory dashboard that automatically handles routing between local LAN and Tailscale networks.

## Features

- **Dynamic Routing**: Automatically detects whether you're accessing via LAN or Tailscale and adjusts service URLs accordingly
- **Real-time Status Monitoring**: Port status checking to show which services are online/offline
- **Beautiful Dark Theme UI**: Modern, responsive interface built with TailwindCSS
- **Easy Management**: Django admin panel for adding/editing services
- **Docker Support**: Fully containerized with persistent storage
- **Zero Configuration**: Works out of the box with sensible defaults

## Quick Start with Docker (Recommended)

1. **Clone or navigate to the repository**:
   ```bash
   cd c:\Users\Komradkat\Documents\Repos\homelab-directory
   ```

2. **Build and start the container**:
   ```bash
   docker-compose up -d --build
   ```

3. **Access the dashboard**:
   - Local LAN: `http://10.0.0.2:8000`
   - Tailscale: `http://100.x.x.x:8000` (use your Tailscale IP)

4. **Create an admin user** (optional, for managing services):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
   Then access the admin panel at `http://10.0.0.2:8000/admin`

## Development Setup with UV

1. **Install dependencies**:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   .venv\Scripts\python.exe manage.py migrate
   ```

3. **Seed initial services**:
   ```bash
   .venv\Scripts\python.exe manage.py seed_services
   ```

4. **Run development server**:
   ```bash
   .venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
   ```

## Configuration

### Adding Your Tailscale IP

If your Tailscale IP doesn't match the `100.*` pattern, update `ALLOWED_HOSTS` in `homelab_directory/settings.py`:

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '10.0.0.2',
    'your-tailscale-ip',  # Add your specific Tailscale IP
]
```

### Adding New Services

**Via Admin Panel** (Recommended):
1. Go to `http://10.0.0.2:8000/admin`
2. Click "Services" → "Add Service"
3. Fill in the details:
   - **Name**: Service name (e.g., "Gitea")
   - **Description**: Brief description
   - **Port**: Port number (e.g., 3000)
   - **Protocol**: http or https
   - **Icon Name**: Bootstrap Icons class (e.g., `bi-git`)
   - **Order**: Display order (lower = first)

**Via Code**:
Edit `dashboard/management/commands/seed_services.py` and add your service to the list.

## Default Services

The dashboard comes pre-configured with:
- **Nginx Proxy Manager** (Port 81)
- **Portainer** (Port 9443, HTTPS)
- **AdGuard Home** (Port 3000)
- **Uptime Kuma** (Port 3001)

## How It Works

### Dynamic Routing Logic

The dashboard uses `request.get_host()` to detect your current IP address:
- If accessing from `10.0.0.x` → generates service URLs with `10.0.0.2`
- If accessing from `100.x.x.x` → generates service URLs with your Tailscale IP

This means you never have to manually switch URLs when moving between networks!

### Port Status Checking

Each service card shows a real-time status indicator:
- 🟢 **Green**: Port is accessible (service is online)
- 🔴 **Red**: Port is not accessible (service is offline)

The status is checked using Python's socket library with a 2-second timeout.

## Troubleshooting

### Services show as offline
- Ensure the services are actually running
- Check firewall settings on your homelab server
- Verify port numbers are correct in the admin panel

### Can't access from Tailscale
- Add your specific Tailscale IP to `ALLOWED_HOSTS` in settings.py
- Rebuild the Docker container: `docker-compose up -d --build`

### Database not persisting
- Ensure the `./data` directory exists and has proper permissions
- Check Docker volume mounting in `docker-compose.yml`

## Tech Stack

- **Backend**: Django 5.x
- **Frontend**: TailwindCSS + Bootstrap Icons
- **Server**: Gunicorn
- **Database**: SQLite
- **Static Files**: WhiteNoise
- **Container**: Docker + Docker Compose

## License

MIT License - Feel free to use and modify for your homelab!
