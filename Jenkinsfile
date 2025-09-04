pipeline {
    agent any

    environment {
        ACR_NAME = 'cpxqa'                      // e.g. mytestacr
        ACR_LOGIN_SERVER = "cpxqa.azurecr.io"   // e.g. mytestacr.azurecr.io
        IMAGE_NAME = 'dev/cpx-re-auth'
        IMAGE_TAG = '-v${BUILD_NUMBER}'
        RESOURCE_GROUP = 'CPX-DEV'        // e.g. test-rg
        ACI_NAME = 'dev-cpx-re-auth'
        LOCATION = 'eastus'                           // pick your region
        AZURE_CLIENT_ID = credentials('cpx-azure-application-id')    
        AZURE_CLIENT_SECRET = credentials('cpx-azure-secret-value')
        AZURE_TENANT_ID = credentials('cpx-azure-tanent-ID')
        AZURE_SUBSCRIPTION_ID = credentials('cpx-azure-subscription-ID')
    }

    stages {
        
        stage('Azure Login') {
            steps {
                sh '''
                    az login --service-principal \
                        --username $AZURE_CLIENT_ID \
                        --password $AZURE_CLIENT_SECRET \
                        --tenant $AZURE_TENANT_ID

                    az account set --subscription $AZURE_SUBSCRIPTION_ID
                '''
            }
        }
        stage('Build and Push to ACR') {
            steps {
                sh '''
                    echo "Logging Docker into ACR..."
                    echo $AZURE_CLIENT_SECRET | docker login $ACR_LOGIN_SERVER -u $AZURE_CLIENT_ID --password-stdin

                    echo "Building image..."
                    docker build -t ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG} .
                    

                    echo "Pushing image..."
                    docker push ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}
                '''
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
                    --ports 80 \\
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