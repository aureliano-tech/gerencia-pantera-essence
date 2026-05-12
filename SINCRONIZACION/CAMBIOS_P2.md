# CAMBIOS_P2.md — HISTORIAL DE CAMBIOS DIRECCIÓN DE VENTAS

> **Versión:** 1.0  
> **Fecha:** 14 de mayo de 2026  
> **Ruta:** C:\Users\USUARIO\Desktop\gerencia-pantera-essence\SINCRONIZACION\  
> **Propósito:** Registro cronológico de todos los cambios originados en P2 Ventas que afectan a otras direcciones. Se genera automáticamente al cierre de cada sesión P2.

---

## CÓMO USAR ESTE ARCHIVO

1. Al cierre de cada sesión P2, se genera una entrada nueva
2. El comando `github_sync.py` agrega la entrada automáticamente
3. Otras direcciones revisan este archivo al abrir sesión
4. Cada entrada incluye: qué cambió, a quién afecta, qué acción se requiere

---

## HISTORIAL

---

### 13/05/2026 — P2 VENTAS

**Qué se hizo:**
- Cupón correcto es PRIMERA10 10% global permanente (no PRIMERAIO). Actualizar todos los MDs y comunicaciones que digan PRIMERAIO.
- UTMs configurados en ambos ads activos: pe-trafico-mayo2026, pe-conversion-mayo2026. Convención obligatoria: pe-[tipo]-[mes][año].
- Ad Conversión corregido: PANTERA15 → PAPA2026 25%.
- PANTERA15 ya no se usa en ningún lado. Todos los copys actualizados a PAPA2026.
- T-016 ROAS definido: P2 registra gasto semanal (viernes), sistema calcula ROAS, CPA, pedidos, ticket promedio automáticamente.
- T-008 decidido: Resend free ($0, 3K emails/mes). No Treble por ahora.
- Google Ads aprobado como segundo canal de venta (Search + Shopping). Cuenta por crear con rhonalduribe@gmail.com.
- /khamrah, /gracias, /seguimiento3 configurados en WhatsApp.

**Afecta a:** P1 Desarrollo, P3 Landing, Gerencia

**MD actualizado:** CLAUDE_VENTAS.md (v5.0), MASTER.md (v5.0)

**Acciones requeridas:**

| Quién | Acción | Estado |
|-------|--------|--------|
| P1 | Recibir API key de Resend para implementar T-007B | ⬜ Pendiente |
| P1 | Cuando API catálogo esté lista, permitir /api/catalog en robots.txt | ⬜ Pendiente |
| P1 | Feed de productos para Google Merchant Center (cuando Google Ads esté listo) | ⬜ Futuro |
| P3 | Verificar que landings no mencionen PRIMERAIO ni PANTERA15 → usar PRIMERA10 y PAPA2026 | ⬜ Pendiente |
| Gerencia | MASTER.md actualizado a v5.0 | ✅ Hecho |
| Aureliano | Enviar API key Resend a P1 | ⬜ Pendiente |

**Estado:** 🟡 Parcialmente completado

---

### 14/05/2026 — P2 VENTAS

**Qué se hizo:**
- Sesión inaugural P2 en repositorio GitHub
- CLAUDE_VENTAS.md actualizado a v5.1 (protocolo de cierre con github_sync.py)
- METRICAS_ADS.md v1.0 creado (tracking semanal 5 semanas, reglas de decisión)
- CAMBIOS_P2.md v1.0 creado (historial inicial con entrada 13/05)
- Verificación de cupones: PRIMERA10 es el correcto (no PRIMERAIO como se indicó en la sesión)
- Estructura confirmada: P1 Desarrollo, P2 Ventas, P3 Landing, Gerencia

**Afecta a:** Gerencia

**MD actualizado:** CLAUDE_VENTAS.md (v5.1), METRICAS_ADS.md (v1.0), CAMBIOS_P2.md (v1.0)

**Acciones requeridas:**

| Quién | Acción | Estado |
|-------|--------|--------|
| Aureliano | Subir 3 archivos al repo GitHub | ⬜ Pendiente |
| Aureliano | Enviar API key Resend a P1 (arrastrado de 13/05) | ⬜ Pendiente |

**Estado:** ⬜ Pendiente (archivos generados, falta subir)

---
