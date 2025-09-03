pipeline {
    agent any

    environment {
        ACR_NAME = 'sanskartestacr'                      // e.g. mytestacr
        ACR_LOGIN_SERVER = "sanskartestacr.azurecr.io"   // e.g. mytestacr.azurecr.io
        IMAGE_NAME = 'sample-aci-app'
        IMAGE_TAG = 'v1'
        RESOURCE_GROUP = 'test-rg'        // e.g. test-rg
        ACI_NAME = 'sample-aci'
        LOCATION = 'eastus'                           // pick your region
        AZURE_CLIENT_ID = credentials('azure-sp-client-id')    
        AZURE_CLIENT_SECRET = credentials('azure-sp-client-secret')
        AZURE_TENANT_ID = credentials('azure-sp-tenant-id')
        AZURE_SUBSCRIPTION_ID = "8b417db1-2052-4045-bea7-16fd2bc33574"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                bat """
                    echo Building Docker image...
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                    docker tag %IMAGE_NAME%:%IMAGE_TAG% %ACR_LOGIN_SERVER%/%IMAGE_NAME%:%IMAGE_TAG%
                """
            }
        }
        stage('Azure Login') {
            steps {
                script {
                    bat """
                        az login --service-principal \
                          --username $AZURE_CLIENT_ID \
                          --password $AZURE_CLIENT_SECRET \
                          --tenant $AZURE_TENANT_ID
                        az account set --subscription $AZURE_SUBSCRIPTION_ID
                    """
                }
            }
        }

        stage('Push to ACR') {
            steps {
                bat """
                    echo Login to ACR and push...
                    az acr login --name %ACR_NAME%
                    docker push %ACR_LOGIN_SERVER%/%IMAGE_NAME%:%IMAGE_TAG%
                """
            }
        }

        stage('Deploy to ACI') {
            steps {
                bat """
                    echo Fetching ACR credentials...
                    for /f "delims=" %%u in ('az acr credential show --name %ACR_NAME% --query "username" -o tsv') do set USERNAME=%%u
                    for /f "delims=" %%p in ('az acr credential show --name %ACR_NAME% --query "passwords[0].value" -o tsv') do set PASSWORD=%%p

                    echo Deploying container to Azure...
                    az container create ^
                      --resource-group %RESOURCE_GROUP% ^
                      --name %ACI_NAME% ^
                      --image %ACR_LOGIN_SERVER%/%IMAGE_NAME%:%IMAGE_TAG% ^
                      --registry-login-server %ACR_LOGIN_SERVER% ^
                      --registry-username %USERNAME% ^
                      --registry-password %PASSWORD% ^
                      --dns-name-label %ACI_NAME%-demo ^
                      --ports 80 ^
                      --os-type Linux ^
                      --location %LOCATION% ^
                      --cpu 1 ^
                      --memory 1.5 ^
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