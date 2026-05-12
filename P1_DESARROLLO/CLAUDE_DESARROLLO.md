# CLAUDE_DESARROLLO.md — Framework de desarrollo web (P1)

> **Proyecto actual:** Pantera Essence — E-commerce de perfumería árabe, nicho y diseñador
> **Versión:** 15.0
> **Propietario:** Aureliano (Ingeniero Financiero)
> **Repo:** https://github.com/aureliano-tech/pantera-essence-web
> **Producción:** https://panteraessence.com
> **Última actualización:** 11 de mayo de 2026 (sesión P1 — Claude.ai)

---

## 1. ROL Y REGLAS FUNDAMENTALES

Claude Code actúa como desarrollador senior fullstack con expertise en React, Vite, Tailwind, Supabase, Vercel, SEO, UX/UI, seguridad web, e-commerce y diseño web. Siempre recomienda la solución más experta que requiera menos trabajo manual.

### Idioma
- Responder SIEMPRE en español
- Comentarios de código en español
- Mensajes para usuario final en español
- Variables, funciones y componentes en inglés
- Archivos: PascalCase (`ProductCard.jsx`)

### Metodología
- Resolver lógica ANTES de código
- Paso a paso — no saltar etapas
- Una instrucción a la vez — no avanzar sin resolver la anterior
- Probar SIEMPRE en localhost antes de push
- Ser directo — preguntar antes de asumir
- Actuar como experto en la materia del tema que se esté trabajando

### Flujo de trabajo
1. Claude.ai da instrucción exacta → 2. Aureliano pega en Claude Code → 3. Ejecuta → 4. Verifica localhost:5173 → 5. Commit + push → 6. Vercel redespliega (~1-2 min) → 7. Verifica producción

### Git
- Commit después de cada bloque funcional: `feat: descripción clara`
- MDs se actualizan siempre vía Claude Code: `docs: actualizar MDs sesión [fecha]`
- Nunca commitear .env
- Push inmediato después de cada commit

### Contexto del usuario
- Ingeniero financiero, experiencia en Excel/VBA, Python, SQL, Power BI
- Principiante en React/deploy web moderno
- Windows · Bucaramanga, Colombia · Moneda COP

---

## 2. METODOLOGÍA PROBADA — REPLICABLE A CUALQUIER PROYECTO

Esta sección documenta la arquitectura y patrones validados en producción. Sirve como base para levantar cualquier proyecto web nuevo con la misma calidad en una fracción del tiempo.

### 2.1 Arquitectura híbrida JSON + Supabase

```
┌─────────────────────────────────────────────────────┐
│  SITIO PÚBLICO                 PANEL ADMIN          │
│  Lee JSON local (rápido)       Lee/escribe Supabase │
│         ▲                            │              │
│         │         "Publicar"         │              │
│         └────── Supabase → JSON → GitHub ───────────┘
│                      → Vercel redeploy              │
└─────────────────────────────────────────────────────┘
```

- Sitio público lee JSON local → carga instantánea, sin dependencia de DB
- Panel admin lee/escribe Supabase → CRUD completo sin código
- Botón "Publicar" sincroniza: Supabase → JSON → GitHub API commit → Vercel redeploy
- "Publicar" ahora también exporta promotions.json (cupones activos)
- Si Supabase se cae → sitio sigue online (JSON local)
- Free tier alcanza para años con este modelo

### 2.2 Stack base replicable

| Capa | Tecnología | Por qué |
|---|---|---|
| Framework | React 18 + Vite | Rápido, HMR, build optimizado |
| Estilos | Tailwind CSS (público) + inline (admin) | Productivo, sin CSS-in-JS |
| DB + Auth + Storage | Supabase | Free tier generoso, RLS, REST API |
| Deploy | Vercel | Push = deploy, serverless incluido |
| DNS + CDN + Seguridad | Cloudflare (free) | Bot protection, DDoS, SSL |
| Pagos | Bold (Colombia) | Embed + hash serverless |
| Analytics | GA4 + Meta Pixel | Gratis, diferidos 5s post-load |
| IA | Claude Haiku API | Enriquecimiento de datos, generación contenido |
| Imágenes | Canvas API → WebP | Compresión en navegador, sin dependencias servidor |

### 2.3 Patrones de rendimiento

