Esta solução é apenas um Protótipo. Foi desenvolvido para responder ao seguinte desafio:

Uma pasta com fotos é partilhada entre amigos através do serviço MEO Cloud. 
Um problema comum é querer ver as fotos novas que os amigos partilham, mas não ter uma forma fácil de o fazer uma vez que não é possível saber quais as fotos que já foram vistas ou não.

A solução desejada é uma script que possa ser chamada da seguinte forma:
$ python script.py <path_to_folder>

O que a script deve fazer é encontrar todas as imagens que se encontrem na pasta dada como parâmetro e criar um ficheiro HTML que possa ser aberto para ver todas as imagens que não existiam da última vez que o script foi corrido.

Um exemplo:
- Pasta F tem 3 ficheiros, A, B e C.
- Corremos "python script.py F" pela primeira vez, e ele gera um ficheiro HTML onde podemos ver as imagens A, B e C.
- São acrescentados os ficheiro D e E à pasta F.
- Corremos novamente "python script.py F" e é gerado um ficheiro HTML onde podemos ver as imagens D e E.

Tecnologias obrigatórias:
- Python


Testado em Python 2.6.5. Dependencias em requirements.txt. 

Para configuração de parâmetros, editar o settings.py.  

Exemplo de uso:
$ python script.py /home/andre

Irá aparecer a informação no ecrã de quantas imagens foram adicionadas e será criado o ficheiro new_photos.html que poderá ser consultado.

Observações:
Não existe mecanismo de reset à base de dados, para limpar a memória das fotografias, simplesmente apagar o desafio.db

---
Personal Blog
http://andrelopes.me
