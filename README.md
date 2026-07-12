# StyleBook

StyleBook is a Django web application for sharing, browsing, saving, and managing game character appearance styles. Users can register an account, upload style screenshots, crop a thumbnail, browse styles by class, like and favourite styles, mark styles as downloadable, and manage their own uploaded styles.

The project serves a single-page React interface from a Django template and exposes the app data through Django REST Framework API endpoints.

## Features

- User registration, login, logout, and current-session detection.
- Style home page with hot and suggested styles.
- View All page with class filters, search, pagination, favourites filter, and savable-only filter.
- My Style page for the signed-in user's styles.
- Style creation with title, description, class, image uploads, thumbnail cropper, and downloadable flag.
- Style editing with metadata updates, thumbnail replacement, gallery image addition, and gallery image removal.
- Style detail modal with gallery browsing, view counts, likes, favourites, and download support.
- Like and favourite interactions for authenticated users.
- Download tracking for styles marked as downloadable.
- Media uploads stored under the local `media/` directory.

## Tech Stack

- Backend: Django 6, Django REST Framework
- Frontend: React 18 loaded through CDN inside `templates/frontend.html`
- Styling: Tailwind CSS CDN utilities
- Database: PostgreSQL
- Media handling: Django `ImageField`/`FileField`, Pillow
- Configuration: `.env` file loaded with `python-dotenv`

There is no Node build step in this project. The frontend runs in the browser through CDN scripts for React, ReactDOM, Babel, and Tailwind.

## Project Structure

```text
StyleBook/
|-- accounts/              # Authentication API and custom user model
|-- common/                # Shared model helpers and game class choices
|-- styles/                # Style models, serializers, API views, tests
|-- StyleBook/             # Django project settings and URL routing
|-- templates/
|   `-- frontend.html      # React single-page frontend
|-- media/                 # Uploaded thumbnails and style images
|-- manage.py
|-- requirements.txt
`-- README.md
```

## Prerequisites

Install these before running the app:

- Python 3.13 or compatible Python 3 version supported by Django 6
- PostgreSQL
- Git
- Internet access in the browser for the frontend CDN scripts

## Download the Project

Clone the repository:

```bash
git clone https://github.com/Ivanivanov-it/StyleBook
cd StyleBook
```

If you received the project as a zip file, extract it and open a terminal in the extracted `StyleBook` folder.

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-this-with-a-local-development-secret
DB_NAME=stylebook
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=127.0.0.1
```

Do not commit real production secrets or database passwords.

## Database Setup

Create the PostgreSQL database:

```sql
CREATE DATABASE stylebook;
```

Make sure the user in `.env` has permission to connect to that database.

## Install and Run

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Optional Admin User

Create a Django admin account:

```bash
python manage.py createsuperuser
```

Then visit:

```text
http://127.0.0.1:8000/admin/
```

## Running Checks and Tests

Run Django's system checks:

```bash
python manage.py check
```

Run the styles app tests:

```bash
python manage.py test styles -v 1
```

## Main API Endpoints

Authentication:

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`

Styles:

- `GET /api/styles/`
- `POST /api/styles/`
- `GET /api/styles/{id}/`
- `PATCH /api/styles/{id}/`
- `DELETE /api/styles/{id}/`
- `GET /api/styles/mine/`
- `GET /api/styles/classes/`
- `POST /api/styles/{id}/like/`
- `POST /api/styles/{id}/favorite/`
- `POST /api/styles/{id}/download/`

## Uploaded Files

Uploaded thumbnails and gallery images are stored locally in:

```text
media/
```

During development, Django serves media files because `StyleBook/urls.py` includes `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`.

For production, configure a real media/static file server or object storage.

## Notes for Development

- The frontend is in `templates/frontend.html`, not in a separate React build folder.
- Because React, ReactDOM, Babel, and Tailwind are loaded from CDNs, the page may not render correctly without internet access.
- PostgreSQL is required by the current `DATABASES` setting.
- `DEBUG = True` is configured for development only.
- `ALLOWED_HOSTS = []` is suitable for local development, but must be configured before deployment.
- The app uses Django sessions and CSRF protection for authenticated POST/PATCH/DELETE requests.

## Troubleshooting

If `pip install -r requirements.txt` fails on the PostgreSQL driver, make sure PostgreSQL client libraries are available, or use the included `psycopg[binary]` package as listed.

If image uploads fail, confirm Pillow is installed:

```bash
python -m pip show Pillow
```

If the app cannot connect to the database, verify:

- PostgreSQL is running.
- The database named in `DB_NAME` exists.
- `DB_USER`, `DB_PASSWORD`, and `DB_HOST` are correct.
- Migrations have been applied with `python manage.py migrate`.

If the frontend appears blank, check that the browser can load the CDN scripts used in `templates/frontend.html`.
