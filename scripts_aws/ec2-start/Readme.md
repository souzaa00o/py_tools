Lambda Start ec2 Steps:

1. Criar a função lambda ec2-start.py
2. Adicionar a policy policy.json para a lambda function
3. Aumentar o tempo de timeout da lambda de 3seg para 2min, a insntancia ec2 demora mais 3 segundos para ser iniciada, logo o tempo padrão da lambda não é o suficiente, causando erro de timeout
4. Criar regra de execução lamda function no Cloudwatch, Cloudwatch/Events/Rules
