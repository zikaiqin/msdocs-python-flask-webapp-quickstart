CREATE TABLE Visit (
    visitor_name VARCHAR(250),
    time DATETIME2 DEFAULT(GETDATE()),
    PRIMARY KEY(visitor_name, time)
)