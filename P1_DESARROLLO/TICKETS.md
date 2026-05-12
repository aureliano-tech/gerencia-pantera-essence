# TICKETS.md — Requerimientos inter-direcciones

> **Proyecto:** Pantera Essence
> **Ubicación:** Raíz del repo pantera-essence-web
> **Regla:** No ejecutar nada de otra dirección sin ticket registrado primero
> **Última actualización:** 11 de mayo de 2026

---

## Convenciones

- **ID:** T-### (secuencial)
- **Origen:** P2, P3, P4, Gerencia, Aureliano
- **Destino:** P1 (siempre, este archivo es de P1)
- **Prioridad:** 🔴 Alta · 🟡 Media · 🟢 Baja
- **Estado:** ⬜ Pendiente · 🔄 En progreso · ✅ Completado · ❌ Rechazado · ⏸️ Bloqueado

---

## TICKETS COMPLETADOS ✅

### T-001 — Meta Pixel 5 eventos
| Campo | Valor |
|---|---|
| Origen | P2/P4 |
| Prioridad | 🔴 Alta |
| Fecha | 10 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Implementar Meta Pixel con eventos e-commerce: ViewContent, AddToCart, InitiateCheckout, Purchase, Lead |
| Resultado | 5 eventos activos con guard, carga diferida 5s, payload completo COP |

### T-003 — GA4 Enhanced E-commerce
| Campo | Valor |
|---|---|
| Origen | P2 |
| Prioridad | 🔴 Alta |
| Fecha | 11 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Implementar GA4 Enhanced E-commerce: view_item, add_to_cart, begin_checkout, purchase |
| Resultado | 4 eventos activos con guard, disparo simultáneo con Pixel, payload Enhanced E-commerce |

### T-004 — Dashboard métricas avanzado
| Campo | Valor |
|---|---|
| Origen | P2 |
| Prioridad | 🔴 Alta |
| Fecha | 11 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Dashboard con KPIs, filtro período (Hoy/7d/30d/Todo), revenue real, top productos, fuentes UTM, leads quiz, gráfica dinámica, pedidos por estado |
| Resultado | Dashboard completo en /admin/dashboard con todas las secciones |

### T-005 — UTM tracking first-touch
| Campo | Valor |
|---|---|
| Origen | P2/P4 |
| Prioridad | 🔴 Alta |
| Fecha | 10 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Capturar UTM params (source, medium, campaign, content) en first-touch y guardar en orders |
| Resultado | sessionStorage con prefijo pe_, guardado automático al crear orden |

### T-006 — Popup exit intent dinámico
| Campo | Valor |
|---|---|
| Origen | P2 |
| Prioridad | 🟡 Media |
| Fecha | 12 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Popup exit intent solo desktop, cupón PRIMERA10 (confirmado P2), CTA contextual, clave sessionStorage independiente del timer |
| Resultado | PromoPopup con dos triggers independientes (timer 5s + exit intent desktop) |

### T-007A — Sistema reseñas
| Campo | Valor |
|---|---|
| Origen | P2 |
| Prioridad | 🔴 Alta |
| Fecha | 11 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | QuickReview en ProductDetail + AdminReviews moderación (aprobar/rechazar) + badge pendientes en sidebar |
| Resultado | Sistema completo: submit público, moderación admin, estrellas en catálogo |

### T-012 — Schema.org Product verificado
| Campo | Valor |
|---|---|
| Origen | P1 (interno) |
| Prioridad | 🟡 Media |
| Fecha | 12 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Verificar Schema.org Product completo en ProductDetail |
| Resultado | JSON-LD con name, image, brand, offers, sku, description, aggregateRating |

### T-013 — Meta tags SEO dinámicos
| Campo | Valor |
|---|---|
| Origen | P1 (interno) |
| Prioridad | 🟡 Media |
| Fecha | 12 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Meta tags dinámicos (title+description+OG con inspired_by y ahorro % calculado) para 151 productos |
| Resultado | Helmet con datos dinámicos por producto, mejora en snippets de buscadores |

### T-014 — sort_position productos estrella
| Campo | Valor |
|---|---|
| Origen | P2 |
| Prioridad | 🟡 Media |
| Fecha | 12 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Asignar sort_position 1-8 a productos estrella en Supabase |
| Resultado | 8 productos con posición fija en catálogo |

### T-015 — /blog verificado completo
| Campo | Valor |
|---|---|
| Origen | P1 (interno) |
| Prioridad | 🟢 Baja |
| Fecha | 12 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Verificar que /blog funcione completo con listado y detalle |
| Resultado | Blog funcional con meta tags SEO + Schema.org Article JSON-LD |

