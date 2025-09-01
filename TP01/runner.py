import yaml
import subprocess
import os

if not os.path.exists('output'):
    print("Création du répertoire : output")
    os.makedirs('output')

with open('pipeline.yaml', 'r') as file:
    pipeline = yaml.safe_load(file)

stages = pipeline.get('stages', [])
jobs = pipeline.get('jobs', {})

for stage in stages:
    print(f"\n🔹 Stage : {stage}")
    for job_name, job in jobs.items():
        if job.get('stage') == stage:
            print(f"  ▶️ Job : {job_name}")
            for command in job.get('script', []):
                print(f"    $ {command}")
                subprocess.run(command, shell=True, check=True)
