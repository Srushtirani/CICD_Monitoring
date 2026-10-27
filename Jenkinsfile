
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
        stage('Train ML Model') {
            steps {
                bat 'python train_model.py'
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
        @echo off
        for /L %%i in (1,1,10) do (
            curl.exe --fail --silent --show-error http://127.0.0.1:5000/health
            if not errorlevel 1 exit /b 0
            timeout /t 2 /nobreak >nul
        )
        echo Health check failed after 10 attempts.
        exit /b 1
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
