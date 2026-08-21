-- ─────────────────────────────────────────────────────────────────────────────
-- Roadmap interactivo DPROMA × 2894 — dejar el roadmap a cero
--
-- Borra TODO lo que se haya escrito en el roadmap (comentarios, historial,
-- estados, fechas movidas, iniciativas y entregables añadidos) y lo devuelve al
-- estado de partida del plan: 22 iniciativas, las 9 de corto plazo con sus
-- fechas propuestas y los 3 entregables ya enlazados.
--
-- Es para usarlo UNA VEZ, antes de abrir la herramienta al equipo. Después no,
-- porque se lleva por delante el trabajo de todo el mundo sin vuelta atrás:
-- esto no archiva, borra.
--
-- Se ejecuta en el SQL Editor de Supabase, con + New query, pegando todo y Run.
-- El borrado funciona aquí porque el editor entra como propietario de la base;
-- desde la página web nadie puede borrar nada, que es justo lo que se busca.
--
-- Si quieres guardar antes lo que hay: Table Editor → cada tabla → Export →
-- Export table as CSV.
-- ─────────────────────────────────────────────────────────────────────────────

-- El orden importa: primero lo que apunta a las iniciativas, luego ellas.
delete from changes;
delete from comments;
delete from deliverables;
delete from initiatives;
delete from settings where key = 'calendar_range';

-- Y se vuelve a sembrar el estado de partida.
insert into initiatives (id, title, note, track, horizon, start_date, end_date, sort_order) values
  ('c4d9bb5d-7e29-5f94-8bfc-8d91966f8d4a', 'Formación IA audiovisual & marketing', null, 'negocio', 'corto', '2026-08-17', '2026-09-04', 0),
  ('21d7a454-7339-57fe-881f-71e62489ed14', 'Seguimiento continuo con Jonathan (UX, UI, accesibilidad) por cada fase/área construida', 'Iniciativa continua: el roadmap la lista en corto y en medio plazo. Aqui va como una sola barra que cruza los dos horizontes.', 'negocio', 'corto', '2026-08-17', '2026-12-18', 10),
  ('d2f00d5f-9af5-5e7a-a305-2d8ee8b67edd', 'Acompañamiento en integración de IA en flujos del sistema de operaciones', 'Iniciativa continua: el roadmap la lista en corto y en medio plazo. Aqui va como una sola barra que cruza los dos horizontes.', 'negocio', 'corto', '2026-08-17', '2026-12-18', 20),
  ('b68f5046-f0bd-5583-bff1-1bf174c0ab1e', 'Área de atención al cliente - planteamiento', null, 'negocio', 'corto', '2026-09-07', '2026-10-02', 30),
  ('afbb5c29-ff64-52d0-96d1-b84ece68d371', 'Validación obligatoria de TO/VIN/orden de servicio al alta del cliente', null, 'discovery', 'corto', '2026-08-17', '2026-09-11', 40),
  ('03a6dd1e-faae-57b2-8b28-19ef5779f1fa', 'Definir alcance formal del rol de asistente de dirección antes de diseñar permisos', null, 'discovery', 'corto', '2026-08-24', '2026-09-11', 50),
  ('e86dfe96-0e1e-543e-9e7f-5f9914f8900a', 'Nomenclatura clara y consistente de perfiles en la herramienta', null, 'discovery', 'corto', '2026-09-14', '2026-10-02', 60),
  ('df3cac03-f9a3-51e1-b85b-ae65e45ac19c', 'Política de montos pre-aprobados', null, 'discovery', 'corto', '2026-09-21', '2026-10-09', 70),
  ('0557326c-d865-58d5-8a99-f5d29ab55223', 'Semáforo como patrón visual estándar en todos los módulos de la herramienta', null, 'discovery', 'corto', '2026-10-05', '2026-10-30', 80),
  ('e41e237b-06fd-5f90-b3f8-1da459c07c7a', 'Área de atención al cliente — estructura y capa digital', null, 'negocio', 'medio', null, null, 90),
  ('55048164-dd00-5773-9f3c-a22f8a2dfa5d', 'Formación IA para todo el equipo', null, 'negocio', 'medio', null, null, 100),
  ('b849ebb7-a958-5695-b32f-bc1b5a5d1f28', '"Área personal" del colaborador — contrato, nómina, vacaciones, asistencia, viáticos y firma digital en un solo lugar', null, 'discovery', 'medio', null, null, 110),
  ('83c4f32f-3b1e-5d8e-adbb-6263e5e144ca', 'Política de gobernanza de datos (dueños, permisos, fuente única de verdad)', null, 'discovery', 'medio', null, null, 120),
  ('8ba5a563-1584-5883-b524-f18f4aedf8ce', 'Portal de autoservicio para clientes/agencias con estatus de trámite en tiempo real', null, 'discovery', 'medio', null, null, 130),
  ('67dd0c39-f09d-541d-bbf3-9ec3ed952091', 'Proceso único (no por área) para cotización y viáticos', null, 'discovery', 'medio', null, null, 140),
  ('4e769d43-a117-5e4c-a96d-57da1058e57c', 'Tratar la evidencia fotográfica como dato de primera clase', null, 'discovery', 'medio', null, null, 150),
  ('47f31232-f863-51a8-9322-eaac5afe5b61', 'Disponibilizar información entre áreas / canales formales de comunicación', null, 'discovery', 'medio', null, null, 160),
  ('970e1ae0-f4b5-57c3-a68e-ba645806c465', 'Capacitación de IA segmentada por tipo de tarea, no por jerarquía', null, 'discovery', 'medio', null, null, 170),
  ('6a880533-d995-5654-b604-890bfa88e055', 'Abordar la desconfianza a la IA desde el uso ético y responsable con conocimiento y criterios claros para incentivar la adopción', null, 'discovery', 'medio', null, null, 180),
  ('21364ae7-2b4a-5366-b839-79cc25dbf686', 'Análisis de usabilidad de AMPECO', null, 'negocio', 'largo', null, null, 190),
  ('fccdbee5-8add-56a9-ba46-3328b93169e5', 'Auditoría inicial de la landing actual y estrategia de SEO/posicionamiento', null, 'negocio', 'largo', null, null, 200),
  ('709c822c-d513-5ff7-942f-814abd2d674c', 'Integración con Happy Robot para atención al cliente automatizada', null, 'negocio', 'largo', null, null, 210)
on conflict (id) do nothing;

-- Entregables ya publicados en el sitio, enlazados a la iniciativa que les toca.
insert into deliverables (initiative_id, label, url)
select v.iid::uuid, v.label, v.url
from (values
  ('21d7a454-7339-57fe-881f-71e62489ed14', 'Recomendaciones Login', '/entregables/recomendaciones-login'),
  ('b68f5046-f0bd-5583-bff1-1bf174c0ab1e', 'Atención al Cliente', '/entregables/atencion-al-cliente'),
  ('afbb5c29-ff64-52d0-96d1-b84ece68d371', 'Padrón de Clientes', '/entregables/padron-clientes')
) as v(iid, label, url)
where not exists (
  select 1 from deliverables d
  where d.initiative_id = v.iid::uuid and d.url = v.url
);

-- Ventana del calendario. La herramienta la amplía desde la interfaz.
insert into settings (key, value) values
  ('calendar_range', '{"start":"2026-08-01","end":"2026-12-31"}'::jsonb)
on conflict (key) do nothing;