| Patrón | Cómo |
|---|---|
| Code splitting | React.lazy() + Suspense en todas las rutas |
| Fonts | Self-hosted en public/fonts/ (no CDN externo) |
| Imágenes | WebP obligatorio + lazy loading + Canvas compress 800px |
| Animaciones below-fold | IntersectionObserver (no Framer Motion global) |
| Scripts terceros | Diferidos 5s post-load |
| overflow-x | hidden en html/body/#root |

### 2.4 Patrones de seguridad

| Patrón | Cómo |
|---|---|
| Secretos | Función serverless en api/ — nunca en frontend |
| Variables | Con VITE_ = frontend. Sin VITE_ = solo servidor (Vercel dashboard) |
| Auth | Supabase Auth con sesión en sessionStorage |
| DB | RLS habilitado en tablas con datos sensibles |
| Headers | CSP, HSTS, X-Frame-Options, X-Content-Type |
| Bot protection | Cloudflare + rate limiting |
| Formularios | Honeypot anti-bot |

**Checklist antes de cada feature nueva:**
1. ¿Expone secreto al frontend? → mover a serverless
2. ¿Acepta input del usuario? → sanitizar
3. ¿Toca datos de clientes? → verificar RLS
4. ¿Agrega dependencia npm? → npm audit después
5. ¿Cambia rutas? → verificar vercel.json catch-all

### 2.5 Patrones de SEO

| Patrón | Implementación |
|---|---|
| Meta tags | OG + Twitter Cards en index.html + dinámicos por producto/blog |
| Datos estructurados | Schema.org JSON-LD en páginas de producto y blog |
| Blog SEO | Meta tags dinámicos (title, description) + Schema.org Article JSON-LD + renderizado markdown |
| Sitemap | public/sitemap.xml (estático, actualizar al agregar páginas) |
| robots.txt | Allow /, Disallow /admin /api/ |
| Blog | Artículos SEO generados con IA o escritos por P2 |
| Search Console | Propiedad verificada + sitemap enviado |

### 2.6 Patrones de UX/UI validados

| Decisión | Resultado |
|---|---|
| Hero tipográfico (sin imagen) | Carga instantánea, impacto editorial |
| 5 cards/fila en catálogo | Densidad óptima desktop |
| Paginación 20/40/60 | Velocidad + control del usuario |
| Estrellas siempre visibles (grises sin reseñas) | Simetría visual |
| Precio tachado automático (is_visible) | Incentivo sin fricción |
| Badge rojo -X% esquina superior izq | Patrón e-commerce universal |
| Placeholder con watermark 8% opacidad | No rompe catálogo sin foto |
| Popup timer 5s + exit intent desktop, claves sessionStorage independientes | No invasivo, doble oportunidad de conversión |
| Checkout híbrido (pasarela + transferencia) | Más métodos = más conversión |

### 2.7 Patrón features dinámicas sin deploy

Configuración en Supabase o JSON público → admin cambia → sitio refleja sin código ni redeploy.

Implementados: banner, costo envío, umbral envío gratis, cupones, popup, quiz.

### 2.8 Patrón de imágenes

- Upload → Canvas API compress (WebP, 800px, quality 0.7-0.8) en navegador
- Sin dependencias servidor (no Sharp, no Cloudinary)
- Supabase Storage (bucket público) para nuevas
- Archivos locales para legacy
- `resolveImg()` detecta http (Supabase) vs nombre local

### 2.9 Principio de eficiencia (aplica a TODOS los proyectos)

**Física:** priorizar free tiers, comprimir todo, minimizar llamadas API, monitorear uso mensual.

**Financiera:** NUNCA integrar servicio de pago sin avisar con costo en COP. Siempre presentar alternativa gratuita. Formato:
```
⚠️ COSTO: [servicio] — $[monto] COP/mes
Alternativa gratuita: [descripción]
¿Proceder con la opción de pago?
```

**Costos actuales:**
| Servicio | Costo |
|---|---|
| Vercel, Supabase, Cloudflare, GA4, Pixel | $0 (free tier) |
| Bold | ~2.49% + IVA por transacción |
| Claude API | ~$0.005 USD por producto |
| Dominio | ~$40.000 COP/año |

### 2.10 Patrón de analytics e-commerce

Todos los eventos de tracking siguen el mismo patrón: guard + disparo simultáneo Meta Pixel + GA4.

```js
// Meta Pixel
if (typeof fbq !== 'undefined') {
  fbq('track', 'EventName', { /* payload */ })
}
// GA4
if (typeof gtag !== 'undefined') {
  gtag('event', 'event_name', { /* Enhanced E-commerce payload */ })
}
```

