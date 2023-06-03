import subprocess

print("Dockerizing...")
subprocess.run("docker-compose build")
subprocess.run("docker-compose up")
