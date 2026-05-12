# ANALYTICS_P2.md — Sistema de Métricas, Medición y Analytics para Ventas

> **Proyecto:** Pantera Essence — E-commerce de perfumería
> **Versión:** 1.0
> **Propietario:** Aureliano (Ingeniero Financiero)
> **Dirección responsable:** P1 — Desarrollo Web (construye) · P2 — Ventas (consume)
> **Última actualización:** 11 de mayo de 2026 — Sesión T-004
> **Clasificación:** Framework reutilizable + estado específico del proyecto

---

## REGLA DE ORO

> **Al finalizar CADA sesión donde se desarrolle algo relacionado con métricas, tracking, eventos, dashboard, datos de ventas o analytics, esta sección se actualiza OBLIGATORIAMENTE.**
>
> Razón: esta documentación es insumo directo para la medición de ventas y la generación de estrategias para optimizar recursos y eficiencia en publicidad pagada en redes sociales. Si no se actualiza, P2 trabaja con información desactualizada y toma decisiones incorrectas.

---

## 1. ARQUITECTURA DE MEDICIÓN

### 1.1 Flujo de datos

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     FLUJO COMPLETO DE MEDICIÓN                          │
│                                                                          │
│  USUARIO LLEGA AL SITIO                                                  │
│       │                                                                  │
│       ├─── UTM params ──► sessionStorage (pe_utm_*) ──► orders.utm_*    │
│       │    (first-touch)                                                 │
│       │                                                                  │
│  USUARIO NAVEGA                                                          │
│       │                                                                  │
│       ├─── Meta Pixel ──► ViewContent ──► Meta Events Manager ──► P4    │
│       ├─── GA4 ──────────► view_item ───► Google Analytics ──────► P2   │
│       │                                                                  │
│  USUARIO AGREGA AL CARRITO                                               │
│       │                                                                  │
│       ├─── Meta Pixel ──► AddToCart                                      │
│       ├─── GA4 ──────────► add_to_cart                                   │
│       │                                                                  │
│  USUARIO INICIA CHECKOUT                                                 │
│       │                                                                  │
│       ├─── Meta Pixel ──► InitiateCheckout                               │
│       ├─── GA4 ──────────► begin_checkout                                │
│       │                                                                  │
│  USUARIO COMPLETA COMPRA                                                 │
│       │                                                                  │
│       ├─── Meta Pixel ──► Purchase (value, currency, content_ids)        │
│       ├─── GA4 ──────────► purchase (value, items, transaction_id)       │
│       ├─── Supabase ─────► INSERT orders (datos completos + UTM)         │
│       └─── coupon_usage ─► INSERT si usó cupón                           │
│                                                                          │
│  USUARIO COMPLETA QUIZ                                                   │
│       │                                                                  │
│       ├─── Meta Pixel ──► Lead                                           │
│       └─── Supabase ─────► INSERT leads (name, contact, answers)         │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════════  │
│                                                                          │
│  DASHBOARD /admin/dashboard                                              │
│       │                                                                  │
│       ├─── Lee: orders + promotions + leads + products (Supabase)        │
│       ├─── Calcula: KPIs, revenue, top productos, fuentes, cupones      │
│       └─── P2 consulta para decisiones de negocio y estrategia          │
│                                                                          │
│  GA4 (analytics.google.com)                                              │
│       └─── P2 consulta: visitas, sesiones, audiencias, comportamiento   │
│                                                                          │
│  Meta Events Manager (business.facebook.com)                             │
│       └─── P4 consulta: eventos Pixel, audiencias, conversiones ads     │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Principios de medición

| Principio | Descripción |
|---|---|
| Captura única | Cada dato se captura UNA vez en su punto de origen, no se duplica |
| No duplicar GA4/Meta | P1 no replica visitas ni audiencias — eso ya lo hacen GA4 y Meta gratis |
| Datos transaccionales en Supabase | Revenue, pedidos, cupones, leads, UTM — solo existen en nuestra DB |
| Guard obligatorio | Todo evento de tracking lleva guard: `if (typeof fbq !== 'undefined')` / `if (typeof gtag !== 'undefined')` |
| Disparo simultáneo | Pixel y GA4 disparan en el MISMO punto del código, uno al lado del otro |
| Scripts diferidos | Pixel y GA4 se cargan 5 segundos después del load para no afectar rendimiento |
| First-touch UTM | Se captura la primera fuente de tráfico, no la última (sessionStorage con prefijo pe_) |