Eventos implementados:

| Evento | Pixel | GA4 | Archivo |
|---|---|---|---|
| Ver producto | ViewContent | view_item | ProductDetail.jsx |
| Agregar al carrito | AddToCart | add_to_cart | CartContext.jsx |
| Iniciar checkout | InitiateCheckout | begin_checkout | Checkout.jsx |
| Compra completada | Purchase | purchase | Checkout.jsx (x2: Bold + transferencia) |
| Lead quiz | Lead | — | Quiz.jsx |

### 2.11 Patrón de requerimientos inter-direcciones (TICKETS.md)

Sistema de tickets para gestionar solicitudes entre direcciones del proyecto:
- Archivo `TICKETS.md` en la raíz del repo
- Formato: ID, origen, destino, prioridad, estado, evaluación técnica
- Regla: no ejecutar nada de otra dirección sin ticket registrado
- Respuestas formales: `RESPUESTA_P[N]_[FECHA].md`
- Todo requerimiento de P2/P3/P4 pasa por evaluación técnica de P1 antes de ejecutarse

### 2.12 Patrón de auditoría (audit log)

Sistema de auditoría en todos los módulos admin:
- `logAudit(action, entity, entityId, details)` en `utils/auditLog.js`
- Registra: acción, entidad, entity_id, detalle con diff campo por campo, admin_email
- Al editar: compara snapshot (estado al abrir modal) vs valores nuevos, registra solo campos que cambiaron
- Formato diff: `"Editado: Producto X | price: $150.000 → $160.000 | gender: mujer → unisex"`
- Módulos con logAudit: Products, Promotions, Orders, Blog, Reviews, Quiz, CampaignSpend, Config
- Tab Auditoría en /admin/config: filtros entidad/fecha/búsqueda, paginación 50/página, export CSV, fila expandible

### 2.13 Patrón de API pública para inter-direcciones

Endpoint `/api/catalog` que expone datos del catálogo para consumo de P2/P3/P4:
- Lee products.json y promotions.json (archivos locales, sin dependencia de Supabase en runtime)
- Devuelve: productos con precios, descuentos calculados, cupones activos
- CORS: `Access-Control-Allow-Origin: *` (público)
- Cache: 5 minutos (se invalida con cada "Publicar cambios")
- Se actualiza automáticamente cuando admin publica cambios
- P2/P3/P4 consultan `https://panteraessence.com/api/catalog` al iniciar sesiones

---

## 3. PANTERA ESSENCE — DATOS DEL PROYECTO

### 3.1 El negocio

| Dato | Valor |
|---|---|
| Tagline | "Tu lujo. Tu valor. Tu esencia." |
| Categorías | Árabe (116) · Diseñador (16) · Nicho (19) = 151 productos |
| WhatsApp | +57 350 306 7121 |
| Email | panteraessence@gmail.com |
| Redes | @panteraessence (IG) · @pantera_essence (TikTok) |
| Puntos físicos | 3 en Piedecuesta, Santander |
| Envío | Dinámico desde siteConfig.json (actual: $17.500 / gratis ≥$260K) |
| Transportadoras | Interrapidísimo, Servientrega, 472 |

### 3.2 Paleta de marca

```css
:root {
  --negro-carbon: #0a0807;    --oro-envejecido: #c9a35a;
  --crema-suave: #f4ead8;     --oud-profundo: #3a1a14;
  --humo-sutil: #1a1a1a;
  --mundo-arabe-bg: #3a1a14;    --mundo-arabe-accent: #c9a35a;
  --mundo-disenador-bg: #1a1a2e; --mundo-disenador-accent: #7b8fc9;
  --mundo-nicho-bg: #2d0a0a;    --mundo-nicho-accent: #c94a4a;
  --font-display: 'Cormorant Garamond', serif;
  --font-body: 'Marcellus', serif;
}
```

Logos: watermark.png (header 66px + marginTop 20px, favicon) · logo-dark.png (footer)

### 3.3 Funciones serverless

| Función | Runtime | Uso |
|---|---|---|
| api/bold-hash.js | Edge | Hash SHA256 Bold |
| api/complete-products.js | Edge | Enriquecimiento IA (carga masiva) |
| api/generate-blog.js | Node.js 60s | Generación artículos blog. Parseo con separadores `---KEY---` |
| api/sync-products.js | Node.js | Sync Supabase → JSON (products + promotions) → GitHub → Vercel redeploy |
| api/catalog.js | Edge | API pública catálogo para P2/P3/P4. Lee JSON local, CORS *, cache 5min |

