#!/usr/bin/env python3
"""Sincroniza el motor del guion del bot (n8n/motor-guion.js) en sus dos usos:

1. n8n/demo-bot-whatsapp-dproma.json  — workflow importable en n8n (sin WhatsApp ni APIs).
2. web/entregables/poc-whatsapp-primer-contacto.html — simulador de la página, entre
   los marcadores /*MOTOR:INICIO*/ y /*MOTOR:FIN*/.

Uso:  python3 scripts/build-poc-whatsapp.py
"""
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MOTOR = (RAIZ / "n8n/motor-guion.js").read_text(encoding="utf-8")
SALIDA_N8N = RAIZ / "n8n/demo-bot-whatsapp-dproma.json"
PAGINA = RAIZ / "web/entregables/poc-whatsapp-primer-contacto.html"

CODIGO_MOTOR = MOTOR + r"""
// ───────── Adaptador para el chat de n8n ─────────
// El chat de n8n no tiene botones ni fotos: las opciones salen numeradas y
// escribir «foto» o «ubicación» simula enviar una imagen o la ubicación.
const memoria = $getWorkflowStaticData('global');   // persiste solo con el workflow ACTIVO
memoria.sesiones = memoria.sesiones || {};
const entrada = $input.first().json;
const sesion = entrada.sessionId || 'demo';
const texto = String(entrada.chatInput || '').trim();

if (/^(reiniciar|reset)$/i.test(texto)) {
  delete memoria.sesiones[sesion];
  return [{ json: { output: '🔄 Conversación reiniciada. Escribe «Hola» (o «Hola, vengo de Changan del Valle») para empezar.', terminado: false } }];
}

const mensaje = /^foto$/i.test(texto) ? { imagen: true }
  : /^ubicaci[oó]n$/i.test(texto) ? { ubicacion: { lat: 19.3907, lng: -99.161 } }
  : { texto };

const previo = memoria.sesiones[sesion] || null;
const yaTerminado = !!(previo && previo.terminado);
const r = MOTOR.paso(previo, mensaje);
memoria.sesiones[sesion] = r.estado;

// Teléfono de demostración estable por sesión (en el piloto viene de WhatsApp: contacts[].wa_id).
let h = 0; for (const c of sesion) h = (h * 31 + c.charCodeAt(0)) >>> 0;
const waId = '52155' + String(h % 100000000).padStart(8, '0');

const terminado = r.estado.terminado && !yaTerminado;
return [{ json: {
  output: MOTOR.comoTexto(r.respuestas),
  terminado,
  paso: r.estado.paso,
  sesion,
  waId,
  ficha: terminado ? MOTOR.armarFicha(r.estado, waId) : null,
} }];
"""

NOTA_GENERAL = """## 🧪 Demo · Bot de primer contacto DPROMA

**Qué hace:** simula la conversación de WhatsApp en el chat de n8n, sin WhatsApp, sin APIs y sin credenciales.

**Cómo probar:**
1. Publica el workflow (botón *Publish*, arriba a la derecha; en versiones anteriores, interruptor *Active*).
2. Abre el nodo **Chat (simula WhatsApp)** y copia la *Chat URL*, o usa el botón **Open chat**.
3. Escribe «Hola, vengo de Changan del Valle» o solo «Hola».
4. Contesta con el número de la opción. Escribe «foto» para simular una imagen y «reiniciar» para empezar de nuevo.

Guía completa: `docs/poc-whatsapp/07-demo-n8n.md`"""

NOTA_MOTOR = """### 1 · Motor del guion
La misma lógica que el simulador de la página: preguntas, validaciones, «no entendí» ×2 → persona, flotilla → Bernardo.
Guarda el avance de cada conversación en la memoria del workflow.

**En el piloto:** la entrada sería el webhook de WhatsApp Cloud API (con firma y filtro) en lugar de este chat."""