---

## 2. EVENTOS DE TRACKING — ESTADO ACTUAL

### 2.1 Meta Pixel (5 eventos activos)

| Evento | Cuándo dispara | Archivo | Payload |
|---|---|---|---|
| ViewContent | Al montar ProductDetail | ProductDetail.jsx | content_name, content_ids, content_type, value, currency: COP |
| AddToCart | Al ejecutar addToCart() | CartContext.jsx | content_name, content_ids, content_type, value, currency: COP |
| InitiateCheckout | Al montar Checkout | Checkout.jsx | value (total carrito), currency: COP, num_items |
| Purchase | Tras saveOrder exitoso | Checkout.jsx (x2) | content_ids (array SKUs), value (total), currency: COP, num_items |
| Lead | Al enviar datos quiz | Quiz.jsx | content_name: "quiz_completado" |

**Guard obligatorio en todos:**
```js
if (typeof fbq !== 'undefined') {
  fbq('track', 'EventName', { /* payload */ })
}
```

**Cómo verificar:** F12 → Console en panteraessence.com. Navegar, agregar al carrito, ir a checkout. También en Meta Events Manager → Test Events.

### 2.2 GA4 Enhanced E-commerce (4 eventos activos)

| Evento | Cuándo dispara | Archivo | Payload |
|---|---|---|---|
| view_item | Al montar ProductDetail | ProductDetail.jsx | currency: COP, value, items: [{item_id, item_name, item_brand, item_category, price, quantity}] |
| add_to_cart | Al ejecutar addToCart() | CartContext.jsx | currency: COP, value, items: [{...}] |
| begin_checkout | Al montar Checkout | Checkout.jsx | currency: COP, value, items: [{...}] |
| purchase | Tras saveOrder exitoso | Checkout.jsx (x2) | transaction_id, currency: COP, value, shipping, items: [{...}] |

**Guard obligatorio en todos:**
```js
if (typeof gtag !== 'undefined') {
  gtag('event', 'event_name', {
    currency: 'COP',
    value: precio,
    items: [{ item_id, item_name, item_brand, item_category, price, quantity }]
  })
}
```

**Cómo verificar P2:** GA4 → Informes → Monetización → Compras de comercio electrónico. También en Tiempo real → Eventos.

### 2.3 UTM Tracking (first-touch)

| Campo | Almacenamiento | Persistencia |
|---|---|---|
| utm_source | sessionStorage (pe_utm_source) → orders.utm_source | Sesión del navegador |
| utm_medium | sessionStorage (pe_utm_medium) → orders.utm_medium | Sesión del navegador |
| utm_campaign | sessionStorage (pe_utm_campaign) → orders.utm_campaign | Sesión del navegador |
| utm_content | sessionStorage (pe_utm_content) → orders.utm_content | Sesión del navegador |

**Cómo funciona:** Al llegar al sitio con `?utm_source=facebook&utm_medium=cpc&utm_campaign=papa2026`, se guarda en sessionStorage. Al completar la compra, se graba en la orden. Si no hay UTM → se registra como "Directo".

**Cómo verificar:** Abrir `panteraessence.com/catalogo?utm_source=facebook&utm_medium=cpc&utm_campaign=test`. Hacer una compra. En /admin/pedidos aparecerá la fuente como "facebook / cpc / test".

---

## 3. DASHBOARD DE MÉTRICAS (/admin/dashboard) — T-004

### 3.1 KPIs disponibles

| KPI | Fuente de datos | Filtrable por período | Descripción |
|---|---|---|---|
| Pedidos | orders (count) | ✅ Hoy/7d/30d/Todo | Total de pedidos en el período |
| Ingresos | orders.total (sum, no cancelados) | ✅ | Revenue neto del período |
| Productos activos | products (count in_stock) | ❌ | Inventario actual |
| Pedidos pendientes | orders (count status=pendiente) | ✅ | Por confirmar en el período |
| Ticket promedio | orders.total (avg, no cancelados) | ✅ | Promedio por pedido |
| Tasa de cancelación | cancelados / total × 100 | ✅ | % pedidos cancelados |

