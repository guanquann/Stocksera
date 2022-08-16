import subprocess

subprocess.run("py --version")

print("Dockerizing...")
subprocess.run("docker-compose build")
subprocess.run("docker-compose up")
