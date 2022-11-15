# steganography-api

API Simples criada para esteganografia.

Para fazer o uso, basta iniciar o servidor utilizando o comando
```uvicorn app:app --reload```

Com o servidor rodando já é possível enviar imagens para ele e começar a esconder mensagens dentro delas. Para enviar uma imagem, basta fazer um POST através da ferramenta que achar melhor. Uma opção é o comando ```curl -v -F file=@filename 127.0.0.1:8000/image```

Este endpoint responderá com o UUID da imagem dentro do servidor, com esse UUID é possível baixar a imagem, e também inserir uma mensagem secreta nela pelo endpoint ```/encode```.

Para utilizar o endpoint ```/encode``` use o formato ```curl --location --request POST 'localhost:8000/encode?_uuid=<UUID>&msg=<MENSAGEM>'```. Como resposta o servidor enviará um novo UUID referente a imagem com a mensagem secreta.

Para baixar uma imagem, o seguinte comando pode ser utilizado ```curl http://localhost:8000/image/<UUID> --output file.bmp```

E por fim, para obter o text contido dentro de uma imagem, é utilizado o endpoint ```/decode```, esse endpoint recebe apenas um UUID de uma imagem que já deve conter uma mensagem. O formato do request a ser feito é ```curl --location --request GET 'http://localhost:8000/decode?_uuid=<UUID>'```