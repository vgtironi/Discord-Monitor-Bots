# Discord-Monitor-Bots
O objetivo desse projeto é criar 3 bots do discord que notificam re-stocks de produtos listados em planilhas no drive para os sites da Nike, Maze e Artwalk.

# Referências necessárias
Antes de tudo, ver essas referências é a parte mais importante para compreender o projeto.
- [Setup Discord Python Bot](https://www.youtube.com/playlist?list=PLqq1dWUDSxy4g1B3h12qPnHb0QsI6T7XG)
- [Setup Google Sheets API](https://youtu.be/cnPlKLEGR7E)

# Sobre os arquivos
## Dependências
Todas podem ser instaladas com pip install
- discord.py (na referencia é usada outra versão, mas nos arquivos é usada a "discord.py")
- bs4
- requests
- gspread
- oauth2client
## Credenciais
Agumas credenciais são necessárias para rodar os scripts, mas elas estão separadas e explicadas com comentários. <br>
Porém, seguindo as Referências necessárias é possível compreender todas essas credenciais.
## Planilhas
[As planilhas do drive usadas no código seguiam o seguinte padrão](https://prnt.sc/upntb4)
## NikeTesting.py
Com o site da nike não consegui uma forma estável de ter o estoque dos itens... 
- Como exemplo: [na primeira execução da certo, mas depois ele pega outros tamanhos, como se armazenasse um cache na própria nike](https://prnt.sc/upnoac) <br>
Por esse motivo não existe ainda o script do bot responsável pelo bot da nike
