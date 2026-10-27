
pipeline {
    agent any

    stages {
        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test Application') {
            steps {
                bat 'python -m compileall -q app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t student-app:%BUILD_NUMBER% .'
            }
        }

        stage('Deploy Application') {
            steps {
                bat '''
                powershell -NoProfile -Command "docker rm -f student-app-container 2>$null; exit 0"
                docker run -d --name student-app-container -p 5000:5000 student-app:%BUILD_NUMBER%
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                bat '''
                powershell -NoProfile -Command "$r = Invoke-WebRequest -Uri 'http://localhost:5000/health' -TimeoutSec 15; if ($r.StatusCode -ne 200) { exit 1 }; Write-Output $r.Content"
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
