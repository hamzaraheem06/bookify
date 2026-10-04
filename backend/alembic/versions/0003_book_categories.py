"""Restore the revision referenced by existing local development databases.

The V1 baseline migration already owns the complete BookPilot schema.  Some
older local databases were stamped with this revision while the file was
missing from the repository, which made every Alembic command fail before it
could even inspect the database.  Keeping the revision in the chain makes
fresh installs and existing stamped databases resolvable without changing
the V1 schema a second time.
"""

from alembic import op

revision = "0003_book_categories"
down_revision = "0001_bookpilot_v1"
branch_labels = None
depends_on = None


def upgrade():
    # The baseline already creates the tables used by the current worker.
    pass


def downgrade():
    pass
