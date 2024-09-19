# EmprestAqui - Testes

Este projeto contém testes automatizados para as classes `Comment`, `Item`, `Person` e `Request`. Os testes foram implementados utilizando o framework `pytest`.

## Arquivos de Teste

Existem quatro arquivos de teste neste projeto, cada um responsável por testar uma classe específica:

1. **test_comment.py**: Contém testes para a classe `Comment`.
2. **test_item.py**: Contém testes para a classe `Item`.
3. **test_person.py**: Contém testes para a classe `Person`.
4. **test_request.py**: Contém testes para a classe `Request`.

## Executando os Testes

Para executar todos os testes de uma vez, siga os passos abaixo:

1. Certifique-se de que você tem todas as dependências instaladas. Caso contrário, instale-as utilizando o arquivo `requirements.txt` com o seguinte comando:

   ```bash
   pip install -r requirements.txt
   ```

2. Navegue até a pasta que contém os arquivos de teste.

3. Execute o seguinte comando para rodar todos os testes:

   ```bash
   python -m pytest test_*.py
   ```

Este comando executará todos os testes presentes nos arquivos que começam com `test_`.

## Observações

- Certifique-se de estar no ambiente virtual correto (se você estiver usando um).
- Todos os testes devem passar com sucesso se o código estiver funcionando corretamente.

Se você encontrar algum erro durante a execução dos testes, verifique o código correspondente e os testes para identificar e corrigir o problema.