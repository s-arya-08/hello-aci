pipeline {
    agent any

    environment {
        ACR_NAME = 'cpxqa'                      // e.g. mytestacr
        ACR_LOGIN_SERVER = "cpxqa.azurecr.io"   // e.g. mytestacr.azurecr.io
        IMAGE_NAME = 'dev/cpx-re-auth'
        IMAGE_TAG = 'v1'
        RESOURCE_GROUP = 'CPX-DEV'        // e.g. test-rg
        ACI_NAME = 'dev-cpx-re-auth'
        LOCATION = 'eastus'                           // pick your region
        //AZURE_CLIENT_ID = credentials('azure-sp-client-id')    
        //AZURE_CLIENT_SECRET = credentials('azure-sp-client-secret')
        //AZURE_TENANT_ID = credentials('azure-sp-tenant-id')
        //AZURE_SUBSCRIPTION_ID = "8b417db1-2052-4045-bea7-16fd2bc33574"
    }

    stages {
        
        stage('Azure Login') {
            steps {
                script {
                    sh """
                    az login --tenant "e525ecf1-01af-442d-8f79-3574ddee69f7" --use-device-code
                                        """
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                sh """
                    echo "Building Docker image..."
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Push to ACR') {
            steps {
                sh """
                    echo "Login to ACR and push..."
                    az login --tenant "e525ecf1-01af-442d-8f79-3574ddee69f7" --use-device-code
                    az acr login --name ${ACR_NAME}
                    docker push ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Deploy to ACI') {
            steps {
                sh """
                    echo "Fetching ACR credentials..."
                    USERNAME=\$(az acr credential show --name \$ACR_NAME --query "username" -o tsv)
                    PASSWORD=\$(az acr credential show --name \$ACR_NAME --query "passwords[0].value" -o tsv)

                    echo "Deploying container to Azure..."
                    az container create \\
                    --resource-group \$RESOURCE_GROUP \\
                    --name \$ACI_NAME \\
                    --image \$ACR_LOGIN_SERVER/\$IMAGE_NAME:\$IMAGE_TAG \\
                    --registry-login-server \$ACR_LOGIN_SERVER \\
                    --registry-username \$USERNAME \\
                    --registry-password \$PASSWORD \\
                    --dns-name-label \${ACI_NAME}-demo \\
                    --ports 8000 \\
                    --os-type Linux \\
                    --location \$LOCATION \\
                    --cpu 1 \\
                    --memory 1.5 \\
                    --restart-policy Always
                """
            }
        }

    }

    post {
        success {
            echo "✅ Deployed successfully. Check your container URL."
        }
        failure {
            echo "❌ Pipeline failed. See logs."
        }
    }
}