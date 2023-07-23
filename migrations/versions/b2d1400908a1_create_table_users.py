from datetime import datetime
from argon2 import PasswordHasher

"""

create_table_users

Revision ID: b2d1400908a1
Creation date: 2023-07-23 22:11:38.490752

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = "b2d1400908a1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """--sql
            CREATE TABLE users(
                uid uuid DEFAULT uuid_generate_v4 (),
                
                email text NOT NULL,
                password text NOT NULL, 
                username text NOT NULL,
                
                created_at timestamp with time zone NOT NULL,
                
                PRIMARY KEY (id)
               );
       """
    )

    if "seed" in context.get_x_argument(as_dictionary=True):
        seed()


def downgrade() -> None:
    op.execute(
        """--sql
        DROP TABLE users;
        """
    )


def seed() -> None:
    ps = PasswordHasher
    op.execute(
        f"""--sql
            INSERT INTO users(email, password, username, created_at)
            VALUES('admin@admin.pl', '{ps.hash("pass")}', 'admin', '{datetime.now()}')
            """
    )
