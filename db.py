import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn


# --- USERS ---

def create_user(email, password_hash, full_name, organization_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO app_users (email, password_hash, full_name, organization_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (email, password_hash, full_name, organization_id))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def get_all_users(organization_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT id, email, full_name
            FROM app_users
            WHERE organization_id = %s AND is_active = TRUE;
        """
        cursor.execute(query, (organization_id,))
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT id, email, full_name, password_hash, organization_id
            FROM app_users
            WHERE email = %s AND is_active = TRUE;
        """
        cursor.execute(query, (email,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT id, email, full_name, organization_id, is_active
            FROM app_users
            WHERE id = %s;
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def update_user(user_id, full_name, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE app_users
            SET full_name = %s, email = %s
            WHERE id = %s;
        """
        cursor.execute(query, (full_name, email, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def deactivate_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE app_users
            SET is_active = FALSE
            WHERE id = %s;
        """
        cursor.execute(query, (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


# --- ORGANIZATIONS ---

def create_organization(name, slug):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO organizations (name, slug, status)
            VALUES (%s, %s, 'active')
            RETURNING id;
        """
        cursor.execute(query, (name, slug))
        org_id = cursor.fetchone()[0]
        conn.commit()
        return org_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def get_organization_by_id(org_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT id, name, slug, status
            FROM organizations
            WHERE id = %s;
        """
        cursor.execute(query, (org_id,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_all_organizations():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT id, name, slug, status
            FROM organizations
            WHERE status = 'active';
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def update_organization(org_id, name, status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE organizations
            SET name = %s, status = %s
            WHERE id = %s;
        """
        cursor.execute(query, (name, status, org_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


# --- ROLES ---

def assign_role(user_id, role_id, organization_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO user_roles (user_id, role_id, organization_id)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (user_id, role_id, organization_id))
        conn.commit()
        return cursor.fetchone()[0]
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def get_user_role(user_id, organization_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT r.name
            FROM user_roles ur
            JOIN roles r ON ur.role_id = r.id
            WHERE ur.user_id = %s AND ur.organization_id = %s;
        """
        cursor.execute(query, (user_id, organization_id))
        row = cursor.fetchone()
        return row[0] if row else None
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_all_roles():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name FROM roles;")
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


# --- DOCUMENTS ---

def create_document(organization_id, uploaded_by, file_name, file_type, file_path, source_type):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO documents
                (organization_id, uploaded_by, file_name, file_type, file_path, source_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (organization_id, uploaded_by, file_name, file_type, file_path, source_type))
        doc_id = cursor.fetchone()[0]
        conn.commit()
        return doc_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def get_documents_by_organization(organization_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT id, file_name, file_type, ocr_status, ai_parse_status, validation_status, uploaded_at
            FROM documents
            WHERE organization_id = %s
            ORDER BY uploaded_at DESC;
        """
        cursor.execute(query, (organization_id,))
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def update_document_status(document_id, ocr_status, ai_parse_status, validation_status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE documents
            SET ocr_status = %s, ai_parse_status = %s, validation_status = %s
            WHERE id = %s;
        """
        cursor.execute(query, (ocr_status, ai_parse_status, validation_status, document_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


# --- EXPENSES ---

def create_expense(organization_id, document_id, vendor_id, category_id,
                   expense_date, document_number, description, currency,
                   subtotal_amount, tax_amount, total_amount,
                   payment_method, expense_type, entered_by):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO expenses
                (organization_id, document_id, vendor_id, category_id,
                 expense_date, document_number, description, currency,
                 subtotal_amount, tax_amount, total_amount,
                 payment_method, expense_type, entered_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (
            organization_id, document_id, vendor_id, category_id,
            expense_date, document_number, description, currency,
            subtotal_amount, tax_amount, total_amount,
            payment_method, expense_type, entered_by
        ))
        expense_id = cursor.fetchone()[0]
        conn.commit()
        return expense_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def get_expenses_by_organization(organization_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT e.id, e.expense_date, e.total_amount, e.currency,
                   e.status, v.name AS vendor_name, ec.name AS category_name
            FROM expenses e
            LEFT JOIN vendors v ON e.vendor_id = v.id
            LEFT JOIN expense_categories ec ON e.category_id = ec.id
            WHERE e.organization_id = %s
            ORDER BY e.expense_date DESC;
        """
        cursor.execute(query, (organization_id,))
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_expenses_by_period(organization_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT e.id, e.expense_date, e.total_amount, e.currency,
                   e.status, v.name AS vendor_name, ec.name AS category_name
            FROM expenses e
            LEFT JOIN vendors v ON e.vendor_id = v.id
            LEFT JOIN expense_categories ec ON e.category_id = ec.id
            WHERE e.organization_id = %s
            AND e.expense_date BETWEEN %s AND %s
            ORDER BY e.expense_date DESC;
        """
        cursor.execute(query, (organization_id, start_date, end_date))
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def update_expense_status(expense_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE expenses
            SET status = %s
            WHERE id = %s;
        """
        cursor.execute(query, (status, expense_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()