### 3.4 Tablas Supabase

| Tabla | RLS | Uso |
|---|---|---|
| orders | ✅ | Pedidos e-commerce. Campos: utm_source, utm_medium, utm_campaign, utm_content |
| products | ✅ | Catálogo para admin. Campos: sort_position (manual, nullable), sort_score (auto) |
| promotions | ✅ | Cupones + descuentos visibles. Campos: is_visible, gender_scope, end_date, product_ids (array SKUs) |
| coupon_usage | ✅ | Control uso cupones por cliente. unique(coupon_code, customer_email) |
| campaign_spend | ✅ | Gasto publicitario por campaña. Campos: campaign_name, platform, spend, period_start, period_end |
| blog_posts | ⚠️ Off | Artículos blog (anon key necesita escribir). Campos: meta_title, meta_description |
| quiz_config | ⚠️ Off | Config quiz (misma razón) |
| leads | ✅ | Captura quiz (name, contact, quiz_answers) |
| audit_log | ✅ | Acciones del admin con diff detallado |
| reviews | ✅ | Reseñas de productos. Campos: product_id, stars, chips[], comment, name, city, status (pending/approved/rejected) |

Storage: product-images (WebP 0.8) · blog-images (WebP 0.7) — ambos públicos.

### 3.5 Arquitectura de rutas

```
/ .......................... Home (banner dinámico + hero + mundos + destacados + quiz CTA)
/arabe, /disenador, /nicho . Landing por mundo
/catalogo .................. Catálogo (filtros, búsqueda, paginación, 5 cards/fila)
/producto/:slug ............ Detalle (galería + pirámide + decant + Schema.org JSON-LD)
/nosotros, /contacto ....... Institucionales
/blog, /blog/:slug ......... Blog SEO (meta tags dinámicos + Schema.org Article JSON-LD + markdown)
/quiz ...................... Quiz 4 preguntas + matching + leads
/checkout .................. Checkout híbrido Bold + transferencia
/confirmacion .............. Post-compra
/api/catalog ............... API pública catálogo (JSON, CORS *, cache 5min)
/admin ..................... Login Supabase Auth (sesión 8h)
  /dashboard ............... Métricas reales + rendimiento por campaña (ROAS/CPA/ticket)
  /campanas ................ Gestión gasto publicitario por campaña
  /productos ............... CRUD + fotos max 5 + drag & drop + carga masiva IA
  /blog .................... CRUD + imagen + generación IA
  /resenas ................. Moderación reseñas: aprobar/rechazar, badge pendientes
  /promociones ............. CRUD cupones + is_visible + gender_scope + product_ids
  /pedidos ................. Pedidos + guías + transportadoras + UTM fuente tráfico
  /config .................. 5 tabs: negocio, keys, seguridad, auditoría (filtros/paginación/export/diff), mantenimiento
  /quiz .................... Config preguntas + productos destacados
```

### 3.6 Variables de entorno

**En .env local + Vercel dashboard (VITE_):**
```
VITE_BOLD_API_KEY · VITE_SUPABASE_URL · VITE_SUPABASE_ANON_KEY
```

**Solo Vercel dashboard (sin VITE_, nunca en .env):**
```
BOLD_SECRET_KEY · ANTHROPIC_API_KEY · GITHUB_TOKEN (expira May 9, 2027) · RESEND_API_KEY (pendiente)
```

⚠️ .env en .gitignore. NUNCA pegar API keys en el chat.

---

## 4. REGLAS TÉCNICAS PERMANENTES

### Imports .jsx (OBLIGATORIO)
```js
// SIEMPRE extensión .jsx en imports locales
import Foo from './Foo.jsx'           // ✅
import Foo from './Foo'               // ❌ falla en Rollup (producción)
lazy(() => import('./pages/Foo.jsx')) // ✅
```

### sbFetch headers (OBLIGATORIO)
```js
// Extraer headers ANTES del spread
const { headers: extraHeaders, ...restOptions } = options
fetch(url, { headers: { ...API_HEADERS, ...extraHeaders }, ...restOptions })
```

### resolveImg()
```js
function resolveImg(img) {
  if (!img) return ''
  if (img.startsWith('http')) return img  // Supabase Storage
  return imgUrl(img)                       // archivo local
}
```

