/* Conexión a Supabase para el roadmap.
 *
 * Con los dos campos vacíos la herramienta arranca en MODO LOCAL: funciona
 * entera, pero lo que se escribe se guarda solo en este navegador y nadie más
 * lo ve. La página lo avisa arriba mientras siga así.
 *
 * Para compartir de verdad, rellena los dos valores siguiendo
 * docs/roadmap-supabase.md. La clave anónima («anon public») está pensada para
 * ir a la vista en el navegador: lo que protege los datos son las reglas RLS
 * de supabase/schema.sql, no esconder la clave.
 *
 * La clave «service_role» NO va aquí ni en ningún archivo del repositorio.
 */
window.ROADMAP_CONFIG = {
  url: '',
  anonKey: ''
};
