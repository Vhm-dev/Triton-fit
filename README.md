# Biblioteca de Exercícios
Site estático, responsivo, sem dependências e compatível com GitHub Pages.

## Publicar
1. Crie um repositório público no GitHub chamado `biblioteca-exercicios`.
2. Envie `index.html`, `exercises.js` e a pasta `assets` para a raiz do repositório.
3. Em **Settings > Pages**, escolha **Deploy from a branch**, branch `main`, pasta `/(root)` e **Save**.
4. Abra `https://SEU-USUARIO.github.io/biblioteca-exercicios/` após a publicação.

## Links individuais
Exemplo: `https://SEU-USUARIO.github.io/biblioteca-exercicios/#exercicio/hip-thrust`.

## Adicionar GIFs autorizados
Coloque o arquivo em `assets/gifs/hip-thrust.gif` e, no registro correspondente de `exercises.js`, altere `gif:''` para `gif:'assets/gifs/hip-thrust.gif'`. Verifique os direitos de republicação antes de hospedar arquivos de terceiros.

## Adicionar exercícios
Copie um objeto de `exercises.js`, altere o `id` (único), nome, grupo, equipamento, resumo, passos e observações. A pesquisa e os filtros serão atualizados automaticamente.