### Meta Pixel (OBLIGATORIO — guard en todos los eventos)
```js
if (typeof fbq !== 'undefined') {
  fbq('track', 'EventName', { /* payload */ })
}
```
Eventos implementados: ViewContent (ProductDetail), AddToCart (CartContext), InitiateCheckout (Checkout mount), Purchase (tras saveOrder), Lead (Quiz submit).

### GA4 Enhanced E-commerce (OBLIGATORIO — guard en todos los eventos)
```js
if (typeof gtag !== 'undefined') {
  gtag('event', 'event_name', {
    currency: 'COP',
    value: precio,
    items: [{ item_id, item_name, item_brand, item_category, price, quantity }]
  })
}
```
Eventos implementados: view_item (ProductDetail), add_to_cart (CartContext), begin_checkout (Checkout), purchase (Checkout x2: Bold + transferencia).

### Reglas de negocio
| Regla | Detalle |
|---|---|
| Cupones | 100% dinámicos desde Supabase — NUNCA hardcodear |
| Cupones acumulación | NO acumulables con descuentos visibles (is_visible = true) |
| Cupón por cliente | 3 capas: localStorage + coupon_usage Supabase + constraint DB unique |
| Decants | ≤$250K → $30K · $250K-$300K → $35K · >$300K → sin decant |
| Montale Paris | Siempre categoría nicho |
| is_featured | Máximo 4 productos simultáneos |
| Fotos | Max 5 por producto |
| Nombre en card | Sin duplicar marca (ya es label) |
| Orden catálogo | sort_position fija (1-8) + sort_score automático (9+) + intercalado anti-repetición de marca |
| UTM tracking | First-touch, sessionStorage con prefijo pe_, guardado en orders |

### Regla de cupones (P2)
- P1 NO crea, modifica ni elimina cupones sin aprobación de P2
- Los cupones son parte de la estrategia de ventas y afectan ads, WhatsApp y comunicación
- Cupones inactivos NO se eliminan — sirven para métricas históricas
- Cualquier cambio en promociones requiere alineación con P2

### Cupones activos (Supabase)
| Código | Descuento | Vigencia | Scope | is_visible |
|---|---|---|---|---|
| PRIMERA10 | 10% | Permanente | Global | No |
| PAPA2026 | 25% | Hasta 15 junio 2026 | Solo hombre+unisex (6 SKUs) | No |

> **Nota:** Cupones inactivos en Supabase (no eliminar — métricas históricas): PANTERA15, OFERTA20, PRIMERA25, MAMA2026. OFERTA20 desactivado como global — descuentos visibles ahora por producto individual mediante `product_ids`. El campo `gender_scope` soporta multi-valor separado por coma ("hombre,unisex"). Exit intent popup usa PRIMERA10 específicamente (cupón confirmado con P2).

---

## 5. ESTRUCTURA DEL PROYECTO

```
pantera-essence-web/
├── .env                         (NO en Git)
├── vercel.json                  rewrites: api/* + SPA catch-all
├── CLAUDE.md                    estado técnico (dentro del repo, actualiza Claude Code)
├── TICKETS.md                   requerimientos inter-direcciones (P2→P1, P3→P1, P4→P1)
├── RESPUESTA_P2_*.md            reportes de entrega a P2
├── api/                         bold-hash, complete-products, generate-blog, sync-products, catalog
├── public/
│   ├── fonts/                   Cormorant + Marcellus self-hosted
│   ├── siteConfig.json          Banner + envío dinámico
│   ├── robots.txt + sitemap.xml
│   └── images/brand/ + products/  Logos + 437 fotos WebP
├── src/
│   ├── components/
│   │   ├── layout/              Header, Footer, PromoBanner, WhatsApp, ScrollToTop
│   │   ├── home/                Hero, WorldSelector, ValueProposition, Featured, QuizBanner
│   │   ├── catalog/             Filters, SearchBar, SortSelect, ProductCard
│   │   ├── product/             ProductGallery, OlfactoryPyramid
│   │   ├── cart/                CartDrawer, CartItem
│   │   ├── worlds/              WorldPage (reutilizable)
│   │   └── ui/                  QuickReview, ReviewsList, PromoPopup
│   ├── context/                 CartContext (addToCart + Pixel + GA4), VisiblePromosProvider
│   ├── data/                    products.json, reviews.json, blogPosts.json, promotions.json, colombiaLocations.js
│   ├── pages/                   Home, Catalog, ProductDetail, Quiz, Checkout, etc.
│   │   └── admin/               Dashboard, CampaignSpend, Products, Blog, Promotions, Orders, Reviews, Config, Quiz
│   └── utils/                   formatPrice, slugify, analytics, imgUrl, supabase, supabaseAuth, auditLog, useHoneypot
```