### 3.2 Secciones del dashboard

**Resumen del período**
- 4 cards KPI principales con filtro global (Hoy / 7 días / 30 días / Todo)
- Pedidos por estado: distribución con barras coloreadas (pendiente/confirmado/enviado/entregado/cancelado)

**Gráfica de ventas**
- Dinámica según filtro: Hoy = 24 barras por hora, 7d = 7 barras por día, 30d = 30 barras por día, Todo = 12 barras por mes
- Tooltip con fecha y monto al pasar el cursor

**Ventas y negocio**
- Ticket promedio con período
- Ingresos por categoría: distribución % entre árabe, diseñador, nicho
- Método de pago: distribución % Bold vs Transferencia
- Tasa de cancelación con barra visual (rojo si >15%)
- Revenue por cupón: % de revenue con cupón vs sin cupón, con montos absolutos

**Marketing y adquisición**
- Fuentes de tráfico: distribución de pedidos por utm_source (facebook, instagram, google, directo, etc.)
- Cupones más usados: ranking top 5 con código, veces usado, revenue generado
- Leads del quiz: total capturados en el período

**Catálogo**
- Total productos, distribución por categoría, decants activos, productos sin foto

**Servicio y envío**
- Pedidos por departamento (top 5)
- Transportadora más usada
- Tiempo promedio de envío (pendiente: requiere campo sent_at)

**Actividad reciente**
- Últimos 5 pedidos con estado y enlace
- Top 5 productos más vendidos con revenue y unidades

### 3.3 Datos disponibles en cada orden

| Campo | Tipo | Uso para métricas |
|---|---|---|
| order_id | string | Identificador único |
| created_at | timestamp | Filtros de período, gráficas temporales |
| customer_name | string | Identificación |
| customer_email | string | Segmentación, recompra |
| customer_phone | string | Contacto post-venta |
| city | string | Geografía |
| department | string | Distribución geográfica |
| items | JSON array | Top productos, revenue por producto, categorías |
| total | number | Revenue, ticket promedio |
| subtotal | number | Revenue antes de descuentos |
| discount | number | Impacto de cupones |
| coupon | string | Cupón usado (null si ninguno) |
| shipping | number | Costo de envío cobrado |
| pay_method | string | Distribución Bold vs Transferencia |
| status | string | Embudo: pendiente → confirmado → enviado → entregado |
| carrier | string | Transportadora asignada |
| tracking_number | string | Guía de envío |
| utm_source | string | Fuente de tráfico (facebook, google, instagram, directo) |
| utm_medium | string | Medio (cpc, organic, social, email) |
| utm_campaign | string | Nombre de campaña |
| utm_content | string | Variante de contenido del ad |

### 3.4 Datos disponibles en promotions

| Campo | Uso para métricas |
|---|---|
| code | Identificar cupón |
| type | percentage o fixed |
| value | Monto o porcentaje del descuento |
| usage_count | Veces usado globalmente |
| is_active | Si está activo o no |
| gender_scope | Segmentación por género |
| product_ids | Productos específicos donde aplica |
| start_date / end_date | Vigencia |

### 3.5 Datos disponibles en leads

| Campo | Uso para métricas |
|---|---|
| name | Nombre del lead |
| contact | WhatsApp o email |
| quiz_answers | Respuestas del quiz (preferencias del cliente) |
| created_at | Fecha de captura |

---

## 4. DÓNDE CONSULTA CADA DIRECCIÓN

| Dato | P2 (Ventas) consulta en | P4 (Ads) consulta en |
|---|---|---|
| Revenue, pedidos, ticket promedio | /admin/dashboard | — |
| Top productos vendidos | /admin/dashboard | — |
| Cupones usados y su impacto | /admin/dashboard + /admin/promociones | — |
| Fuente de tráfico por venta | /admin/dashboard + /admin/pedidos | — |
| Leads del quiz | /admin/dashboard | — |
| Distribución geográfica | /admin/dashboard | — |
| Visitas al sitio | GA4 → analytics.google.com | — |
| Sesiones, páginas vistas | GA4 → analytics.google.com | — |
| Audiencias y demografía | GA4 → analytics.google.com | Meta Business Suite |
| Eventos Pixel (conversiones) | — | Meta Events Manager |
| Rendimiento de campañas ads | — | Meta Ads Manager |
| Costo por conversión | — | Meta Ads Manager |
| ROAS (retorno sobre gasto en ads) | — | Meta Ads Manager (necesita Purchase event) |

