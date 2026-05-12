# MANTENIMIENTO.md — Guía de operaciones de Pantera Essence Web

> **Proyecto:** Pantera Essence — E-commerce de perfumería
> **Versión:** 10.0
> **Última actualización:** 10 de mayo de 2026
> **Responsable:** Aureliano

---

## 1. Cómo iniciar una sesión de trabajo

### Opción A — Claude.ai (planear cambios)
1. Abrir conversación nueva en https://claude.ai
2. Adjuntar: `PANTERA_ESSENCE_MASTER.md` + `CLAUDE.md` + `MANTENIMIENTO.md`
3. Mensaje inicial: "Lee estos archivos. Eres el arquitecto de Pantera Essence."
4. Claude.ai da instrucciones exactas → Aureliano las pega en Claude Code

### Opción B — Claude Code (ejecutar cambios)
1. VS Code en carpeta `pantera-essence-web`
2. Terminal: `claude --dangerously-skip-permissions`
3. Claude Code lee CLAUDE.md automáticamente

### Cuándo usar cada uno
| Situación | Usar |
|---|---|
| Planear cambio grande o tomar decisión | Claude.ai |
| Ejecutar cambio concreto sobre el código | Claude Code |
| Agregar productos, precios, fotos, blog | Panel admin V2 |
| Carga masiva Excel | Panel admin V2 |

---

## 2. Flujo de mantenimiento — 8 pasos

| Paso | Acción |
|---|---|
| 1 | Abrir VS Code en `pantera-essence-web` |
| 2 | Terminal 1: `npm run dev` → localhost:5173 |
| 3 | Terminal 2: `claude` (o `claude --dangerously-skip-permissions`) |
| 4 | Pegar instrucción en Claude Code |
| 5 | Verificar en navegador (Ctrl+Shift+R) |
| 6 | `git commit` + `git push` |
| 7 | Vercel redespliega automático (~1-2 min) |
| 8 | Verificar en panteraessence.com |

> **Regla de oro:** nunca hacer push sin verificar en localhost primero.

---

## 3. Operaciones desde el panel admin

### Productos (/admin/productos)
- **Agregar:** Nuevo producto → formulario completo → Guardar
- **Editar:** Buscar → Editar → cambiar campos → Guardar
- **Fotos:** Editar → sección Fotos → + Agregar foto (max 5, compresión automática WebP)
- **Drag & drop:** reordenar fotos arrastrando
- **Eliminar:** con confirmación (fotos en Supabase Storage quedan huérfanas — eliminar manualmente si necesario)
- **Carga masiva:** botón Carga masiva → subir Excel/CSV (SKU, Nombre, Marca, ml, Precio) → Enriquecer con IA → Insertar en Supabase

### Blog (/admin/blog)
- **Crear artículo:** Nuevo artículo → llenar campos → subir imagen (compresión automática) → Guardar
- **Generar con IA:** botón "Generar artículo con IA" → tema opcional → esperar 15-30s → revisar → Guardar
- **Editar/eliminar:** en la lista de artículos

### Promociones (/admin/promociones)
- **Crear cupón:** Nuevo cupón → código, tipo (porcentaje/fijo), valor, fechas, scope → Guardar
- **Descuento visible:** activar toggle "Visible en catálogo" → aparece precio tachado en cards sin cupón
- **Gender scope:** filtrar por género (all/hombre/mujer/unisex)
- **Desactivar:** toggle is_active o desactivar is_visible

### Publicar cambios al sitio público
1. Hacer cambios en el admin (productos, precios, etc.)
2. Presionar botón "📦 Publicar cambios" (verde, barra superior)
3. Esperar confirmación de sincronización
4. Vercel redespliega automáticamente (~1-2 min)
5. Verificar en panteraessence.com

> Internamente: Supabase → JSON → GitHub API commit → Vercel redeploy

---

## 4. Fórmula del SKU

`MARCA-NOMBRE-##`
- **MARCA:** abreviatura 3-4 letras mayúsculas
- **NOMBRE:** iniciales del producto
- **##:** secuencial (01, 02 para variantes)

| Marca | Abreviatura |
|---|---|
| Afnan | AFN |
| Al Haramain | ALH |
| Armaf | ARM |
| Lattafa | LAT |
| Rasasi | RAS |
| Maison Alhambra | MAH |
| Fragrance World | FRW |
| Ard Al Zaafaran | AAZ |

---

## 5. Reglas de negocio para campos de producto

| Campo | Valores válidos | Regla |
|---|---|---|
| category | arabe, disenador, nicho | Montale Paris = siempre nicho |
| family | amaderada, citrica, especiada, floral, oriental, oud | Coincidir con filtros |
| gender | hombre, mujer, unisex | Filtro de género |
| occasion | casual, deporte, dia, evento, noche, oficina | Usado en quiz |
| has_decant | true si precio ≤ $300.000 | Obligatorio |
| decant_price | $30.000 si ≤$250K / $35.000 si $250K-$300K | Obligatorio |
| is_featured | true solo para los 4 del home | Máximo 4 simultáneos |
| images | Array de nombres WebP o URLs http | Max 5 fotos |

