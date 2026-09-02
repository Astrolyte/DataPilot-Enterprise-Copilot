CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    region VARCHAR(100),
    role VARCHAR(100),
    email VARCHAR(255) UNIQUE
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    country VARCHAR(100),
    customer_segment VARCHAR(50),
    account_manager_id INT REFERENCES employees(employee_id),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    status VARCHAR(50),
    total_amount NUMERIC(12,2) NOT NULL
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id),
    product_id INT NOT NULL REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL
);


CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    amount NUMERIC(12,2) NOT NULL,
    transaction_type VARCHAR(50),
    transaction_date DATE NOT NULL,
    status VARCHAR(50)
);

CREATE TABLE customer_contracts (
    contract_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    contract_type VARCHAR(50),
    refund_window_days INT,
    document_id VARCHAR(255),
    signed_date DATE,
    annual_value NUMERIC(12,2)
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    employee_id INT REFERENCES employees(employee_id),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    request_id VARCHAR(100),
    user_id INT REFERENCES users(user_id),
    role VARCHAR(50),
    query_text TEXT,
    route VARCHAR(20),
    tables_used TEXT[],
    sources_used TEXT[],
    latency_ms INT,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT now()
);