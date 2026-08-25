import random
from datetime import date, timedelta
from decimal import Decimal

from faker import Faker
from sqlalchemy import text

from app.core.database import engine


fake = Faker()

# Reproducible dataset
Faker.seed(42)
random.seed(42)


# ============================================================
# Dataset Size
# ============================================================

NUM_EMPLOYEES = 50
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 100
NUM_ORDERS = 5000
NUM_USERS = 20


# ============================================================
# Business Constants
# ============================================================

DEPARTMENTS = ["sales","finance","hr","support",]

REGIONS = ["North","South","East","West",]

CUSTOMER_SEGMENTS = ["enterprise","mid-market","smb",]

INDUSTRIES = ["Technology","Healthcare","Finance","Retail","Manufacturing","Education","Logistics","Telecommunications",]

PRODUCT_CATEGORIES = ["Analytics","Security","Collaboration","Infrastructure","AI",]

ORDER_STATUSES = ["completed","pending","cancelled",]

TRANSACTION_TYPES = ["payment","refund","chargeback",]

TRANSACTION_STATUSES = ["completed","pending","failed",]

CONTRACT_TYPES = ["standard","enterprise","custom",]


# ============================================================
# Utility Functions
# ============================================================

def random_date(start_date: date, end_date: date) -> date:
    """Return a random date between start_date and end_date."""

    days = (end_date - start_date).days

    return start_date + timedelta(
        days=random.randint(0, days)
    )


# ============================================================
# Employees
# ============================================================

def generate_employees(connection):
    print("Generating employees...")

    employees = []

    for _ in range(NUM_EMPLOYEES):

        department = random.choice(DEPARTMENTS)

        if department == "sales":
            role = random.choice(
                [
                    "Account Manager",
                    "Sales Manager",
                    "Sales Executive",
                ]
            )

        elif department == "finance":
            role = random.choice(
                [
                    "Financial Analyst",
                    "Finance Manager",
                    "Accountant",
                ]
            )

        elif department == "hr":
            role = random.choice(
                [
                    "HR Manager",
                    "HR Specialist",
                ]
            )

        else:
            role = random.choice(
                [
                    "Support Engineer",
                    "Support Manager",
                    "Customer Success Manager",
                ]
            )

        employees.append(
            {
                "name": fake.name(),
                "department": department,
                "region": random.choice(REGIONS),
                "role": role,
                "email": fake.unique.email(),
            }
        )

    connection.execute(
        text(
            """
            INSERT INTO employees
                (name, department, region, role, email)
            VALUES
                (:name, :department, :region, :role, :email)
            """
        ),
        employees,
    )

    result = connection.execute(
        text(
            """
            SELECT employee_id
            FROM employees
            ORDER BY employee_id
            """
        )
    )

    employee_ids = [row[0] for row in result]

    print(f"Inserted {len(employee_ids)} employees.")

    return employee_ids


# ============================================================
# Products
# ============================================================

def generate_products(connection):
    print("Generating products...")

    products = []

    price_ranges = {
        "Analytics": (500, 5000),
        "Security": (1000, 8000),
        "Collaboration": (200, 3000),
        "Infrastructure": (2000, 15000),
        "AI": (3000, 25000),
    }

    for _ in range(NUM_PRODUCTS):

        category = random.choice(PRODUCT_CATEGORIES)

        min_price, max_price = price_ranges[category]

        price = Decimal(
            str(round(random.uniform(min_price,max_price,),2,)))

        products.append(
            {
                "product_name": (f"{fake.company()} {category} Suite"),
                "category": category,
                "price": price,
            }
        )

    connection.execute(
        text(
            """
            INSERT INTO products
                (product_name, category, price)
            VALUES
                (:product_name, :category, :price)
            """
        ),
        products,
    )

    result = connection.execute(
        text(
            """
            SELECT product_id
            FROM products
            ORDER BY product_id
            """
        )
    )

    product_ids = [row[0] for row in result]

    print(f"Inserted {len(product_ids)} products.")

    return product_ids


# ============================================================
# Customers
# ============================================================

