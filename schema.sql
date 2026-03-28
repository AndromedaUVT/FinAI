

CREATE TABLE organizations (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR NOT NULL,
    slug        VARCHAR UNIQUE,
    status      VARCHAR DEFAULT 'active',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE app_users (
    id              SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    full_name       VARCHAR,
    email           VARCHAR NOT NULL UNIQUE,
    password_hash   VARCHAR NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR UNIQUE NOT NULL
);

INSERT INTO roles (name) VALUES ('admin'), ('editor'), ('cititor');

CREATE TABLE user_roles (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL,
    role_id         INT NOT NULL,
    organization_id INT NOT NULL
);

CREATE TABLE documents (
    id                  SERIAL PRIMARY KEY,
    organization_id     INT NOT NULL,
    uploaded_by         INT NOT NULL,
    file_name           VARCHAR,
    file_type           VARCHAR,
    file_path           VARCHAR,
    source_type         VARCHAR,
    ocr_status          VARCHAR DEFAULT 'pending',
    ai_parse_status     VARCHAR DEFAULT 'pending',
    validation_status   VARCHAR DEFAULT 'pending',
    uploaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vendors (
    id              SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    name            VARCHAR NOT NULL,
    tax_id          VARCHAR,
    address         VARCHAR,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE expense_categories (
    id              SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    name            VARCHAR NOT NULL,
    description     VARCHAR
);

CREATE TABLE expenses (
    id              SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    document_id     INT,
    vendor_id       INT,
    category_id     INT,
    expense_date    DATE,
    document_number VARCHAR,
    description     VARCHAR,
    currency        VARCHAR DEFAULT 'RON',
    subtotal_amount DECIMAL(10,2),
    tax_amount      DECIMAL(10,2),
    total_amount    DECIMAL(10,2),
    payment_method  VARCHAR,
    expense_type    VARCHAR,
    status          VARCHAR DEFAULT 'pending',
    entered_by      INT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE budget_rules (
    id                  SERIAL PRIMARY KEY,
    organization_id     INT NOT NULL,
    rule_name           VARCHAR,
    condition_json      TEXT,
    mapped_category_id  INT,
    project_code        VARCHAR,
    grant_code          VARCHAR,
    is_active           BOOLEAN DEFAULT TRUE
);

CREATE TABLE reports (
    id              SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    report_type     VARCHAR,
    period_start    DATE,
    period_end      DATE,
    generated_by    INT,
    file_path       VARCHAR,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id              SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    user_id         INT,
    action_type     VARCHAR,
    entity_type     VARCHAR,
    entity_id       INT,
    old_values      TEXT,
    new_values      TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE app_users ADD FOREIGN KEY (organization_id) REFERENCES organizations (id);
ALTER TABLE user_roles ADD FOREIGN KEY (user_id) REFERENCES app_users (id);
ALTER TABLE user_roles ADD FOREIGN KEY (role_id) REFERENCES roles (id);
ALTER TABLE user_roles ADD FOREIGN KEY (organization_id) REFERENCES organizations (id);
ALTER TABLE documents ADD FOREIGN KEY (organization_id) REFERENCES organizations (id);
ALTER TABLE documents ADD FOREIGN KEY (uploaded_by) REFERENCES app_users (id);
ALTER TABLE vendors ADD FOREIGN KEY (organization_id) REFERENCES organizations (id);
ALTER TABLE expense_categories ADD FOREIGN KEY (organization_id) REFERENCES organizations (id);
ALTER TABLE expenses ADD FOREIGN KEY (organization_id) REFERENCES organizations (id);
ALTER TABLE expenses ADD FOREIGN KEY (document_id) REFERENCES documents (id);
ALTER TABLE expenses ADD FOREIGN KEY (vendor_id) REFERENCES vendors (id);
ALTER TABLE expenses ADD FOREIGN KEY (category_id) REFERENCES expense_categories (id);
ALTER TABLE expenses ADD FOREIGN KEY (entered_by) REFERENCES app_users (id);
ALTER TABLE budget_rules ADD FOREIGN KEY (organization_id) REFERENCES organizations (id);
ALTER TABLE budget_rules ADD FOREIGN KEY (mapped_category_id) REFERENCES expense_categories (id);
ALTER TABLE reports ADD FOREIGN KEY (organization_id) REFERENCES organizations (id);
ALTER TABLE reports ADD FOREIGN KEY (generated_by) REFERENCES app_users (id);
ALTER TABLE audit_logs ADD FOREIGN KEY (organization_id) REFERENCES organizations (id);
ALTER TABLE audit_logs ADD FOREIGN KEY (user_id) REFERENCES app_users (id);