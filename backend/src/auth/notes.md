Okay so for authentication, the endpoints under auth are used by the frontend and the dependencies are used by the backend to verify incoming requests which have access tokens in their headers. 

Auth endpoints:
- POST /auth/register (for new users)
- POST /auth/login    (for existing users)
- POST /auth/refresh  (for refreshing the access token)
- POST /auth/logout   (for logging out)


A note about Annotated type. It is basically a way to attach additional metadata to a type without changing the type. So say I have a Session but it is also a dependency which depends on some function foo and I must call foo in order to produce this object properly. 

In essence, before it would have been the following for a database session with the func as get_db:

    db: Session = Depends(get_db)       Now this is confusing because db is of type Session but also of type Depends so it is both a dependency & session

Now, we can simply use Annotated to indicate that db is just a Session but attach additional metadata to indicate that it also is a dependency which depends on get_db function being called to yield a database connection to use. 

Thus, we now declare it as -> DB_Session = Annotated[Session (actual type), Depends(get_db) (additional metadata/type)]

Now fastapi reads the above as: DB_Session is of type Session but I must call get_db to produce it so whenever you declare some object db:Db_Session, fastapi knows what to do. 
