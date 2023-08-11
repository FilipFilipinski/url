"""

create_table_stats

Revision ID: 4d8ff5bc488b
Creation date: 2023-07-25 18:51:25.209136

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "4d8ff5bc488b"
down_revision = "6666e268c7d1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """--sql
        CREATE TABLE stats(
            s_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            link_uid UUID NOT NULL,

            date TIMESTAMP WITH TIME ZONE NOT NULL,
            views INTEGER DEFAULT 0 NOT NULL,

            CONSTRAINT fk_link FOREIGN KEY(link_uid) REFERENCES links(l_uid) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    op.execute(
        """--sql
        DROP TABLE stats;
        """
    )