### T-016 — ROAS por campaña
| Campo | Valor |
|---|---|
| Origen | P2 |
| Prioridad | 🔴 Alta |
| Fecha | 13 mayo 2026 |
| Estado | ✅ Completado |
| Descripción | Sistema de registro de gasto publicitario + cálculo automático ROAS/CPA/ticket por campaña en dashboard |
| Resultado | /admin/campanas + sección rendimiento en dashboard + tabla campaign_spend + RLS + auditoría |

---

## TICKETS PENDIENTES / BLOQUEADOS

### T-007B — Email post-entrega Resend
| Campo | Valor |
|---|---|
| Origen | P2 |
| Prioridad | 🔴 Alta |
| Fecha | 11 mayo 2026 |
| Estado | ⏸️ Bloqueado |
| Bloqueador | API key Resend pendiente en Vercel (Aureliano debe revocar key expuesta, generar nueva, agregar en Vercel) |
| Descripción | Email automático post-entrega solicitando reseña del producto |

### T-008 — Email/WhatsApp post-compra
| Campo | Valor |
|---|---|
| Origen | P2 |
| Prioridad | 🟡 Media |
| Fecha | 11 mayo 2026 |
| Estado | ⬜ Pendiente |
| Bloqueador | Presupuesto (Resend free 3K/mes o Treble ~$150K COP/mes) |
| Descripción | Secuencia automática: confirmación → guía de envío → solicitar review → recompra |

### T-009 — Carrito abandonado
| Campo | Valor |
|---|---|
| Origen | P2 |
| Prioridad | 🟢 Baja |
| Fecha | 11 mayo 2026 |
| Estado | ⬜ Pendiente |
| Bloqueador | Presupuesto (ManyChat ~$15 USD/mes) |
| Descripción | Recuperación de carritos abandonados vía WhatsApp/email |

---

## TAREAS INTERNAS P1 (sin ticket externo)

| ID | Tarea | Prioridad | Estado |
|---|---|---|---|
| INT-001 | Revisión completa versión móvil (layout, navegación, UX) | 🔴 Alta | ⬜ |
| INT-002 | Fix logo pantera que se sale del banner en móvil | 🔴 Alta | ⬜ |
| INT-003 | Fix admin_email "desconocido" en audit_log | 🔴 Alta | ⬜ |
| INT-004 | Revertir precio Emper Stallion 53 a $190.000 | 🔴 Alta | ⬜ |
| INT-005 | Ampliar catálogo: 20 diseñador + 20 nicho | 🟡 Media | ⬜ |
| INT-006 | Quiz: 2 productos nicho (hombre+oud, unisex+cítrica) | 🟡 Media | ⬜ |
| INT-007 | Fotos 17 productos pendientes | 🟡 Media | ⬜ |
| INT-008 | Conexión Config → Checkout datos bancarios | 🟢 Baja | ⬜ |
| INT-009 | Chat IA integrado | 🟢 Baja | ⬜ |
| INT-010 | PWA | 🟢 Baja | ⬜ |
| INT-011 | 2FA admin | 🟢 Baja | ⬜ |
| INT-012 | Backup automático DB | 🟢 Baja | ⬜ |

---

## ACCIONES PENDIENTES DE AURELIANO

| Acción | Contexto | Estado |
|---|---|---|
| Revocar API key Resend expuesta | Key pegada en chat 13 mayo | ⬜ Pendiente |
| Generar nueva API key Resend | Después de revocar la anterior | ⬜ Pendiente |
| Agregar RESEND_API_KEY en Vercel | Solo en Vercel dashboard, nunca en chat | ⬜ Pendiente |
| Vincular Pixel al conjunto de datos Meta Ads | Tarea de P4, no de P1 | ⬜ Pendiente |

---

## PLANTILLA PARA NUEVOS TICKETS

```
### T-### — [Título]
| Campo | Valor |
|---|---|
| Origen | [P2/P3/P4/Gerencia/Aureliano] |
| Prioridad | [🔴 Alta / 🟡 Media / 🟢 Baja] |
| Fecha | [fecha] |
| Estado | [⬜ Pendiente / 🔄 En progreso / ✅ Completado / ❌ Rechazado / ⏸️ Bloqueado] |
| Descripción | [qué se necesita] |
```

---

*Archivo mantenido por P1 — actualizar en cada sesión de trabajo.*
*Última actualización: 11 de mayo de 2026*
