-- ─────────────────────────────────────────────────────────────────────────────
-- Roadmap interactivo DPROMA × 2894 — esquema
--
-- Se ejecuta una sola vez, en el editor SQL de Supabase, antes que seed.sql.
--
-- La página del roadmap es estática y lleva la clave anónima a la vista, así que
-- cualquiera puede llamar a esta API directamente. Por eso las reglas de verdad
-- viven aquí y no en la interfaz:
--
--   · No existe permiso de DELETE en ninguna tabla. Nada se puede borrar, venga
--     de donde venga la petición. Quitar algo es marcar archived = true, y eso
--     se puede deshacer.
--   · El texto de un comentario es inmutable: sobre comments solo se concede
--     UPDATE de la columna archived, así que nadie puede reescribir lo que
--     escribió otra persona.
--   · El historial es de solo añadir: sobre changes no hay UPDATE ninguno.
--   · Las longitudes se limitan por constraint, no por el formulario.
-- ─────────────────────────────────────────────────────────────────────────────

-- ── Tablas ───────────────────────────────────────────────────────────────────

create table if not exists initiatives (
  id          uuid primary key default gen_random_uuid(),
  title       text not null check (char_length(title) between 1 and 160),
  note        text check (char_length(note) <= 1000),
  track       text not null check (track in ('negocio','discovery')),
  horizon     text not null check (horizon in ('corto','medio','largo')),
  -- Sin fecha = todavía no programada: vive en la bandeja lateral.
  start_date  date,
  end_date    date,
  status      text not null default 'no-iniciada'
              check (status in ('no-iniciada','en-curso','bloqueada','hecha')),
  archived    boolean not null default false,
  sort_order  integer not null default 0,
  rev         integer not null default 1,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  -- O las dos fechas o ninguna, y nunca al revés.
  constraint fechas_coherentes check (
    (start_date is null and end_date is null)
    or (start_date is not null and end_date is not null and end_date >= start_date)
  )
);

create table if not exists deliverables (
  id            uuid primary key default gen_random_uuid(),
  initiative_id uuid not null references initiatives(id),
  label         text not null check (char_length(label) between 1 and 120),
  url           text not null check (char_length(url) between 1 and 600
                                     and url ~ '^(https?://|/)'),
  archived      boolean not null default false,
  created_at    timestamptz not null default now()
);

create table if not exists comments (
  id            uuid primary key default gen_random_uuid(),
  initiative_id uuid not null references initiatives(id),
  author_name   text not null check (char_length(author_name) between 1 and 60),
  author_area   text check (char_length(author_area) <= 60),
  body          text not null check (char_length(body) between 1 and 2000),
  archived      boolean not null default false,
  created_at    timestamptz not null default now()
);

-- Historial. Solo se añade; no se edita ni se borra.
create table if not exists changes (
  id            bigint generated always as identity primary key,
  initiative_id uuid references initiatives(id),
  actor_name    text check (char_length(actor_name) <= 60),
  action        text not null check (char_length(action) between 1 and 40),
  detail        jsonb,
  created_at    timestamptz not null default now()
);

-- Ajustes de la herramienta; hoy solo el rango del calendario.
create table if not exists settings (
  key        text primary key check (char_length(key) between 1 and 60),
  value      jsonb not null,
  updated_at timestamptz not null default now()
);

create index if not exists comments_initiative_idx    on comments(initiative_id, created_at);
create index if not exists deliverables_initiative_idx on deliverables(initiative_id);
create index if not exists changes_created_idx        on changes(created_at desc);

-- ── rev y updated_at los lleva la base, no el cliente ────────────────────────
-- rev es un entero que sube en cada escritura. El cliente lo usa para detectar
-- que otra persona tocó la misma iniciativa antes que él (PATCH ... rev=eq.N):
-- si no coincide, no se actualiza ninguna fila y la interfaz avisa en lugar de
-- pisar el cambio ajeno. Un entero evita los líos de formato de un timestamp.

create or replace function touch_row() returns trigger
language plpgsql as $$
begin
  new.updated_at := now();
  new.rev        := old.rev + 1;
  new.created_at := old.created_at;   -- no se reescribe la fecha de alta
  return new;
end $$;

drop trigger if exists initiatives_touch on initiatives;
create trigger initiatives_touch before update on initiatives
  for each row execute function touch_row();

-- ── RLS ──────────────────────────────────────────────────────────────────────

alter table initiatives  enable row level security;
alter table deliverables enable row level security;
alter table comments     enable row level security;
alter table changes      enable row level security;
alter table settings     enable row level security;

drop policy if exists p_read   on initiatives;
drop policy if exists p_write  on initiatives;
drop policy if exists p_update on initiatives;
create policy p_read   on initiatives for select using (true);
create policy p_write  on initiatives for insert with check (true);
create policy p_update on initiatives for update using (true) with check (true);

drop policy if exists p_read   on deliverables;
drop policy if exists p_write  on deliverables;
drop policy if exists p_update on deliverables;
create policy p_read   on deliverables for select using (true);
create policy p_write  on deliverables for insert with check (true);
create policy p_update on deliverables for update using (true) with check (true);

drop policy if exists p_read   on comments;
drop policy if exists p_write  on comments;
drop policy if exists p_update on comments;
create policy p_read   on comments for select using (true);
create policy p_write  on comments for insert with check (true);
create policy p_update on comments for update using (true) with check (true);

drop policy if exists p_read  on changes;
drop policy if exists p_write on changes;
create policy p_read  on changes for select using (true);
create policy p_write on changes for insert with check (true);
-- changes no tiene política de UPDATE: el historial no se reescribe.

drop policy if exists p_read   on settings;
drop policy if exists p_write  on settings;
drop policy if exists p_update on settings;
create policy p_read   on settings for select using (true);
create policy p_write  on settings for insert with check (true);
create policy p_update on settings for update using (true) with check (true);

-- ── Permisos por columna ─────────────────────────────────────────────────────
-- Supabase concede ALL al rol anónimo por defecto. Se retira y se vuelve a dar
-- solo lo necesario. Esto es lo que hace que el borrado sea imposible y que el
-- texto de un comentario no se pueda reescribir.

revoke all on table initiatives, deliverables, comments, changes, settings
  from anon, authenticated;

grant usage on schema public to anon, authenticated;

grant select, insert on table initiatives to anon, authenticated;
grant update (title, note, track, horizon, start_date, end_date,
              status, archived, sort_order) on table initiatives to anon, authenticated;

grant select, insert on table deliverables to anon, authenticated;
grant update (label, url, archived) on table deliverables to anon, authenticated;

grant select, insert on table comments to anon, authenticated;
grant update (archived) on table comments to anon, authenticated;   -- el texto es inmutable

grant select, insert on table changes to anon, authenticated;        -- solo añadir
grant usage, select on all sequences in schema public to anon, authenticated;

grant select, insert on table settings to anon, authenticated;
grant update (value, updated_at) on table settings to anon, authenticated;

-- ── Comprobación ─────────────────────────────────────────────────────────────
-- Las cinco tablas deben salir con rowsecurity = true. Si alguna sale en false,
-- la base está abierta de par en par: no continúes.
--
--   select tablename, rowsecurity from pg_tables
--   where schemaname = 'public'
--     and tablename in ('initiatives','deliverables','comments','changes','settings');
