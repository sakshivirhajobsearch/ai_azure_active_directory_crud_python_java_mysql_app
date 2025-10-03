CREATE DATABASE IF NOT EXISTS ai_azure_active_directory;

USE ai_azure_active_directory;

CREATE TABLE IF NOT EXISTS azure_users (
    id VARCHAR(255) PRIMARY KEY,
    displayName VARCHAR(255),
    mail VARCHAR(255),
    jobTitle VARCHAR(255),
    risk VARCHAR(50)
);
