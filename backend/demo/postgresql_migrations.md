# PostgreSQL Migrations

Best practices for schema changes with zero-downtime deployments.

## Naming convention

| Pattern        | Example                    |
|----------------|----------------------------|
| Create table   | `YYYYMMDD_create_users`    |
| Add column     | `YYYYMMDD_add_email_to_users` |
| Index          | `YYYYMMDD_idx_users_email` |

## Example migration (Alembic / raw SQL)

```sql
-- Add nullable column first (safe)
ALTER TABLE user_data.resources
  ADD COLUMN IF NOT EXISTS file_size_bytes BIGINT;

-- Backfill data, then add constraint if needed
-- ALTER TABLE user_data.resources ALTER COLUMN file_size_bytes SET NOT NULL;
```

## Rollback

Always write a reversible migration or document the rollback steps.
