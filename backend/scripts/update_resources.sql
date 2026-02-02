-- Update file_path for demo resources so "Open Resource" serves Markdown from /demo.
-- Target: user_data.resources (see app.models.core).
-- Run: psql -U techvault -d techvault -f backend/scripts/update_resources.sql
-- Or from backend/: psql $DATABASE_URL -f scripts/update_resources.sql

UPDATE user_data.resources
SET file_path = '/demo/design_tokens.md'
WHERE title = 'Design Tokens in Figma';

UPDATE user_data.resources
SET file_path = '/demo/postgresql_migrations.md'
WHERE title = 'PostgreSQL Migrations';

UPDATE user_data.resources
SET file_path = '/demo/react_typescript_setup.md'
WHERE title = 'React + TypeScript Setup';

UPDATE user_data.resources
SET file_path = '/demo/figma_components.md'
WHERE title = 'Figma Components';

UPDATE user_data.resources
SET file_path = '/demo/react_hooks_cheatsheet.md'
WHERE title = 'React Hooks Cheatsheet';