---

## 5. MÉTRICAS CLAVE PARA DECISIONES DE P2

### 5.1 Métricas de eficiencia comercial

| Métrica | Fórmula | Dónde se ve | Para qué sirve |
|---|---|---|---|
| Ticket promedio | Revenue / Pedidos (no cancelados) | Dashboard | Ajustar precios, bundles, upselling |
| Revenue por categoría | Sum(items) agrupado por category | Dashboard | Saber qué mundo vende más |
| Tasa de cancelación | Cancelados / Total × 100 | Dashboard | Detectar problemas en proceso de compra |
| Revenue por cupón | Sum(total) donde coupon != null | Dashboard | Medir impacto de campañas |
| Top productos | items agrupados por nombre | Dashboard | Restock, ads, contenido |

### 5.2 Métricas de adquisición

| Métrica | Fórmula | Dónde se ve | Para qué sirve |
|---|---|---|---|
| Fuente de tráfico | orders.utm_source agrupado | Dashboard | Saber de dónde vienen las ventas |
| Costo por adquisición (CPA) | Gasto ads / Compras | Meta Ads Manager | Eficiencia de la publicidad |
| ROAS | Revenue / Gasto ads | Meta Ads Manager | Retorno de la inversión en ads |
| Leads capturados | Count(leads) | Dashboard | Efectividad del quiz como embudo |
| Conversión quiz → compra | Leads que luego compran / Total leads | Manual (cruzar leads vs orders por email/teléfono) | Calidad de los leads |

### 5.3 Métricas de retención (futuras)

| Métrica | Estado | Requiere |
|---|---|---|
| Tasa de recompra | ⬜ Pendiente | Cruce orders por customer_email con >1 pedido |
| Lifetime Value (LTV) | ⬜ Pendiente | Sum revenue por customer_email |
| Frecuencia de compra | ⬜ Pendiente | Promedio días entre compras por cliente |
| Tasa de uso de cupón recompra | ⬜ Pendiente | coupon_usage cruzado con cliente recurrente |

---

## 6. ESTADO DE IMPLEMENTACIÓN

### 6.1 Completado ✅

| Feature | Ticket | Fecha | Descripción |
|---|---|---|---|
| Meta Pixel 5 eventos | T-001 | 10 mayo 2026 | ViewContent, AddToCart, InitiateCheckout, Purchase, Lead |
| UTM tracking first-touch | T-005 | 10 mayo 2026 | Captura utm_source/medium/campaign/content en orders |
| GA4 Enhanced E-commerce | T-003 | 11 mayo 2026 | view_item, add_to_cart, begin_checkout, purchase |
| Dashboard métricas avanzado | T-004 | 11 mayo 2026 | KPIs con filtro período, revenue por cupón, fuentes tráfico, cupones más usados, leads quiz, top productos con revenue, gráfica dinámica, pedidos por estado |

### 6.2 Pendiente — Requiere decisión de P2 o presupuesto

| Feature | Ticket | Bloqueador | Impacto en métricas |
|---|---|---|---|
| Popup exit intent | T-006 | P2 debe confirmar cupón | Nuevo canal de captura de leads + cupón |
| Sistema reseñas post-compra | T-007 | Mes 2 | Datos de satisfacción, social proof, NPS |
| Email/WhatsApp post-compra | T-008 | Presupuesto (Resend free 3K/mes o Treble ~$150K COP/mes) | Secuencia: confirmación → guía → review → recompra |
| Carrito abandonado | T-009 | Presupuesto (ManyChat ~$15 USD/mes) | Tasa de recuperación, revenue rescatado |

### 6.3 Roadmap de métricas — Próximas implementaciones recomendadas

