"""Create students and grades tables."""
from alembic import op
import sqlalchemy as sa


revision = "20260711_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("students", sa.Column("id", sa.String(length=36), nullable=False), sa.Column("full_name", sa.String(length=120), nullable=False), sa.Column("section", sa.String(length=3), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("uq_student_name_section_ci", "students", [sa.text("lower(full_name)"), sa.text("upper(section)")], unique=True)
    op.create_index(op.f("ix_students_full_name"), "students", ["full_name"], unique=False)
    op.create_index(op.f("ix_students_section"), "students", ["section"], unique=False)
    op.create_table("grades", sa.Column("id", sa.String(length=36), nullable=False), sa.Column("student_id", sa.String(length=36), nullable=False), sa.Column("subject", sa.String(length=40), nullable=False), sa.Column("score", sa.Float(), nullable=False), sa.CheckConstraint("score >= 0 AND score <= 100", name="ck_grade_score_range"), sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("student_id", "subject", name="uq_grade_student_subject"))
    op.create_index(op.f("ix_grades_student_id"), "grades", ["student_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_grades_student_id"), table_name="grades")
    op.drop_table("grades")
    op.drop_index("uq_student_name_section_ci", table_name="students")
    op.drop_index(op.f("ix_students_section"), table_name="students")
    op.drop_index(op.f("ix_students_full_name"), table_name="students")
    op.drop_table("students")