---

## 6. PAGOS — BOLD + TRANSFERENCIA

### Bold
- Checkout embebido + hash integridad en api/bold-hash.js
- Métodos: tarjeta, PSE, Nequi, DaviPlata, Bancolombia
- Redirección: /confirmacion (solo producción)
- Guardar pedido ANTES de abrir pasarela

### Transferencia directa
| Método | Número |
|---|---|
| Nequi / DaviPlata | 317 437 6647 |
| Bancolombia Ahorros | 020 4211 0887 |
Titular: Rho**** Fer**** Uri**** Cas****

---

## 7. SEGURIDAD

### Estado actual
✅ Hash Bold serverless · ✅ Variables seguras Vercel · ✅ RLS en orders/products/promotions/campaign_spend
✅ Supabase Auth · ✅ Cloudflare Bot Protection + Rate limiting
✅ Security headers (CSP, HSTS, X-Frame, X-Content-Type) · ✅ CORS serverless · ✅ useHoneypot
✅ Audit log con diff detallado en todos los módulos admin
⬜ JWT propio · ⬜ 2FA admin · ⬜ Backup automático DB

### Rotación de keys
| Key | Frecuencia |
|---|---|
| Bold API/Secret | Cada 12 meses o si se compromete |
| Supabase Anon | Solo si se compromete |
| Anthropic API | Cada 12 meses o si se compromete |
| GITHUB_TOKEN | Expira May 9, 2027 |
| Contraseña admin | Cada 3 meses |

### Manejo de incidentes
1. Key comprometida → revocar → generar nueva → Vercel → redeploy
2. Acceso no autorizado → cambiar contraseña → cerrar sesiones → revisar audit_log → rotar keys
3. Inyección de datos → audit_log → restaurar → sanitizar

### Plan de mejora
- Fase 1: JWT propio, rate limiting login, políticas RLS por auth.uid()
- Fase 2: 2FA TOTP, CORS estricto, IP whitelist admin, sanitización inputs
- Fase 3: Webhooks alertas, logs seguridad 1 año, backup automático semanal
- Fase 4: Pen testing trimestral, npm audit mensual, auditoría RLS semestral

### Política de retención de datos
- orders, campaign_spend, reviews, leads: conservar TODO (historial de negocio)
- audit_log: limpiar registros >6 meses. Exportar CSV antes de limpiar. Recordatorio en checklist trimestral

---

## 8. MANTENIMIENTO Y OPERACIONES

### Operaciones desde panel admin
| Módulo | Funcionalidades clave |
|---|---|
| /admin/dashboard | KPIs + rendimiento por campaña (ROAS/CPA/ticket) con filtro período |
| /admin/campanas | Registrar gasto publicitario por campaña, plataforma, período |
| /admin/productos | CRUD + fotos max 5 + drag & drop + carga masiva Excel/CSV + IA + sort_position |
| /admin/blog | CRUD + imagen + generación IA (Claude Haiku) + meta_title + meta_description |
| /admin/promociones | CRUD cupones + is_visible + gender_scope + product_ids (por producto) |
| /admin/pedidos | Lista + estados + guías + transportadoras + UTM fuente tráfico |
| /admin/resenas | Moderación reseñas: aprobar/rechazar, filtros, búsqueda, paginación, badge rojo pendientes |
| /admin/quiz | Preguntas + opciones + productos destacados |
| /admin/config | Negocio, API keys, seguridad, auditoría (filtros/paginación/export CSV/diff detallado), mantenimiento |
| 📦 Publicar cambios | Sync Supabase → JSON (products + promotions) → GitHub → Vercel redeploy |

### Requerimientos inter-direcciones
Todos los requerimientos de P2, P3 o P4 hacia P1 se registran en `TICKETS.md` en la raíz del repo.
- Formato: ticket con ID, origen, prioridad, estado, evaluación técnica
- Regla: no ejecutar nada sin ticket registrado primero
- Actualizar estados en cada sesión de trabajo
- Respuestas formales: `RESPUESTA_P[N]_[FECHA].md`
- Commit: `docs: actualizar TICKETS.md`

### Fórmula del SKU
`MARCA-NOMBRE-##` (ej: AFN-9PNO-01)

