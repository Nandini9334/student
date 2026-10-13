pipeline {
    agent any

    environment {
        // Replace with your Docker Hub username/repository if different.
        IMAGE_NAME = 'nandini9334/student-records'
        K8S_NAMESPACE = 'default'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Flask files') {
            steps {
              bat '"C:\\Users\\POTTA NANDINI\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m py_compile app.py'
            }
        }

        stage('Build Docker image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Push image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    bat 'echo %DOCKERHUB_TOKEN%| docker login -u %DOCKERHUB_USER% --password-stdin'
                    bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'docker push %IMAGE_NAME%:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Set up kubectl and cluster credentials on the Jenkins agent first.
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl apply -f k8s/service.yaml'
                bat 'kubectl set image deployment/student-records-deployment student-records=%IMAGE_NAME%:%BUILD_NUMBER% -n %K8S_NAMESPACE%'
                bat 'kubectl rollout status deployment/student-records-deployment -n %K8S_NAMESPACE% --timeout=120s'
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs above.'
        }
    }
}
