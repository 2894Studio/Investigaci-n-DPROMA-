-- ─────────────────────────────────────────────────────────────────────────────
-- Roadmap DPROMA × 2894 — permitir quitar iniciativas de verdad
--
-- Se ejecuta UNA VEZ sobre una base que ya tiene schema.sql aplicado.
-- (En una base nueva no hace falta: schema.sql ya viene con esto.)
--
-- Hasta ahora no se podía borrar nada: quitar era archivar. Esto añade el
-- borrado definitivo, pero acotado:
--
--   · Solo se puede borrar lo que ya está archivado. Un «delete from
--     initiatives» lanzado contra la API no se lleva el roadmap por delante:
--     solo tocaría lo que alguien ya apartó a propósito.
--   · Al borrar una iniciativa se van con ella sus comentarios, sus entregables
--     y sus líneas de historial, en la misma operación y sin dejar restos.
--
-- Sigue sin poderse borrar un comentario suelto ni reescribir el historial.
-- ─────────────────────────────────────────────────────────────────────────────

-- 1. Que los hijos caigan con la iniciativa en vez de bloquear el borrado.
alter table deliverables drop constraint if exists deliverables_initiative_id_fkey;
alter table deliverables add  constraint deliverables_initiative_id_fkey
  foreign key (initiative_id) references initiatives(id) on delete cascade;

alter table comments drop constraint if exists comments_initiative_id_fkey;
alter table comments add  constraint comments_initiative_id_fkey
  foreign key (initiative_id) references initiatives(id) on delete cascade;

alter table changes drop constraint if exists changes_initiative_id_fkey;
alter table changes add  constraint changes_initiative_id_fkey
  foreign key (initiative_id) references initiatives(id) on delete cascade;

-- 2. Borrar, solo lo archivado.
drop policy if exists p_delete on initiatives;
create policy p_delete on initiatives for delete using (archived = true);
grant delete on table initiatives to anon, authenticated;

-- ── Comprobación ─────────────────────────────────────────────────────────────
-- Tiene que salir 1 (solo initiatives admite borrado) y las tres claves en
-- CASCADE. Si sale otra cosa, algo no se aplicó.
--
--   select
--     (select count(*) from information_schema.role_table_grants
--        where grantee='anon' and privilege_type='DELETE'
--          and table_name in ('initiatives','deliverables','comments','changes','settings'))
--                                                            as tablas_con_borrado,
--     (select count(*) from pg_constraint
--        where confdeltype='c' and conname like '%initiative_id_fkey%') as claves_en_cascada;
