CREATE TABLE papper.literature (
                                   publication varchar(2000) NULL,
                                   pub_year varchar(2000) NULL,
                                   doi varchar(2000) NULL,
                                   id BIGINT auto_increment NOT NULL,
                                   CONSTRAINT literature_pk PRIMARY KEY (id)
)
    ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;
