# Student Record Management — Flask DevOps Case Study

## Features
- Home dashboard, Add Student, View Students, and About pages
- Add and delete student records
- In-memory storage (records reset on process restart)
- Health endpoint: `/health`

## Important settings
- Flask listens on port `5050`.
- Docker image repository used in the example: `nandini9334/student-records`.
- Kubernetes Service uses NodePort `30080`.
- Update the Docker Hub repository in `k8s/deployment.yaml` and `Jenkinsfile` if needed.

## Run locally
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Open http://localhost:5050.

## Docker
```powershell
docker build -t student-records:local .
docker run --rm -p 5050:5050 student-records:local
```
Open http://localhost:5050.

## Kubernetes (Docker Desktop Kubernetes)
Log in to Docker Hub first and push an image:
```powershell
docker login
docker build -t nandini9334/student-records:latest .
docker push nandini9334/student-records:latest
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/student-records-deployment
kubectl get pods
kubectl get service student-records-service
```
Open http://localhost:30080 when using Docker Desktop Kubernetes. If NodePort is not reachable in your setup:
```powershell
kubectl port-forward service/student-records-service 5051:5050
```
Then open http://localhost:5051.

## Jenkins setup overview
1. Install Jenkins plugins: Pipeline, Git, and GitHub integration (if using the GitHub webhook trigger).
2. Configure tools/agent so `git`, Python, Docker CLI, and `kubectl` are available to the Jenkins service account.
3. Add a Jenkins username/password credential with ID `dockerhub-creds`; use a Docker Hub access token as the password.
4. Configure kubeconfig/cluster access for the Jenkins service account. Confirm `kubectl get nodes` works in the same Windows account/service context used by Jenkins.
5. Create a Pipeline job from SCM, enter the GitHub repository URL, and select `Jenkinsfile`.
6. In the job configuration, enable **GitHub hook trigger for GITScm polling**.
7. In GitHub repository Settings → Webhooks → Add webhook, set Payload URL to `http://YOUR-JENKINS-HOST:8080/github-webhook/`, Content type to `application/json`, and choose **Just the push event**. Jenkins must be reachable from GitHub; `localhost` alone will not work as a public webhook endpoint.
8. Push a code change and inspect the Jenkins build log.

## Notes
- The Jenkinsfile uses Windows `bat` steps, suitable for a Windows Jenkins agent. For a Linux agent, replace `bat` with `sh` and adjust commands.
- Docker Hub image pushes require a public repository or valid credentials.
- A public webhook endpoint should be secured; do not expose Jenkins without appropriate authentication/network protections.
- In-memory data is not persistent. With two replicas, requests may reach different pods and show different records. This is intentional for the simple case-study version; use a database for real deployments.
