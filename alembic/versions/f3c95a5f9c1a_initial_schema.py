import sqlalchemy as sa

from alembic import op

revision = "f3c95a5f9c1a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("phone", sa.String(length=50), nullable=False),
    )
    op.create_index(op.f("ix_patients_id"), "patients", ["id"], unique=False)
    op.create_index(op.f("ix_patients_email"), "patients", ["email"], unique=True)

    op.create_table(
        "doctors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("specialization", sa.String(length=255), nullable=False),
    )
    op.create_index(op.f("ix_doctors_id"), "doctors", ["id"], unique=False)

    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("doctor_id", sa.Integer(), nullable=False),
        sa.Column("appointment_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("appointment_end", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.ForeignKeyConstraint(["doctor_id"], ["doctors.id"]),
    )
    op.create_index(op.f("ix_appointments_id"), "appointments", ["id"], unique=False)
    op.create_index(op.f("ix_appointments_patient_id"), "appointments", ["patient_id"], unique=False)
    op.create_index(op.f("ix_appointments_doctor_id"), "appointments", ["doctor_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_appointments_doctor_id"), table_name="appointments")
    op.drop_index(op.f("ix_appointments_patient_id"), table_name="appointments")
    op.drop_index(op.f("ix_appointments_id"), table_name="appointments")
    op.drop_table("appointments")
    op.drop_index(op.f("ix_doctors_id"), table_name="doctors")
    op.drop_table("doctors")
    op.drop_index(op.f("ix_patients_email"), table_name="patients")
    op.drop_index(op.f("ix_patients_id"), table_name="patients")
    op.drop_table("patients")
