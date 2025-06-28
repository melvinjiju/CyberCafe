pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Verify Dockerfile') {
            steps {
                dir("${WORKSPACE}/project") {
                    echo '🔍 Showing Dockerfile content from ./project directory...'
                    sh 'cat Dockerfile'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                dir("${WORKSPACE}") {
                    echo '🔨 Building images with --no-cache...'
                    sh 'docker-compose -f docker-compose.yml build --no-cache'
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                dir("${WORKSPACE}") {
                    echo '🚀 Starting containers...'
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
            echo '❌ Build or deploy failed. Please check above logs.'
        }
    }
}
