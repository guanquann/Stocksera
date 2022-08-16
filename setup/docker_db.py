import subprocess

subprocess.run("py --version")

print("Dockerizing...")
subprocess.run("docker-compose run --rm web python scheduled_tasks/create_database.py")
subprocess.run("docker-compose run --rm web python manage.py makemigrations users")
subprocess.run("docker-compose run --rm web python manage.py migrate")
subprocess.run("""docker-compose run --rm web  python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('ADMIN_USERNAME', 'admin_email@example.com', 'ADMIN_PW')" """)
