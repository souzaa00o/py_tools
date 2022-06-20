Lambda Backup Dynamo tables Steps:

1. Criar a função lambda dynamoDb-bkp.py
2. Adicionar a policy policy.json para a lambda function
3. Criar tabela Dynamo com alguns items para teste
4. Criar regra de execução lamda function no Cloudwatch, Cloudwatch/Events/Rules
    4.1. Adicionar o nome da tabela para a variavel 'TableName' no 'Configure input' como Json text. Exemplo: {"TableName":"XPTO"}