def generate_customers(connection, employee_ids):
    print("Generating customers...")

    customers = []

    for _ in range(NUM_CUSTOMERS):

        segment = random.choices(
            CUSTOMER_SEGMENTS,
            weights=[20, 30, 50],
            k=1,
        )[0]

        customers.append(
            {
                "company_name": fake.company(),
                "industry": random.choice(INDUSTRIES),
                "country": random.choice(
                    [
                        "India",
                        "United States",
                        "United Kingdom",
                        "Germany",
                        "Singapore",
                        "Australia",
                        "Canada",
                    ]
                ),
                "customer_segment": segment,
                "account_manager_id": random.choice(
                    employee_ids
                ),
            }
        )

    connection.execute(
        text(
            """
            INSERT INTO customers
                (
                    company_name,
                    industry,
                    country,
                    customer_segment,
                    account_manager_id
                )
            VALUES
                (
                    :company_name,
                    :industry,
                    :country,
                    :customer_segment,
                    :account_manager_id
                )
            """
        ),
        customers,
    )

    result = connection.execute(
        text(
            """
            SELECT customer_id
            FROM customers
            ORDER BY customer_id
            """
        )
    )

    customer_ids = [row[0] for row in result]

    print(f"Inserted {len(customer_ids)} customers.")

    return customer_ids


# ============================================================
# Orders + Order Items
# ============================================================

def generate_orders(connection,customer_ids,product_ids,):
    print("Generating orders...")

    # --------------------------------------------------------
    # Preload frequently accessed data.
    #
    # This avoids executing SELECT queries inside the
    # 5,000-order generation loop.
    # --------------------------------------------------------

    segment_by_customer = dict(
        connection.execute(
            text(
                """
                SELECT
                    customer_id,
                    customer_segment
                FROM customers
                """
            )
        ).all()
    )

    price_by_product = dict(
        connection.execute(
            text(
                """
                SELECT
                    product_id,
                    price
                FROM products
                """
            )
        ).all()
    )

    start_date = date(2025, 1, 1)
    end_date = date(2026, 8, 1)

    order_items = []

    for _ in range(NUM_ORDERS):

        customer_id = random.choice(customer_ids)

        segment = segment_by_customer[customer_id]

        # Enterprise customers can have larger orders.
        if segment == "enterprise":
            max_items = 5

        elif segment == "mid-market":
            max_items = 4

        else:
            max_items = 3

        selected_products = random.sample(
            product_ids,
            random.randint(1, max_items),
        )

        order_date = random_date(
            start_date,
            end_date,
        )

        status = random.choices(
            ORDER_STATUSES,
            weights=[85, 10, 5],
            k=1,
        )[0]

        total_amount = Decimal("0.00")

        item_data = []

        for product_id in selected_products:

            price = price_by_product[product_id]

            if segment == "enterprise":
                quantity = random.randint(5, 20)

            elif segment == "mid-market":
                quantity = random.randint(2, 10)

            else:
                quantity = random.randint(1, 5)

            total_amount += price * quantity

            item_data.append(
                {
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": price,
                }
            )

        # Insert order and retrieve generated ID.
        order_result = connection.execute(
            text(
                """
                INSERT INTO orders
                    (
                        customer_id,
                        order_date,
                        status,
                        total_amount
                    )
                VALUES
                    (
                        :customer_id,
                        :order_date,
                        :status,
                        :total_amount
                    )
                RETURNING order_id
                """
            ),
            {
                "customer_id": customer_id,
                "order_date": order_date,
                "status": status,
                "total_amount": total_amount,
            },
        )

        order_id = order_result.scalar_one()

        # Prepare order items for batch insertion.
        for item in item_data:

            order_items.append(
                {
                    "order_id": order_id,
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "unit_price": item["unit_price"],
                }
            )

    # Batch insert all order items.
    connection.execute(
        text(
            """
            INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                )
            VALUES
                (
                    :order_id,
                    :product_id,
                    :quantity,
                    :unit_price
                )
            """
        ),
        order_items,
    )

    print(f"Inserted {NUM_ORDERS} orders.")
    print(
        f"Inserted {len(order_items)} order items."
    )


# ============================================================
# Transactions
# ============================================================

def generate_transactions(
    connection,
    customer_ids,
):
    print("Generating transactions...")

    transactions = []

    start_date = date(2025, 1, 1)
    end_date = date(2026, 8, 1)

    for _ in range(NUM_ORDERS):

        transactions.append(
            {
                "customer_id": random.choice(
                    customer_ids
                ),
                "amount": Decimal(
                    str(
                        round(
                            random.uniform(
                                100,
                                50000,
                            ),
                            2,
                        )
                    )
                ),
                "transaction_type": random.choice(
                    TRANSACTION_TYPES
                ),
                "transaction_date": random_date(
                    start_date,
                    end_date,
                ),
                "status": random.choices(
                    TRANSACTION_STATUSES,
                    weights=[85, 10, 5],
                    k=1,
                )[0],
            }
        )

    connection.execute(
        text(
            """
            INSERT INTO transactions
                (
                    customer_id,
                    amount,
                    transaction_type,
                    transaction_date,
                    status
                )
            VALUES
                (
                    :customer_id,
                    :amount,
                    :transaction_type,
                    :transaction_date,
                    :status
                )
            """
        ),
        transactions,
    )

    print(
        f"Inserted {len(transactions)} transactions."
    )


