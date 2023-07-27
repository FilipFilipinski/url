"""

create_table_links

Revision ID: 6666e268c7d1
Creation date: 2023-07-25 18:34:32.790850

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "6666e268c7d1"
down_revision = "b2d1400908a1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """--sql
        CREATE TABLE links(
            l_uid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            owner_uid UUID NOT NULL,

            original_link TEXT NOT NULL,
            short_link TEXT NOT NULL,
            protected BOOLEAN NOT NULL,
            password TEXT,


            created_at TIMESTAMP WITH TIME ZONE NOT NULL,

            CONSTRAINT fk_user FOREIGN KEY(owner_uid) REFERENCES users(uid) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    op.execute(
        """--sql
        DROP TABLE links;
        """
    )
