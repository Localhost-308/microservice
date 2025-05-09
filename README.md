# Microservice

## Portabilidade
A portabilidade está disponível para todos os usuários (exceto os usuários admin). Com essa recurso, o usuário pode utilizar seus dados em outras aplicações, como, por exemplo, dados para login (e-mail, nome, ...) e/ou dados relacionados às suas áreas (emissão de CO₂, árvores plantadas, ...) para realizar análises em outras plataformas.

#### Como funciona? 
A aplicação externa deve fazer uma requisição para a API de portabilidade (http://127.0.0.1:5000/portability/) e enviar como parâmetros a URL para o callback (o callback é uma funcionalidade que retorna à API que fez a requisição) e a public key. Após isso, a API solicitará que o usuário faça o login na API principal. Em seguida, o usuário poderá escolher os dados que deseja exportar. Pronto! Os dados serão enviados, de forma criptografada, para a URL de callback definida na chamada da API de portabilidade.