| Prioridad | Feature | Qué habilita para P2 |
|---|---|---|
| 🔴 Alta | Tasa de recompra (cruce orders por email) | LA métrica principal del negocio — sin costo, solo código |
| 🔴 Alta | LTV por cliente | Identificar clientes VIP, segmentar campañas |
| 🟡 Media | Tiempo promedio de entrega (campo sent_at + delivered_at) | Medir calidad del servicio, optimizar transportadoras |
| 🟡 Media | Embudo de conversión visual (visita → carrito → checkout → compra) | Identificar dónde se pierden clientes |
| 🟡 Media | Revenue por campaña UTM | Saber exactamente cuánto genera cada campaña de ads |
| 🟢 Baja | Cohorts mensuales | Ver si los clientes de enero siguen comprando en mayo |
| 🟢 Baja | Segmentación RFM (Recency/Frequency/Monetary) | Automatizar segmentos de clientes para campañas |
| 🟢 Baja | Predicción de demanda por producto | Optimizar inventario |

---

## 7. MEJORES PRÁCTICAS — FRAMEWORK REPLICABLE

> Estas prácticas aplican a Pantera Essence y a cualquier proyecto e-commerce futuro. Son el estándar mínimo de medición profesional.

### 7.1 Tracking — Reglas de implementación

| Regla | Descripción | Por qué |
|---|---|---|
| Guard siempre | `if (typeof fbq !== 'undefined')` antes de cada disparo | Pixel/GA4 se cargan diferidos 5s — si el evento dispara antes, no hay error |
| Disparo simultáneo | Pixel y GA4 en el mismo punto del código, uno debajo del otro | Coherencia de datos entre plataformas |
| Datos completos | Siempre enviar value, currency, items con id/name/brand/category | Habilita reportes avanzados en GA4 y audiencias en Meta |
| No duplicar | El evento Purchase dispara UNA vez por transacción (tras saveOrder exitoso) | Evita inflar métricas |
| Moneda local | currency siempre 'COP' | Meta y GA4 necesitan la moneda para calcular ROAS |
| transaction_id en purchase | Usar order_id como transaction_id en GA4 | Permite deduplicar y cruzar con DB |

### 7.2 UTM — Convención de nomenclatura

| Parámetro | Convención | Ejemplos |
|---|---|---|
| utm_source | Plataforma de origen, minúsculas | facebook, instagram, google, tiktok, whatsapp, email |
| utm_medium | Tipo de tráfico | cpc (pagado), organic (orgánico), social (redes), email, referral |
| utm_campaign | Nombre de campaña | papa2026, mama2026, blackfriday, lanzamiento-nicho |
| utm_content | Variante del ad o contenido | video-asad, carousel-top5, story-promo |

**Ejemplo completo de URL para campaña:**
```
https://panteraessence.com/catalogo?utm_source=facebook&utm_medium=cpc&utm_campaign=papa2026&utm_content=video-asad
```

**Regla para P2/P4:** SIEMPRE usar UTM en links de campañas pagadas y emails. Sin UTM, el pedido se registra como "Directo" y no se puede atribuir a ninguna campaña.

### 7.3 Dashboard — Principios de diseño

| Principio | Descripción |
|---|---|
| Datos de Supabase, no de GA4 API | El dashboard lee directamente de la DB. No depende de APIs externas que tienen rate limits y requieren OAuth. GA4 se consulta aparte |
| Filtro de período global | Todos los KPIs responden al mismo filtro temporal. No mezclar períodos |
| Sin dependencias extra | El dashboard usa React puro + fetch a Supabase. No recharts, no chart.js, no D3. Barras CSS puras |
| Cero costo | Todo el sistema de métricas opera en free tier: Supabase, GA4, Meta Pixel, Vercel |
| Actualización en tiempo real | Al abrir el dashboard, consulta datos frescos de Supabase. No hay caché |
| Formato COP | Todos los montos en formatPrice() — pesos colombianos con separador de miles |

### 7.4 Cupones — Medición de impacto

| Métrica de cupón | Cómo se mide | Dónde |
|---|---|---|
| Veces usado | promotions.usage_count + cruce orders.coupon | Dashboard + /admin/promociones |
| Revenue generado | Sum(orders.total) donde coupon = código | Dashboard (cupones más usados) |
| % de revenue con descuento | Revenue con cupón / Revenue total × 100 | Dashboard (revenue por cupón) |
| Segmentación por género | promotions.gender_scope | /admin/promociones |
| Control por cliente | coupon_usage (unique constraint email+código) + localStorage | Automático |

