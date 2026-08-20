# Conectar el roadmap a Supabase

El roadmap de `/roadmap` funciona sin configurar nada, pero en **modo local**: lo que cada
persona escribe se guarda solo en su navegador y nadie más lo ve. La página lo avisa arriba
mientras siga así.

Estos son los pasos para que el equipo comparta de verdad iniciativas, estados y
comentarios. Son unos cinco minutos y no hace falta saber SQL.

## 1. Crear el proyecto

1. Entra en <https://supabase.com> y crea una cuenta (el plan gratuito sobra para esto).
2. **New project**. Ponle un nombre — por ejemplo `dproma-roadmap` — y elige la región más
   cercana a México (`East US` o `West US` van bien).
3. Guarda la contraseña de base de datos que te pida en un gestor de contraseñas. No se
   usa para esto, pero es la única vez que te la enseña.
4. Espera a que termine de crearse, un par de minutos.

## 2. Crear las tablas

1. En el menú lateral, **SQL Editor** → **New query**.
2. Copia el contenido entero de `supabase/schema.sql` y pégalo. **Run**.
3. Nueva consulta. Copia el contenido entero de `supabase/seed.sql`. **Run**.

La siembra deja las 22 iniciativas del plan con las de corto plazo ya fechadas. Ejecutarla
dos veces no duplica nada.

## 3. Comprobar que la base no queda abierta

Esto no te lo saltes. Nueva consulta, pega esto y ejecútalo:

```sql
select tablename, rowsecurity from pg_tables
where schemaname = 'public'
  and tablename in ('initiatives','deliverables','comments','changes','settings');
```

Las cinco filas tienen que salir con `rowsecurity` en **true**. Si alguna sale en `false`,
algo falló al ejecutar `schema.sql`: vuelve a lanzarlo entero antes de seguir.

## 4. Copiar las dos claves

1. **Project Settings** (el engranaje) → **API**.
2. Copia **Project URL** — algo como `https://abcdefgh.supabase.co`.
3. Copia la clave **anon public**. Es una cadena larga que empieza por `eyJ…`.

## 5. Pegarlas en el sitio

Abre `web/roadmap-config.js` y rellena los dos valores:

```js
window.ROADMAP_CONFIG = {
  url: 'https://abcdefgh.supabase.co',
  anonKey: 'eyJhbGciOi…'
};
```

Sube el cambio. En cuanto Vercel despliegue, el aviso amarillo de «Modo local» desaparece y
lo que escriba cualquiera lo ven todos.

## Sobre las claves

**La clave `anon public` va a la vista en la página, y está bien.** Es su función: viaja en
el navegador de cualquiera que abra el roadmap. Lo que protege los datos no es esconderla,
son las reglas de seguridad de `schema.sql`:

- No existe permiso de borrado en ninguna tabla, así que nadie puede vaciar el roadmap ni
  llamando a la API por su cuenta. Quitar algo es archivarlo, y se recupera desde el
  historial.
- El texto de un comentario no se puede reescribir: solo se puede archivar.
- El historial es de solo añadir.
- Las longitudes máximas las impone la base, no el formulario.

**La clave `service_role` no se pone aquí ni en ningún archivo del repositorio.** Esa sí se
salta todas las reglas anteriores. Si alguna vez se filtra, hay que rotarla desde el panel
de Supabase.

## Lo que queda abierto, a propósito

Cualquiera con el enlace puede comentar y mover fechas: fue una decisión deliberada para
que el equipo no tenga que gestionar cuentas. Todo cambio queda firmado con el nombre que
la persona escribe y con la hora, y nada se borra, así que cualquier destrozo es visible y
reversible desde el historial. Lo que no hay es forma de impedirlo por adelantado.

Si más adelante conviene cerrarlo, las dos salidas naturales son pedir una clave compartida
para escribir, o pasar a login por correo con Supabase Auth. Ninguna de las dos obliga a
rehacer los datos.

## Copia de seguridad

Supabase hace copias automáticas en el plan gratuito, pero conviene exportar de vez en
cuando: **Table Editor** → cada tabla → **Export to CSV**.
