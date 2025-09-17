pipeline {
    agent any

    parameters {
        string(name: 'ACR_NAME', defaultValue: 'cpxqa', description: 'Azure Container Registry name')
        string(name: 'ACR_LOGIN_SERVER', defaultValue: 'cpxqa.azurecr.io', description: 'ACR login server (e.g. myacr.azurecr.io)')
        string(name: 'IMAGE_NAME', defaultValue: 'dev/cpx-re-auth', description: 'Image name (e.g. myapp/service)')
        string(name: 'RESOURCE_GROUP', defaultValue: 'CPX-DEV', description: 'Azure resource group name')
        string(name: 'ACI_NAME', defaultValue: 'dev-cpx-re-auth', description: 'Container Instance name')
        string(name: 'LOCATION', defaultValue: 'eastus', description: 'Azure region for deployment')
        string(name: 'PORT', defaultValue: '80', description: 'Port your container listens on')
        string(name: 'OS', defaultValue: 'Linux', description: 'Operating System (Linux or Windows)')
        string(name: 'CPU', defaultValue: '1', description: 'Number of CPU cores')
        string(name: 'MEMORY', defaultValue: '1.5', description: 'Memory in GB')
    }

    environment {
        IMAGE_TAG = "build-v${BUILD_NUMBER}"

        // Azure credentials from Jenkins credentials store
        AZURE_CLIENT_ID       = credentials('cpx-azure-application-id')
        AZURE_CLIENT_SECRET   = credentials('cpx-azure-secret-value')
        AZURE_TENANT_ID       = credentials('cpx-azure-tanent-ID')
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
                sh """
                    echo "Logging Docker into ACR..."
                    echo $AZURE_CLIENT_SECRET | docker login $ACR_LOGIN_SERVER -u $AZURE_CLIENT_ID --password-stdin

                    echo "Building image..."
                    docker build -t ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG} .

                    echo "Pushing image..."
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
                    az container create \
                        --resource-group \$RESOURCE_GROUP \
                        --name \$ACI_NAME \
                        --image \$ACR_LOGIN_SERVER/\$IMAGE_NAME:\$IMAGE_TAG \
                        --registry-login-server \$ACR_LOGIN_SERVER \
                        --registry-username \$USERNAME \
                        --registry-password \$PASSWORD \
                        --dns-name-label \${ACI_NAME}-demo \
                        --ports \$PORT \
                        --os-type \$OS \
                        --location \$LOCATION \
                        --cpu \$CPU \
                        --memory \$MEMORY \
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
