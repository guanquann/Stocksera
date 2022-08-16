import subprocess

subprocess.run("py --version")

print("Creating Database...")
subprocess.run("py scheduled_tasks/create_database.py")

print("Making Migrations...")
subprocess.run("py manage.py makemigrations users")

print("Migrating Database...")
subprocess.run("py manage.py migrate")

print("Creating Admin...")
subprocess.run("""py manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('ADMIN_USERNAME', 'admin_email@example.com', 'ADMIN_PW')" """)