### 7.5 Seguridad de datos de métricas

| Regla | Implementación |
|---|---|
| RLS en orders | Solo admin puede leer/escribir. Datos de clientes protegidos |
| RLS en leads | Solo admin puede leer |
| No exponer métricas al público | Dashboard solo accesible tras login admin |
| Audit log | Todas las acciones del admin se registran |
| UTM en sessionStorage | No persiste entre sesiones — privacy-friendly |

### 7.6 Checklist para cada feature de tracking nuevo

Antes de implementar cualquier evento o métrica nueva:

1. ¿Qué decisión de negocio habilita este dato? (si no habilita ninguna, no implementar)
2. ¿Ya existe en GA4 o Meta? (si sí, no duplicar — solo documentar dónde consultarlo)
3. ¿Requiere campo nuevo en Supabase? (evaluar migración)
4. ¿Tiene guard para carga diferida?
5. ¿Dispara Pixel y GA4 simultáneamente?
6. ¿Se refleja en el dashboard?
7. ¿Se actualizó ANALYTICS_P2.md?

---

## 8. GLOSARIO PARA P2

| Término | Significado |
|---|---|
| UTM | Urchin Tracking Module — parámetros en la URL que identifican de dónde viene el usuario |
| First-touch | Se guarda la PRIMERA fuente de tráfico del usuario, no la última |
| ROAS | Return On Ad Spend — cuánto revenue genera cada peso invertido en ads |
| CPA | Cost Per Acquisition — cuánto cuesta adquirir un cliente |
| LTV | Lifetime Value — cuánto gasta un cliente en total a lo largo del tiempo |
| RFM | Recency, Frequency, Monetary — modelo de segmentación de clientes |
| Funnel / Embudo | Secuencia: visita → producto → carrito → checkout → compra. En cada paso se pierden usuarios |
| Pixel | Código de Meta (Facebook) que trackea acciones del usuario en el sitio |
| GA4 | Google Analytics 4 — plataforma gratuita de analytics de Google |
| Enhanced E-commerce | Formato estándar de Google para eventos de comercio electrónico |
| Cohort | Grupo de clientes que comparten una característica (ej: todos los que compraron en enero) |
| NPS | Net Promoter Score — métrica de satisfacción del cliente (¿recomendarías?) |
| Session | Visita de un usuario al sitio. Una sesión puede tener múltiples páginas vistas |
| Bounce rate | % de usuarios que llegan y se van sin interactuar |

---

## 9. RESUMEN DE ACCESOS PARA P2

| Qué necesitas ver | Dónde ir | URL |
|---|---|---|
| Revenue, pedidos, ticket promedio | Dashboard admin | panteraessence.com/admin |
| Detalle de un pedido + UTM | Pedidos admin | panteraessence.com/admin/pedidos |
| Cupones activos y su uso | Promociones admin | panteraessence.com/admin/promociones |
| Visitas, sesiones, páginas | GA4 | analytics.google.com |
| Eventos Pixel, audiencias | Meta Events Manager | business.facebook.com → Events Manager |
| Rendimiento campañas ads | Meta Ads Manager | business.facebook.com → Ads Manager |
| Indexación SEO, keywords | Search Console | search.google.com/search-console |

---

## 10. HISTORIAL DE CAMBIOS

| Fecha | Sesión | Cambio |
|---|---|---|
| 10 mayo 2026 | T-001, T-005 | Meta Pixel 5 eventos + UTM tracking first-touch |
| 11 mayo 2026 | T-003 | GA4 Enhanced E-commerce 4 eventos |
| 11 mayo 2026 | T-004 | Dashboard métricas avanzado: filtro período, revenue por cupón, fuentes tráfico, cupones más usados, leads quiz, top productos con revenue, gráfica dinámica, pedidos por estado |

---

*Documento mantenido por P1 — Actualizar OBLIGATORIAMENTE en cada sesión con cambios de métricas.*
*Próxima actualización: al implementar cualquier ticket de la sección 6.2 o 6.3.*
