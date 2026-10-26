# API de Atividades da Mergington High School

Uma aplicação FastAPI super simples que permite que estudantes visualizem e se inscrevam em atividades extracurriculares.

## Funcionalidades

- Visualizar todas as atividades extracurriculares disponíveis
- Inscrever-se em atividades

## Primeiros Passos

1. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

2. Execute a aplicação:

   ```
   uvicorn src.app:app --reload
   ```

3. Abra seu navegador e acesse:
   - Documentação da API: http://localhost:8000/docs
   - Documentação alternativa: http://localhost:8000/redoc

## Endpoints da API

| Método | Endpoint                            | Descrição                                              |
| ------ | ----------------------------------- | ------------------------------------------------------ |
| GET    | `/activities`                       | Obtém atividades, emails inscritos e nomes disponíveis |
| POST   | `/activities/{activity_name}/signup` | Recebe `email` e `name` como parâmetros de consulta     |

## Modelo de Dados

A aplicação usa um modelo de dados simples com identificadores significativos:

1. **Activities** - Usa o nome da atividade como identificador:

   - Descrição
   - Horário
   - Número máximo de participantes permitidos
   - Lista de emails dos estudantes inscritos
   - Mapa `participant_names` que associa cada email ao nome informado na inscrição

Participantes já existentes sem nome associado continuam identificados pelo email na interface.

Todos os dados são armazenados em memória, o que significa que os dados serão resetados quando o servidor reiniciar.
