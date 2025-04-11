CREATE TABLE website_updates (
    id VARCHAR(36) PRIMARY KEY,
    website VARCHAR(10) CHECK(website in ('TERHUNE', 'STULTS')) NOT NULL,
    fetch_time TIMESTAMP,
    contents JSON NOT NULL,
    previous_id VARCHAR(36),
    FOREIGN KEY (previous_id) REFERENCES website_updates(id),
    UNIQUE(previous_id)
);