NOTA_SIMULADO = """### 2 · Lo que en el piloto será real
- **Simular registro en panel** → RPC `whatsapp_registrar_lead` en Supabase (crea la ficha «lead» en Contactos y la actividad en la Agenda de Bernardo).
- **Simular aviso a Bernardo** → mensaje de WhatsApp al número de Bernardo.
- Las fotos irían a Drive (`DPROMA — Comercial/{folio}`).

Abre *Executions* para ver la ficha completa que se habría enviado."""


def nodo(nombre, tipo, version, pos, params, id_):
    return {"parameters": params, "id": id_, "name": nombre, "type": tipo,
            "typeVersion": version, "position": pos}


def asignacion(nombre, valor, tipo="string", i=0):
    return {"id": f"a{i}-{nombre}", "name": nombre, "value": valor, "type": tipo}


def construir_workflow():
    nodos = [
        nodo("Chat (simula WhatsApp)", "@n8n/n8n-nodes-langchain.chatTrigger", 1.1, [0, 300], {
            "public": True,
            "mode": "hostedChat",
            "initialMessages": "Hola 👋 Esta es una demo del bot de DPROMA.\nEscribe «Hola» o «Hola, vengo de Changan del Valle» para empezar.",
            "options": {
                "title": "DPROMA · Demo bot WhatsApp",
                "subtitle": "Simulación sin WhatsApp ni APIs",
                "inputPlaceholder": "Escribe un mensaje…",
                "responseMode": "lastNode",
            },
        }, "b1f0c001-0000-4000-8000-000000000001"),
        nodo("Motor del guion", "n8n-nodes-base.code", 2, [260, 300],
             {"jsCode": CODIGO_MOTOR}, "b1f0c001-0000-4000-8000-000000000002"),
        nodo("¿Terminó la conversación?", "n8n-nodes-base.if", 2.2, [520, 300], {
            "conditions": {
                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
                "conditions": [{
                    "id": "c1", "leftValue": "={{ $json.terminado }}", "rightValue": True,
                    "operator": {"type": "boolean", "operation": "true", "singleValue": True},
                }],
                "combinator": "and",
            },
            "options": {},
        }, "b1f0c001-0000-4000-8000-000000000003"),
        nodo("Responder siguiente pregunta", "n8n-nodes-base.set", 3.4, [800, 420], {
            "assignments": {"assignments": [asignacion("output", "={{ $json.output }}")]},
            "options": {},
        }, "b1f0c001-0000-4000-8000-000000000004"),
        nodo("Simular registro en panel", "n8n-nodes-base.set", 3.4, [800, 180], {
            "assignments": {"assignments": [
                asignacion("rpc", "whatsapp_registrar_lead", i=1),
                asignacion("parametros", "={{ $json.ficha }}", "object", 2),
                asignacion("respuesta_simulada", "={{ { folio: 'C-DEMO-' + $json.waId.slice(-4), nuevo: true } }}", "object", 3),
                asignacion("actividad_agenda", "={{ 'Contactar lead de WhatsApp: ' + $json.ficha.nombre }}", "string", 4),
            ]},
            "options": {},
        }, "b1f0c001-0000-4000-8000-000000000005"),
        nodo("Simular aviso a Bernardo", "n8n-nodes-base.set", 3.4, [1060, 180], {
            "assignments": {"assignments": [
                asignacion("para", "Bernardo (WhatsApp)", i=5),
                asignacion("aviso", "={{ '🔌 Nuevo lead WhatsApp · ' + ($json.parametros.agencia || 'venta directa') + '\\nFicha ' + $json.respuesta_simulada.folio + ' · ' + $json.parametros.nombre + ' · ' + $json.parametros.telefono + '\\n🏠 ' + ($json.parametros.tipo_inmueble || '—') + ' · 🚗 ' + ($json.parametros.vehiculo || '—') + '\\n📍 ' + ($json.parametros.domicilio || '—') + '\\n📝 ' + $json.parametros.observaciones_texto }}", "string", 6),
            ]},
            "options": {},
        }, "b1f0c001-0000-4000-8000-000000000006"),
        nodo("Responder al cliente", "n8n-nodes-base.set", 3.4, [1320, 180], {
            "assignments": {"assignments": [
                asignacion("output", "={{ $('Motor del guion').item.json.output + '\\n\\n— 🧪 Solo en la demo: esto le llegaría a Bernardo —\\n' + $json.aviso }}", i=7),
            ]},
            "options": {},
        }, "b1f0c001-0000-4000-8000-000000000007"),
        nodo("Nota · Cómo probar", "n8n-nodes-base.stickyNote", 1, [-60, -200],
             {"content": NOTA_GENERAL, "height": 380, "width": 520, "color": 4}, "b1f0c001-0000-4000-8000-000000000008"),
        nodo("Nota · Motor", "n8n-nodes-base.stickyNote", 1, [200, 480],
             {"content": NOTA_MOTOR, "height": 240, "width": 400, "color": 7}, "b1f0c001-0000-4000-8000-000000000009"),
        nodo("Nota · Simulado", "n8n-nodes-base.stickyNote", 1, [760, -120],
             {"content": NOTA_SIMULADO, "height": 260, "width": 560, "color": 6}, "b1f0c001-0000-4000-8000-000000000010"),
    ]
    conexiones = {
        "Chat (simula WhatsApp)": {"main": [[{"node": "Motor del guion", "type": "main", "index": 0}]]},
        "Motor del guion": {"main": [[{"node": "¿Terminó la conversación?", "type": "main", "index": 0}]]},
        "¿Terminó la conversación?": {"main": [
            [{"node": "Simular registro en panel", "type": "main", "index": 0}],
            [{"node": "Responder siguiente pregunta", "type": "main", "index": 0}],
        ]},
        "Simular registro en panel": {"main": [[{"node": "Simular aviso a Bernardo", "type": "main", "index": 0}]]},
        "Simular aviso a Bernardo": {"main": [[{"node": "Responder al cliente", "type": "main", "index": 0}]]},
    }
    nodos[0]["webhookId"] = "d9f1a2b3-4c5d-4e6f-8a9b-0c1d2e3f4a5b"   # URL estable del chat: /webhook/<id>/chat
    return {
        "name": "DPROMA · Demo bot WhatsApp (sin APIs)",
        "nodes": nodos,
        "connections": conexiones,
        "settings": {"executionOrder": "v1"},
        "pinData": {},
        "active": False,
        "id": "dpromaDemoBotWa01",
        "tags": [],
    }


def main():
    SALIDA_N8N.write_text(json.dumps(construir_workflow(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {SALIDA_N8N.relative_to(RAIZ)}")
    if PAGINA.exists():
        html = PAGINA.read_text(encoding="utf-8")
        nuevo, n = re.subn(r"/\*MOTOR:INICIO\*/.*?/\*MOTOR:FIN\*/",
                           lambda _: "/*MOTOR:INICIO*/\n" + MOTOR + "\n/*MOTOR:FIN*/", html, flags=re.S)
        flujo = json.dumps(construir_workflow(), ensure_ascii=False).replace("</", "<\\/")
        nuevo, m = re.subn(r"/\*N8N:INICIO\*/.*?/\*N8N:FIN\*/",
                           lambda _: "/*N8N:INICIO*/\nconst N8N_WORKFLOW = " + flujo + ";\n/*N8N:FIN*/", nuevo, flags=re.S)
        if n:
            PAGINA.write_text(nuevo, encoding="utf-8")
            print(f"✓ {PAGINA.relative_to(RAIZ)} (motor y workflow sincronizados)")
        else:
            print(f"· {PAGINA.relative_to(RAIZ)} sin marcadores /*MOTOR:INICIO*/: no se tocó")


if __name__ == "__main__":
    main()
