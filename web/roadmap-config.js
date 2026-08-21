/* Conexión a Supabase para el roadmap.
 *
 * La clave «publishable» está pensada para ir a la vista en el navegador: es lo
 * que hace funcionar la página para cualquiera que la abra. Lo que protege los
 * datos no es esconderla, son las reglas RLS de supabase/schema.sql.
 *
 * La clave «secret» (sb_secret_…, antes service_role) NO va aquí ni en ningún
 * archivo del repositorio: esa se salta todas las reglas.
 *
 * Con los dos campos vacíos la herramienta arranca en modo local y lo avisa.
 * Ver docs/roadmap-supabase.md.
 */
window.ROADMAP_CONFIG = {
  url: 'https://ixrmqpejamfjoojmdzqt.supabase.co',
  anonKey: 'sb_publishable_hhtUiy24fnUK4E8OxZnJ2A_FgbTzwBS'
};
