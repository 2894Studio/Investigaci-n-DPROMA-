/* Conexión a Supabase para el roadmap.
 *
 * La clave pública puede venir en dos formatos y los dos son seguros de
 * publicar aquí: el JWT clásico («anon public», empieza por ey…) y el nuevo
 * «publishable» (sb_publishable_…). Van a la vista en el navegador a propósito:
 * lo que protege los datos no es esconderlas, son las reglas RLS de
 * supabase/schema.sql.
 *
 * La clave secreta (service_role / sb_secret_…) NO va aquí ni en ningún archivo
 * del repositorio: esa se salta todas las reglas.
 *
 * Con los dos campos vacíos la herramienta arranca en modo local y lo avisa.
 * Ver docs/roadmap-supabase.md.
 */
window.ROADMAP_CONFIG = {
  url: 'https://ixrmqpejamfjoojmdzqt.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4cm1xcGVqYW1mam9vam1kenF0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyOTIwNjIsImV4cCI6MjEwMjg2ODA2Mn0.0Nb5hkRAH7pNLOk6O8ukKhpdaaD3mT7Yyrz5v9_sriM'
};