| Marca | Abrev. | Marca | Abrev. |
|---|---|---|---|
| Afnan | AFN | Lattafa | LAT |
| Al Haramain | ALH | Rasasi | RAS |
| Armaf | ARM | Maison Alhambra | MAH |

### Accesos a dashboards
| Sistema | URL |
|---|---|
| Admin local / prod | localhost:5173/admin · panteraessence.com/admin |
| API catálogo | panteraessence.com/api/catalog |
| Vercel | vercel.com/dashboard |
| Supabase | supabase.com/dashboard |
| Cloudflare | dash.cloudflare.com |
| Bold | commerce.bold.co |
| Anthropic | console.anthropic.com |
| Meta Business | business.facebook.com |
| GA4 | analytics.google.com |
| Search Console | search.google.com/search-console |

### Checklists
**Semanal:** revisar pedidos · verificar sitio en producción · WhatsApp · P2 registra gasto campañas (viernes)
**Mensual:** npm audit · uso Supabase (500MB/50K filas) · logs Vercel · métricas GA4 · cupones vigentes · RLS activo
**Trimestral:** Lighthouse (>90) · npm outdated · rotar contraseña · auditar RLS · limpiar imágenes huérfanas · exportar y limpiar audit_log >6 meses

### Solución de problemas
| Problema | Solución |
|---|---|
| Sitio no carga en prod | Vercel → logs build → import sin .jsx es lo más común |
| Admin en blanco | F12 → "Failed to fetch dynamically imported module" → agregar .jsx |
| Imágenes no se ven | Verificar WebP local o bucket público Supabase |
| Carga masiva falla | ANTHROPIC_API_KEY en Vercel → logs api/complete-products |
| Fotos no suben | Buckets existen + son públicos + F12 para error |
| Bold no procesa | BOLD_SECRET_KEY en Vercel → logs api/bold-hash |
| /admin 404 en prod | vercel.json: regla API primero, luego catch-all SPA |
| Login no funciona | Supabase Auth → Users → verificar email confirmado |
| git push rejected | `git pull origin master --rebase` → push |
| Pixel no dispara | `typeof fbq !== 'undefined'` en F12 → verificar carga diferida |
| GA4 no dispara | `typeof gtag !== 'undefined'` en F12 → verificar carga diferida |
| Publicar cambios 404 localhost | Normal — funciones serverless solo corren en Vercel, probar en producción |

---

## 9. RENDIMIENTO Y ESTADO

### Lighthouse actual
| Métrica | V1 | Actual |
|---|---|---|
| Performance | 76 | 87-90 |
| Accessibility | 96 | 96 |
| Best Practices | 81 | 100 |
| SEO | 92 | 100 |

### Productos pendientes de fotos (17)
Subir desde /admin/productos → Editar → Fotos (max 5, compresión automática).

AFN-SG-01, AFN-SIH-01, ALH-AOGEE-01, ALH-AOGEE-02, ARM-TPKTMS-01, AZZ-TMW-01, AZZ-WM-01, CAC-AAEDP-01, ISSM-LDPH-01, KATP-M-01, LAT-AG-01, LAT-MBE-01, LAT-ML-01, LATP-AQG-01, MOS-T2-01, MOS-TB-01, PARH-RR-01

### Pendientes próximas sesiones

**Alta:**
1. T-007B: Email post-entrega Resend (API key pendiente en Vercel)
2. Revisión completa versión móvil (layout, navegación, UX en dispositivos reales)
3. Fix logo pantera que se sale del banner en móvil
4. Fix admin_email "desconocido" en audit_log
5. Revertir precio Emper Stallion 53 a $190.000 (cambio de prueba)
6. Ampliar catálogo: 20 diseñador + 20 nicho
7. Vincular Pixel al conjunto de datos de Meta Ads (tarea de P4, no P1)

**Media:**
8. Actualizar ANALYTICS_P2.md con T-016 (ROAS)
9. Quiz: 2 productos nicho (hombre+oud, unisex+cítrica)
10. Fotos 17 productos pendientes

**Baja:**
11. Conexión Config → Checkout datos bancarios (leer desde Supabase)
12. Email/WhatsApp post-compra automático
13. Carrito abandonado
14. Chat IA integrado · PWA · 2FA admin · Backup automático DB

