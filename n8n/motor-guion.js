/* Motor del guion — bot de primer contacto DPROMA (PoC WhatsApp)
 * Fuente única de la lógica de conversación. Se inserta tal cual en:
 *   - n8n/demo-bot-whatsapp-dproma.json (nodo Code «Motor del guion»)
 *   - web/entregables/poc-whatsapp-primer-contacto.html (simulador)
 * mediante scripts/build-poc-whatsapp.py. Edita aquí y vuelve a correr el script.
 * Sin dependencias: JavaScript puro, sin red, sin credenciales.
 */
const MOTOR = (() => {
  const AGENCIAS = [
    { clave: 'changan del valle', nombre: 'Changan del Valle', slug: 'changan-del-valle', marca: 'Changan' },
  ];
  const PALABRAS_ASESOR = /\b(asesor|humano|persona|llamar|ll[aá]mame|hablar con alguien)\b/i;
  const PREGUNTA_LIBRE = /\?|cu[aá]nto|precio|costo|cuesta/i;

  const P = {
    INMUEBLE: { tipo: 'botones', texto: 'Gracias, {nombre}. ¿Dónde quieres instalar el cargador?',
      opciones: [ { id: 'casa', label: 'Casa', claves: ['casa'] },
                  { id: 'condominio', label: 'Condominio / edificio', claves: ['condominio', 'edificio', 'depa', 'departamento'] },
                  { id: 'empresa', label: 'Empresa / flotilla', claves: ['empresa', 'flotilla', 'negocio', 'oficina'] } ] },
    VEHICULO: { tipo: 'lista', texto: '¿Qué auto tienes o vas a recibir?',
      opciones: [ { id: 'Changan Dipal S07', label: 'Changan Dipal S07', claves: ['dipal', 'changan'] },
                  { id: 'BYD', label: 'BYD', claves: ['byd'] },
                  { id: 'MG', label: 'MG', claves: ['mg'] },
                  { id: 'Tesla', label: 'Tesla', claves: ['tesla'] },
                  { id: 'otro', label: 'Otro…', claves: ['otro'] } ] },
    VEHICULO_OTRO: { tipo: 'texto', texto: '¿Cuál? Escríbelo, por favor (marca y modelo).' },
    DOMICILIO: { tipo: 'texto', texto: '¿Cuál es el domicilio de la instalación? Calle, número, colonia y código postal.\nSi te queda más fácil, también puedes mandar tu ubicación 📍' },
    DOMICILIO_CP: { tipo: 'texto', texto: '¡Gracias! ¿Y el código postal? (5 dígitos)' },
    METROS: { tipo: 'lista', texto: 'Más o menos, ¿qué distancia hay del tablero eléctrico al lugar donde vas a cargar el auto? 📏 Un auto mide unos 4.5 m.',
      opciones: [ { id: 'hasta_10', label: 'Hasta 10 m', claves: ['hasta 10', 'menos de 10'] },
                  { id: '11_20', label: 'De 11 a 20 m', claves: ['11 a 20', '11-20'] },
                  { id: '21_30', label: 'De 21 a 30 m', claves: ['21 a 30', '21-30'] },
                  { id: 'mas_30', label: 'Más de 30 m', claves: ['mas de 30', 'más de 30'] },
                  { id: 'no_se', label: 'No sé', claves: ['no se', 'no sé', 'ni idea'] } ] },
    MEDIDOR: { tipo: 'botones', texto: '¿Quieres un medidor de CFE independiente solo para el cargador, o conectarlo a tu luz de siempre?',
      opciones: [ { id: 'si', label: 'Medidor nuevo', claves: ['nuevo', 'independiente', 'si', 'sí'] },
                  { id: 'no', label: 'Mi luz actual', claves: ['actual', 'mi luz', 'no'] },
                  { id: 'no_se', label: 'No sé', claves: ['no se', 'no sé'] } ] },
    FOTO_TABLERO: { tipo: 'foto', foto: 'tablero', texto: '¿Nos mandas una foto de tu tablero eléctrico (la caja con los interruptores)? Así la cotización sale más precisa.',
      opciones: [ { id: 'despues', label: 'Enviar después', claves: ['despues', 'después', 'luego', 'no tengo'] } ] },
    FOTO_SITIO: { tipo: 'foto', foto: 'sitio_recorrido', texto: 'Ahora una foto del lugar donde quieres cargar el auto y, si se puede, del camino por donde iría el cable.',
      opciones: [ { id: 'despues', label: 'Enviar después', claves: ['despues', 'después', 'luego', 'no tengo'] } ] },
    FOTO_MEDIDOR: { tipo: 'foto', foto: 'medidor', texto: 'Y por último, una foto de tu medidor de CFE.',
      opciones: [ { id: 'despues', label: 'Enviar después', claves: ['despues', 'después', 'luego', 'no tengo'] } ] },
  };
  const ORDEN = ['INMUEBLE', 'VEHICULO', 'DOMICILIO', 'METROS', 'MEDIDOR', 'FOTO_TABLERO', 'FOTO_SITIO', 'FOTO_MEDIDOR'];
  const NOMBRE_INMUEBLE = { casa: 'Casa particular', condominio: 'Residencial', empresa: 'Empresa / flotilla' };

  const norm = s => String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').trim();
  const titulo = s => String(s).trim().replace(/\s+/g, ' ').replace(/(^|\s)\S/g, c => c.toUpperCase());

  function nuevoEstado() {
    return { paso: 'NUEVO', datos: {}, fallos: 0, fotos: [], fotosPendientes: [], origen: 'directa', agencia: null,
             terminado: false, estado_bot: null, motivo_humano: null, eventos: [] };
  }

  function pregunta(clave, est) {
    const p = P[clave];
    return { clave, tipo: p.tipo, texto: p.texto.replace('{nombre}', (est.datos.nombre || '').split(' ')[0]),
             opciones: (p.opciones || []).map(o => ({ id: o.id, label: o.label })) };
  }

  function siguiente(clave, est) {
    let i = ORDEN.indexOf(clave) + 1;
    if (ORDEN[i] === 'VEHICULO' && est.agencia) i++;           // la agencia ya dice la marca
    return ORDEN[i] || 'COMPLETO';
  }

  function elegir(clave, entrada) {
    const ops = P[clave].opciones || [];
    if (entrada.opcion) return ops.find(o => o.id === entrada.opcion) || null;
    const t = norm(entrada.texto);
    if (!t) return null;
    if (/^\d+$/.test(t)) return ops[Number(t) - 1] || null;
    // Gana la clave más larga que aparezca como palabra completa («no sé» antes que «no»).
    let mejor = null, largo = 0;
    for (const o of ops) for (const k of o.claves) {
      const nk = norm(k).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      if (new RegExp(`(^|[^a-z0-9])${nk}($|[^a-z0-9])`).test(t) && nk.length > largo) { mejor = o; largo = nk.length; }
    }
    return mejor;
  }

  function evento(est, tipo, detalle, t) { est.eventos.push({ tipo, detalle: detalle == null ? null : String(detalle), t: t || null }); }

  function aHumano(est, motivo, texto) {
    est.paso = 'HUMANO'; est.terminado = true; est.estado_bot = 'HUMANO'; est.motivo_humano = motivo;
    evento(est, 'derivado_humano', motivo);
    return [{ tipo: 'texto', texto }];
  }

  function fallo(est, clave) {
    est.fallos++;
    evento(est, 'no_reconocido', clave);
    if (est.fallos >= 2) return aHumano(est, 'no_reconocido', 'Mejor te comunico con alguien del equipo para no hacerte perder tiempo. Bernardo te escribe en cuanto pueda 🙂');
    const p = pregunta(clave, est);
    return [{ tipo: 'texto', texto: 'Perdón, no te entendí. Elige una opción o escribe tu respuesta, por favor.' }, p];
  }

  function avanzar(est, clave) {
    est.fallos = 0;
    evento(est, 'paso_respondido', clave);
    const sig = siguiente(clave, est);
    est.paso = sig;
    if (sig === 'COMPLETO') return completar(est);
    return [pregunta(sig, est)];
  }

  function completar(est) {
    est.terminado = true; est.estado_bot = 'COMPLETO';
    evento(est, 'datos_completos');
    const nombre = (est.datos.nombre || '').split(' ')[0];
    return [{ tipo: 'texto', texto: `¡Listo, ${nombre}! Ya tenemos todo ✅ Bernardo, de nuestro equipo, te escribe para darte tu cotización. Horario: lun–vie 9–18 h, sáb 9–14 h.` }];
  }

  /** entrada: { texto?, opcion?, imagen?: true, ubicacion?: {lat, lng} } → { estado, respuestas[] } */
  function paso(estadoPrevio, entrada) {
    const est = estadoPrevio ? JSON.parse(JSON.stringify(estadoPrevio)) : nuevoEstado();
    entrada = entrada || {};
    const texto = entrada.texto || '';
    let r;

    if (est.terminado) {
      evento(est, 'mensaje_posterior', texto || (entrada.imagen ? 'imagen' : ''));
      if (entrada.imagen) est.fotos.push('otro');
      return { estado: est, respuestas: [{ tipo: 'texto', texto: 'Gracias, ya se lo pasé a Bernardo junto con tu ficha 👍' }] };
    }

    if (texto && PALABRAS_ASESOR.test(texto) && est.paso !== 'NUEVO') {
      r = aHumano(est, 'pidio_asesor', 'Claro, te comunico con alguien del equipo. Bernardo te escribe en cuanto pueda 🙂');
      return { estado: est, respuestas: r };
    }

    switch (est.paso) {
      case 'NUEVO': {
        evento(est, 'primer_mensaje', texto);
        const ag = AGENCIAS.find(a => norm(texto).includes(a.clave));
        let saludo = '¡Hola! 👋 Soy el asistente de DPROMA.';
        if (ag) { est.agencia = ag.nombre; est.origen = 'oem'; est.datos.vehiculo = `${ag.marca} (modelo por confirmar)`;
                  saludo = `¡Hola! 👋 Vienes de ${ag.nombre}, ¡felicidades por tu auto nuevo! Soy el asistente de DPROMA.`; }
        est.paso = 'NOMBRE';
        r = [{ tipo: 'texto', texto: `${saludo} En un par de minutos tomo los datos para preparar la cotización de la instalación de tu cargador.\n\nAl seguir aceptas nuestro aviso de privacidad: dproma.com/privacidad\n\n¿A nombre de quién hacemos la cotización? (persona o empresa)` }];
        break;
      }
      case 'NOMBRE': {
        if (!texto || texto.trim().length < 2 || PREGUNTA_LIBRE.test(texto)) {
          est.fallos++; evento(est, 'no_reconocido', 'NOMBRE');
          if (est.fallos >= 2) { r = aHumano(est, 'no_reconocido', 'Mejor te comunico con alguien del equipo para resolver tus dudas. Bernardo te escribe en cuanto pueda 🙂'); break; }
          r = [{ tipo: 'texto', texto: 'Con gusto te damos el precio exacto, solo necesito unos datos 🙂 ¿A nombre de quién hacemos la cotización?' }];
          break;
        }
        est.datos.nombre = titulo(texto); est.fallos = 0; evento(est, 'paso_respondido', 'NOMBRE');
        est.paso = 'INMUEBLE'; r = [pregunta('INMUEBLE', est)];
        break;
      }
      case 'INMUEBLE': {
        const o = elegir('INMUEBLE', entrada);
        if (!o) { r = fallo(est, 'INMUEBLE'); break; }
        est.datos.tipo_inmueble = NOMBRE_INMUEBLE[o.id];
        if (o.id === 'empresa') { r = aHumano(est, 'flotilla', 'Para empresas y flotillas armamos una propuesta a la medida. Te comunico con Bernardo, de nuestro equipo comercial 🙂'); break; }
        r = avanzar(est, 'INMUEBLE');
        break;
      }
      case 'VEHICULO': {
        const o = elegir('VEHICULO', entrada);
        if (!o) { r = fallo(est, 'VEHICULO'); break; }
        if (o.id === 'otro') { est.fallos = 0; est.paso = 'VEHICULO_OTRO'; r = [pregunta('VEHICULO_OTRO', est)]; break; }
        est.datos.vehiculo = o.id; r = avanzar(est, 'VEHICULO');
        break;
      }
      case 'VEHICULO_OTRO': {
        if (!texto || texto.trim().length < 2) { r = fallo(est, 'VEHICULO_OTRO'); break; }
        est.datos.vehiculo = titulo(texto); est.paso = 'VEHICULO'; r = avanzar(est, 'VEHICULO');
        break;
      }
      case 'DOMICILIO':
      case 'DOMICILIO_CP': {
        if (entrada.ubicacion) {
          est.datos.mapa = `https://maps.google.com/?q=${entrada.ubicacion.lat},${entrada.ubicacion.lng}`;
          est.paso = 'DOMICILIO_CP'; est.fallos = 0;
          r = [{ tipo: 'texto', texto: '¡Gracias por la ubicación! Para la cotización necesito también el domicilio por escrito: calle, número, colonia y código postal.' }];
          break;
        }
        const cp = (texto.match(/\b\d{5}\b/) || [])[0];
        if (est.paso === 'DOMICILIO') {
          if (!texto || texto.trim().length < 6) { r = fallo(est, 'DOMICILIO'); break; }
          est.datos.domicilio = texto.trim().replace(/\s+/g, ' ');
          if (!cp) { est.paso = 'DOMICILIO_CP'; est.fallos = 0; r = [pregunta('DOMICILIO_CP', est)]; break; }
        } else {
          if (!cp) { r = fallo(est, 'DOMICILIO_CP'); break; }
          if (!est.datos.domicilio || est.datos.domicilio === cp) est.datos.domicilio = texto.trim();
          else if (!est.datos.domicilio.includes(cp)) est.datos.domicilio += `, CP ${cp}`;
        }
        est.datos.codigo_postal = cp; est.paso = 'DOMICILIO'; r = avanzar(est, 'DOMICILIO');
        break;
      }
      case 'METROS':
      case 'MEDIDOR': {
        const clave = est.paso; const o = elegir(clave, entrada);
        if (!o) { r = fallo(est, clave); break; }
        est.datos[clave === 'METROS' ? 'metros_aprox' : 'medidor_independiente'] = o.id;
        r = avanzar(est, clave);
        break;
      }
      case 'FOTO_TABLERO':
      case 'FOTO_SITIO':
      case 'FOTO_MEDIDOR': {
        const clave = est.paso;
        if (entrada.imagen) { est.fotos.push(P[clave].foto); evento(est, 'foto_recibida', P[clave].foto); r = avanzar(est, clave); break; }
        const o = elegir(clave, entrada);
        if (!o) { r = fallo(est, clave); break; }
        est.fotosPendientes.push(P[clave].foto); r = avanzar(est, clave);
        break;
      }
      default:
        r = [{ tipo: 'texto', texto: 'Gracias, ya se lo pasé al equipo 👍' }];
    }
    return { estado: est, respuestas: r };
  }

  /** Sin respuesta en 23 h: se registra con lo que haya. */
  function abandonar(estadoPrevio) {
    const est = JSON.parse(JSON.stringify(estadoPrevio || nuevoEstado()));
    if (est.terminado) return est;
    est.terminado = true; est.estado_bot = 'INCOMPLETO'; est.motivo_humano = 'sin_respuesta';
    evento(est, 'sin_respuesta_23h', est.paso);
    return est;
  }

  const ETIQUETA = { hasta_10: 'Hasta 10 m', '11_20': '11–20 m', '21_30': '21–30 m', mas_30: 'Más de 30 m', no_se: 'No sé',
                     si: 'Sí, medidor nuevo', no: 'No, luz actual' };

  const FOTO = { tablero: 'tablero', sitio_recorrido: 'lugar de carga', medidor: 'medidor' };

  /** Parámetros para la RPC whatsapp_registrar_lead (ver schema/poc-whatsapp-lead.schema.json). */
  function armarFicha(est, waId) {
    const d = est.datos;
    const partes = ['[Bot WhatsApp]', d.tipo_inmueble, d.metros_aprox && `Distancia: ${ETIQUETA[d.metros_aprox]}`,
      d.medidor_independiente && `Medidor: ${d.medidor_independiente === 'no_se' ? 'No sé' : ETIQUETA[d.medidor_independiente]}`,
      est.agencia && `Agencia: ${est.agencia}`, `${est.fotos.length} foto(s)`,
      est.fotosPendientes.length ? `Fotos pendientes: ${est.fotosPendientes.map(f => FOTO[f] || f).join(', ')}` : null,
      d.mapa && `Mapa: ${d.mapa}`, est.estado_bot !== 'COMPLETO' ? `Conversación: ${est.estado_bot} (${est.motivo_humano})` : null];
    return {
      nombre: d.nombre || 'Sin nombre (WhatsApp)',
      telefono: '+' + waId,
      correo: null,
      vehiculo: d.vehiculo || null,
      domicilio: d.domicilio || null,
      codigo_postal: d.codigo_postal || null,
      estado_id: null,
      origen: est.origen,
      agencia: est.agencia,
      canal: 'whatsapp',
      tipo_inmueble: d.tipo_inmueble || null,
      metros_aprox: d.metros_aprox || null,
      medidor_independiente: d.medidor_independiente || null,
      observaciones_texto: partes.filter(Boolean).join(' · '),
      wa_id: waId,
      estado_bot: est.estado_bot,
      motivo_humano: est.motivo_humano,
      evidencias: est.fotos.map((tipo, i) => ({ tipo, wa_media_id: `MEDIA_DEMO_${i + 1}`, mime_type: 'image/jpeg', drive_file_id: null })),
      eventos: est.eventos.map((e, i) => ({ tipo: e.tipo === 'foto_recibida' ? 'foto_subida' : ['primer_mensaje', 'datos_completos', 'derivado_humano', 'no_reconocido'].includes(e.tipo) ? e.tipo : 'paso_respondido',
                                            ocurrido_en: e.t || new Date(Date.UTC(2026, 10, 2, 16, 0, i * 20)).toISOString(), detalle: e.detalle })),
    };
  }

  /** Texto plano con opciones numeradas, para canales sin botones (chat de n8n). */
  function comoTexto(respuestas) {
    return respuestas.map(m => m.texto + (m.opciones && m.opciones.length
      ? '\n\n' + m.opciones.map((o, i) => `${i + 1}) ${o.label}`).join('\n') + (m.tipo === 'foto' ? '\n(o adjunta la foto; en esta demo escribe «foto»)' : '')
      : '')).join('\n\n');
  }

  return { paso, abandonar, armarFicha, comoTexto, nuevoEstado, ETIQUETA, FOTO };
})();
