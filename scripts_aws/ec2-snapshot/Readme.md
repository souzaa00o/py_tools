Lambda Create Snapshot Steps:

    1. Criar a instancia ec2 com a tag "backup" com o valor "true" 
    2. Criar lambda com o codigo ec2-snapshot.py
    3. Adicionar a policy policy.json para a lambda function 
    4. Aumentar o tempo de timeout da lambda de 3seg para 1min, o snapshot demora mais 3 segundos para ser criado, logo o tempo padrao da lambda não é o suficiente, causando erro de timeout
    5. Agendar tempo de trigger Lambda em Cloudwatch > Events > Rules 