### Progreso completado
- **V1 ✅** — E-commerce completo: hero, catálogo, producto, carrito, checkout, quiz, blog, reseñas, WebP, deploy
- **V2 ✅** — Panel admin: auth, dashboard, CRUD todo, carga masiva IA, fotos Storage, config, auditoría
- **9 mayo ✅** — Sync products, code splitting, self-host fonts, rendimiento 87-90, dominio, Cloudflare, seguridad V3, Search Console
- **10 mayo (día) ✅** — 151 productos, 437 fotos, quiz 4 resultados + leads, generate-blog IA, descuentos visibles, popup, banner dinámico, cupones dinámicos Supabase, max 5 fotos, Schema.org, drag & drop fotos
- **10 mayo (noche) ✅** — Meta Pixel 5 eventos, UTM tracking, orden catálogo sort_position+sort_score+intercalado, cupones por cliente 3 capas, descuentos visibles por producto, banner, badge+precio tachado FeaturedProducts
- **11 mayo (sesión 1) ✅** — GA4 eventos e-commerce, BlogPost.jsx mejorado (meta tags SEO dinámicos, Schema.org Article JSON-LD), artículo Khamrah, cupón PAPA2026, sistema TICKETS.md, respuesta formal P2
- **11 mayo (sesión 2) ✅** — Dashboard métricas avanzado T-004, Sistema reseñas T-007A, fix conteo productos, padding uniforme, ResizeObserver header
- **12 mayo ✅** — T-006 popup exit intent, T-012 Schema Product, T-013 meta tags SEO dinámicos, T-014 sort_position 1-8, T-015 /blog verificado, multi-select género cupones, badges confianza, fix global botones móvil 44px
- **13 mayo ✅** — T-016 ROAS por campaña (CampaignSpend + dashboard rendimiento), API pública /api/catalog, sync promotions.json, limpieza datos prueba Supabase, sistema auditoría robusto (filtros/paginación/export CSV/diff detallado/logAudit en 7 módulos)

---

## PROTOCOLO DE CIERRE DE SESIÓN — OBLIGATORIO P1

> Ejecutar al final de CADA sesión, sin excepción.

### Paso 1 — Verificación final (si hubo cambios en código)
- [ ] Cambios verificados en localhost
- [ ] `git commit` + `git push` realizado
- [ ] Verificado en panteraessence.com (producción)
- [ ] TICKETS.md actualizado (ticket completado o avanzado)

### Paso 2 — Cierre formal
Al terminar, Aureliano escribe en el chat: **"cierra sesión P1"**

Claude genera UN solo comando Python listo para copiar y pegar en PowerShell:

```powershell
cd C:\Users\USUARIO\Desktop\gerencia-pantera-essence
python github_sync.py "P1" "### [FECHA] — P1 DESARROLLO
**Qué se hizo:** [resumen de lo que se hizo en la sesión]
**Afecta a:** [P2 / P3 / P4 / Gerencia / Aureliano — según corresponda]
**MD actualizado:** [lista de archivos MD actualizados]
**Acción requerida:** [qué debe hacer cada dirección afectada]
**Estado:** ⬜ Pendiente"
```

**Reglas del comando de cierre:**
- El resumen debe ser concreto: qué se construyó, qué se arregló, qué se planificó
- Solo incluir en "Afecta a" las direcciones que realmente necesitan actuar
- "Acción requerida" debe ser específica: "[dirección]: [acción concreta]"
- Si la sesión fue solo de planificación (Claude.ai), indicarlo
- Si no hubo cambios que afecten a otras direcciones, el comando igual se genera con "Sin impacto inter-direcciones"

### Paso 3 — Aureliano ejecuta
1. Abre PowerShell
2. Pega el comando generado
3. `github_sync.py` sube los archivos MD a `P1_DESARROLLO/` y la entrada a `SINCRONIZACION/CAMBIOS.md`

### Paso 4 — Apertura de próxima sesión P1
Boot mínimo:
```
Eres el Director de Desarrollo Web de Pantera Essence. P1.
[PEGAR CLAUDE_DESARROLLO.md]
[PEGAR otros MDs relevantes]

Última sesión: [fecha]
Instrucción de hoy: [tarea]
```

**Repositorio gerencia:** https://github.com/aureliano-tech/gerencia-pantera-essence
**Script:** `C:\Users\USUARIO\Desktop\gerencia-pantera-essence\github_sync.py`
**Carpeta P1:** `P1_DESARROLLO/`
**Carpeta sync:** `SINCRONIZACION/`

---

*Protocolo de cierre actualizado: 11 de mayo de 2026 — v15 con github_sync.py automatizado*
*Última actualización: 11 de mayo de 2026*
