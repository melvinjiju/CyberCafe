pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Debug: Show Structure') {
            steps {
                dir("${WORKSPACE}") {
                    sh 'echo "Current workspace: $(pwd)"'
                    sh 'ls -la'
                    sh 'ls -la project' // check Dockerfile is there
                    sh 'cat project/Dockerfile || echo "Dockerfile not found!"'
                    sh 'docker-compose --version || echo "Docker Compose not found"'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                dir("${WORKSPACE}") {
                    // Use --no-cache to force rebuild with updated Dockerfile
                    sh 'docker-compose -f docker-compose.yml build --no-cache'
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                dir("${WORKSPACE}") {
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
    }

    post {
        success {
            echo '✅ App deployed successfully at http://localhost:5000'
        }
        failure {
            echo '❌ Build or deploy failed. Check logs above.'
        }
    }
}