---

## 6. Actualizar llaves API

### Bold
| Llave | Dónde |
|---|---|
| VITE_BOLD_API_KEY | .env local + Vercel dashboard |
| BOLD_SECRET_KEY | Solo Vercel dashboard (nunca en código) |

### Supabase
| Variable | Dónde |
|---|---|
| VITE_SUPABASE_URL | .env local + Vercel dashboard |
| VITE_SUPABASE_ANON_KEY | .env local + Vercel dashboard |

### Anthropic / GitHub
| Variable | Dónde |
|---|---|
| ANTHROPIC_API_KEY | Solo Vercel dashboard |
| GITHUB_TOKEN | Solo Vercel dashboard (expira May 9, 2027) |

### Meta Pixel / GA4
| Servicio | ID actual | Ubicación |
|---|---|---|
| Meta Pixel | 1478179957390831 | index.html |
| GA4 | G-JNEQ0RXTJB | index.html |

Para cambiar IDs, instrucción a Claude Code: "En index.html, reemplaza el ID [viejo] por [nuevo] en todas las ocurrencias."

---

## 7. Tabla de accesos a dashboards

| Sistema | URL |
|---|---|
| Panel admin (local) | http://localhost:5173/admin |
| Panel admin (prod) | https://panteraessence.com/admin |
| Sitio producción | https://panteraessence.com |
| Vercel | https://vercel.com/dashboard |
| GitHub | https://github.com/aureliano-tech/pantera-essence-web |
| Supabase | https://supabase.com/dashboard |
| Cloudflare | https://dash.cloudflare.com |
| Bold | https://commerce.bold.co |
| Anthropic | https://console.anthropic.com |
| Meta Business | https://business.facebook.com |
| GA4 | https://analytics.google.com |
| Search Console | https://search.google.com/search-console |

---

## 8. Checklists de mantenimiento

### Semanal
- [ ] Revisar pedidos nuevos en Supabase (tabla orders)
- [ ] Verificar que el sitio carga en producción
- [ ] Revisar WhatsApp y consultas de clientes

### Mensual
- [ ] `npm audit` y corregir vulnerabilidades
- [ ] Revisar uso de Supabase (storage + filas vs free tier: 500MB / 50K filas)
- [ ] Revisar logs Vercel (bold-hash, complete-products)
- [ ] Revisar métricas GA4 y Meta Business
- [ ] Verificar cupones activos y vigentes
- [ ] Verificar RLS activo en tablas principales

### Trimestral
- [ ] Lighthouse (objetivo: Performance >90)
- [ ] `npm outdated` + actualizar dependencias
- [ ] Rotar contraseña admin
- [ ] Revisar políticas RLS
- [ ] Limpiar imágenes huérfanas en Supabase Storage
- [ ] Evaluar agregar productos nuevos al catálogo

---

## 9. Solución de problemas comunes

### Sitio no carga en producción
1. Vercel dashboard → revisar último deploy → logs de build
2. Error más común: import sin extensión .jsx
3. Solución: corregir localmente → verificar localhost → push

### Página admin en blanco
- Causa: imports sin `.jsx` (Vite dev resuelve, Rollup producción no)
- Diagnóstico: F12 → Console → "Failed to fetch dynamically imported module"
- Solución: agregar `.jsx` a todos los imports locales

### Imágenes no se ven
1. Imagen local: verificar WebP en `public/images/products/`
2. Imagen Supabase: verificar bucket público y URL correcta
3. En producción: esperar 5 min + Ctrl+Shift+R

### Carga masiva IA no funciona
1. Verificar ANTHROPIC_API_KEY en Vercel dashboard
2. Vercel → Functions → Logs → api/complete-products
3. Error 401: key inválida. Error 500: formato Excel incorrecto

### Fotos no se suben desde admin
1. Verificar buckets product-images / blog-images existen y son públicos
2. F12 → Console para ver error exacto
3. Común: RLS bloqueando upload

### Bold no procesa pago
1. Verificar BOLD_SECRET_KEY en Vercel dashboard
2. Verificar VITE_BOLD_API_KEY en .env + Vercel
3. Revisar logs Vercel → Functions → api/bold-hash

### Ruta /admin 404 en producción
- Verificar vercel.json: regla API primero, luego catch-all SPA
```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/$1" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Login admin no funciona
1. Verificar usuario en Supabase → Authentication → Users
2. "Invalid login credentials": email o contraseña incorrecto
3. "Email not confirmed": confirmar manualmente en Supabase Auth

### Error git push "rejected non-fast-forward"
```
git pull origin master
```
Resolver conflictos si los hay, luego push de nuevo.

---

*Guía mantenida por Aureliano — actualizar en cada hito importante.*
