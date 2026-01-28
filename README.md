# About
This is a FastAPI backend with alembic and jwt authentication. Auth endpoints, schemas, and services have already been implemented along with dependencies for usage in other areas of 
the application. Users endpoints have also been minimally implemented and can easily be extended further for any project. Files are organized in a way that makes it very easy to follow
the code and has clear separation of concerns. 

# Getting Started
- Ensure you have Docker Desktop set up
- Simply open the root directory in the terminal then type: docker-compose up
- That should be enough to get everything up and running. If you experience issues, ensure that the requirements.txt files are properly updated. To update them, simply do uv pip freeze > requirements.txt aftering cding into the backend directory
- Also ensure you have uv installed (pip instal uv) in your global environment as this project uses uv package manager.
- You will need to create a .env file and provide all of the secrets as shown in the config.py file. This approach offers much more security than relying only on .env files.
- NOTE: In the config.py file within backend/core, there are redis configurations and those are primarily for celery usage. If you don't intent to use celery, then you can remove those. 

# Extensions
- Alembic commands have been provided. If you want to add further database tables, simply add the sqlalchemy classes in backend/core/entities.py and then run the alembic commands in commands.md
- If you want to add more functionality, the organization of this project is so integration can be done horizontally. If you need to add a new service, you simply create another folder in backend. That folder should have a router.py file and a schemas.py file. If the functionality is complicated, then you can add a service.py file to abstract away some of the details and keep router.py clean. Then, all you need to do is import this router in main and attach it to the fastapi app object. You can keep adding microservices like these very easily doing that same approach.
- If you want to add a frontend, simply create a /frontend directory in the root directory and then uncomment the frontend config in the docker-compose.yml file
- If you have a lot of tasks in your backend that take some time to do like an AI request or something of that nature, I recommend using Celery to manage tasks. For this, you can initialize the celery app within the backend/core directory with a celery_app.py file then uncomment the celery config in docker-compose.yml and use celery as you wish in other parts of the program via imports.
- Also, if you do end up using celery, I also recommend using flower to manage and view celery tasks. It is basically a GUI to see which tasks are currently being executed and which ones are not. You can also uncomment the flower section in the docker-compose.yml file if you wish to use that service too.