# ============================================================
# Customer Contracts
# ============================================================

def generate_contracts(
    connection,
    customer_ids,
):
    print("Generating contracts...")

    # Pull segment alongside customer_id so contract type can correlate with it
    segment_by_customer = dict(
        connection.execute(
            text("SELECT customer_id, customer_segment FROM customers")
        ).all()
    )

    contracts = []

    for customer_id in customer_ids:
        segment = segment_by_customer[customer_id]

        # Enterprise customers skew toward custom/enterprise contracts;
        # SMBs skew toward standard. Still some randomness, not deterministic.
        if segment == "enterprise":
            contract_type = random.choices(
                CONTRACT_TYPES, weights=[10, 40, 50], k=1  # standard, enterprise, custom
            )[0]
        elif segment == "mid-market":
            contract_type = random.choices(
                CONTRACT_TYPES, weights=[30, 40, 30], k=1
            )[0]
        else:  # smb
            contract_type = random.choices(
                CONTRACT_TYPES, weights=[70, 20, 10], k=1
            )[0]

        if contract_type == "standard":
            refund_window = random.choice([15, 30])
        elif contract_type == "enterprise":
            refund_window = random.choice([30, 60])
        else:
            refund_window = random.choice([60, 90, 120])

        contracts.append({
            "customer_id": customer_id,
            "contract_type": contract_type,
            "refund_window_days": refund_window,
            "document_id": f"contract_{customer_id}",
            "signed_date": random_date(date(2025, 1, 1), date(2026, 6, 1)),
            "annual_value": Decimal(str(round(random.uniform(10000, 250000), 2))),
        })


    connection.execute(
        text(
            """
            INSERT INTO customer_contracts
                (
                    customer_id,
                    contract_type,
                    refund_window_days,
                    document_id,
                    signed_date,
                    annual_value
                )
            VALUES
                (
                    :customer_id,
                    :contract_type,
                    :refund_window_days,
                    :document_id,
                    :signed_date,
                    :annual_value
                )
            """
        ),
        contracts,
    )

    print(
        f"Inserted {len(contracts)} contracts."
    )


# ============================================================
# Users
# ============================================================

def generate_users(
    connection,
    employee_ids,
):
    print("Generating users...")

    roles = [
        "ADMIN",
        "SALES",
        "FINANCE",
        "HR",
    ]

    users = []

    for i in range(NUM_USERS):

        employee_id = random.choice(
            employee_ids
        )

        users.append(
            {
                "username": f"user_{i + 1}",
                "password_hash": "PLACEHOLDER",
                "role": random.choice(roles),
                "employee_id": employee_id,
            }
        )

    connection.execute(
        text(
            """
            INSERT INTO users
                (
                    username,
                    password_hash,
                    role,
                    employee_id
                )
            VALUES
                (
                    :username,
                    :password_hash,
                    :role,
                    :employee_id
                )
            """
        ),
        users,
    )

    print(
        f"Inserted {len(users)} users."
    )


# ============================================================
# Main
# ============================================================

def main():

    print("Starting AcmeCloud dataset generation...")

    with engine.begin() as connection:

        # ----------------------------------------------------
        # Clear existing generated data.
        #
        # Because of foreign keys, delete child tables first.
        # ----------------------------------------------------

        connection.execute(text("DELETE FROM audit_logs"))

        connection.execute(text("DELETE FROM users"))

        connection.execute(text("DELETE FROM customer_contracts"))

        connection.execute(text("DELETE FROM transactions"))

        connection.execute(text("DELETE FROM order_items"))

        connection.execute(text("DELETE FROM orders"))

        connection.execute(text("DELETE FROM customers"))

        connection.execute(text("DELETE FROM products"))

        connection.execute(text("DELETE FROM employees"))

        print("Existing data cleared.")

        # ----------------------------------------------------
        # Generate data in dependency order.
        # ----------------------------------------------------

        employee_ids = generate_employees(connection)

        product_ids = generate_products(connection)

        customer_ids = generate_customers(connection,employee_ids,)

        generate_orders(connection,customer_ids,product_ids,)

        generate_transactions(connection,customer_ids,)

        generate_contracts(connection,customer_ids,)

        generate_users(connection,employee_ids,)

    print("\nDataset generation completed successfully!")


if __name__ == "__main__":
    main()