# PLAN DE SEGURIDAD — Pantera Essence

> Proyecto: Pantera Essence — E-commerce de perfumería
> Versión: 1.0
> Fecha: 9 de mayo de 2026
> Responsable: Aureliano
> Clasificación: Confidencial

## 1. Estado actual de seguridad (V2)

### Implementado ✅
- HTTPS automático vía Vercel (SSL/TLS)
- Row Level Security (RLS) habilitado en orders, products, promotions — ver tabla de estado por tabla
- Hash de integridad de Bold generado en función serverless (api/bold-hash.js) — llave secreta nunca expuesta al frontend
- Variables sensibles en Vercel Environment Variables (BOLD_SECRET_KEY, ANTHROPIC_API_KEY)
- Variables del frontend con prefijo VITE_ separadas de variables del servidor
- Archivo .env en .gitignore — nunca se sube a GitHub
- Panel admin en ruta /admin no visible en navegación pública
- Sesión admin con expiración de 8 horas (JWT en sessionStorage)
- Keys enmascaradas en panel de configuración (solo últimos 4 caracteres visibles)
- Tabla audit_log para registrar todas las acciones del admin
- Checklist de seguridad visual en el panel de configuración

### Estado RLS por tabla
| Tabla | RLS | Estado | Razón |
|---|---|---|---|
| orders | ✅ Habilitado | Producción | Datos de clientes — protegidos |
| products | ✅ Habilitado | Producción | Catálogo — solo admin puede modificar |
| promotions | ✅ Habilitado | Producción | Cupones — solo admin puede modificar |
| blog_posts | ⚠️ Deshabilitado | Intencional | Operaciones de escritura del admin con anon key no pasan RLS por defecto |
| quiz_config | ⚠️ Deshabilitado | Intencional | Misma razón — anon key no tiene rol de admin en Supabase |
| reviews | N/A | Pendiente implementación | — |

### Vulnerabilidades conocidas ⚠️
- Credenciales del admin gestionadas con Supabase Auth (migrado de hardcoded — ✅ mejorado)
- Sin rate limiting en login — vulnerable a fuerza bruta
- Sin 2FA — acceso con solo email + contraseña
- RLS deshabilitado en blog_posts y quiz_config — riesgo si la anon key se compromete
- Sin sanitización formal de inputs
- Sin backup automático de base de datos
- Sesión en sessionStorage — vulnerable a XSS

## 2. Plan de implementación V3 — Seguridad avanzada

### Fase 1 — Autenticación real (Prioridad CRÍTICA)
| Tarea | Descripción | Complejidad |
|---|---|---|
| Migrar a Supabase Auth | Reemplazar login hardcodeado por auth.signInWithPassword() | Media |
| Bcrypt en servidor | Hashear contraseñas con bcrypt, validar en servidor | Media |
| Políticas RLS basadas en auth.uid() | Reemplazar USING(true) por auth.uid() = admin_id | Media |
| Rate limiting login | Bloquear IP después de 5 intentos fallidos en 15 min | Baja |
| Tokens de sesión rotativos | Refresh token cada 1 hora, access token cada 15 min | Media |
| Política de contraseñas estricta | 12+ caracteres, mayúscula, número, carácter especial, no repetir últimas 3 | Baja |

### Fase 2 — Protección de infraestructura (Prioridad ALTA)
| Tarea | Descripción | Complejidad |
|---|---|---|
| 2FA con TOTP | Google Authenticator / Authy para acceso al admin | Alta |
| CORS estricto | Funciones serverless solo aceptan requests del dominio panteraessence.co | Baja |
| CSP headers | Content-Security-Policy en Vercel para prevenir XSS | Baja |
| Encriptación AES-256 | Encriptar keys sensibles en Supabase (reemplazar base64) | Media |
| IP whitelist admin | Solo IPs autorizadas pueden acceder a /admin | Media |
| Sanitización de inputs | Validar y limpiar todos los formularios del admin contra SQL injection y XSS | Media |

### Fase 3 — Monitoreo y respuesta (Prioridad MEDIA)
| Tarea | Descripción | Complejidad |
|---|---|---|
| Webhooks de alertas | Notificar a WhatsApp/email: login desde IP nueva, cambio de contraseña, eliminación masiva | Alta |
| Logs de seguridad | Tabla separada con retención de 1 año para eventos de seguridad | Baja |
| Sesiones en Supabase | Mover sesiones de sessionStorage a tabla en Supabase (multi-dispositivo, revocables) | Media |
| Backup automático | Exportar toda la DB a JSON cada semana, guardar en Supabase Storage | Media |
| WAF | Web Application Firewall con Vercel o Cloudflare (bloqueo de bots, DDoS) | Media |

### Fase 4 — Auditoría externa (Prioridad BAJA)
| Tarea | Descripción | Complejidad |
|---|---|---|
| Pen testing trimestral | Pruebas de penetración manuales o con herramientas (OWASP ZAP) | Alta |
| npm audit mensual | Revisar y corregir vulnerabilidades de dependencias | Baja |
| Revisión de políticas RLS | Auditar todas las políticas cada 6 meses | Baja |
| Certificación SSL | Verificar que el certificado se renueve automáticamente (Vercel lo hace) | Baja |

## 3. Políticas de seguridad operativa

### Rotación de keys
| Key | Frecuencia | Dónde se cambia |
|---|---|---|
| Bold API Key | Cada 12 meses o si se compromete | Vercel dashboard + .env |
| Bold Secret Key | Cada 12 meses o si se compromete | Solo Vercel dashboard |
| Supabase Anon Key | Solo si se compromete | Vercel dashboard + .env |
| Anthropic API Key | Cada 12 meses o si se compromete | Vercel dashboard + .env |
| Contraseña admin | Cada 3 meses | Panel admin /admin/config |

### Manejo de incidentes
1. Si se compromete una API key: revocarla inmediatamente en el dashboard correspondiente, generar una nueva, actualizar en Vercel, hacer redeploy
2. Si se detecta acceso no autorizado al admin: cambiar contraseña, cerrar todas las sesiones, revisar audit_log, rotar todas las keys
3. Si se detecta inyección de datos: revisar audit_log, restaurar desde backup, sanitizar inputs, reportar
4. Si Supabase se cae: el sitio público sigue funcionando (lee del JSON local), solo el admin queda inactivo

### Checklist de seguridad mensual
- [ ] Ejecutar npm audit y corregir vulnerabilidades
- [ ] Verificar que RLS esté activo en todas las tablas
- [ ] Revisar audit_log por actividad sospechosa
- [ ] Verificar que .env no esté en el repositorio
- [ ] Confirmar que BOLD_SECRET_KEY no esté en el frontend
- [ ] Revisar logs de funciones serverless en Vercel
- [ ] Verificar uso de Supabase (límites free tier)

### Checklist de seguridad trimestral
- [ ] Rotar contraseña del admin
- [ ] Ejecutar Lighthouse y verificar Best Practices
- [ ] Revisar políticas RLS de todas las tablas
- [ ] Verificar que todas las keys funcionen correctamente
- [ ] Actualizar dependencias (npm outdated + npm update)
- [ ] Revisar que los backups se estén generando

## 4. Arquitectura de seguridad

### Capas de protección
1. Red: HTTPS (Vercel), DNS seguro
2. Aplicación: CORS, CSP headers, sanitización de inputs
3. Autenticación: Supabase Auth (V3), 2FA (V3), rate limiting (V3)
4. Autorización: RLS en Supabase, roles admin/super_admin
5. Datos: Encriptación en reposo (Supabase), encriptación de keys sensibles
6. Monitoreo: audit_log, webhooks de alertas, logs de seguridad
7. Recuperación: Backups automáticos, JSON local como fallback

### Datos sensibles y su ubicación
| Dato | Ubicación | Protección |
|---|---|---|
| Bold Secret Key | Vercel env vars | Nunca en frontend, solo en serverless |
| Anthropic API Key | Vercel env vars + .env local | Nunca en frontend, solo en serverless |
| Supabase Anon Key | .env + Vercel | Pública pero protegida con RLS |
| Contraseña admin | sessionStorage (V2) / Supabase Auth (V3) | Hasheada con bcrypt (V3) |
| Datos de clientes | Supabase tabla orders | RLS, acceso solo lectura para admin |
| Datos de transferencia | Supabase site_config | Parcialmente visible en checkout |

## 5. Cumplimiento legal (Colombia)
- Ley 1581 de 2012 (Protección de datos personales): los datos de clientes (nombre, email, teléfono, dirección) se almacenan en Supabase con RLS. Agregar política de privacidad en el sitio (pendiente).
- Habeas data: implementar opción para que el cliente solicite eliminación de sus datos (pendiente V3).
- SIC (Superintendencia de Industria y Comercio): registrar base de datos si supera umbrales.

---

*Plan revisado y actualizado: 10 de mayo de 2026*
*Próxima revisión: 10 de agosto de 2026*
*Responsable: Aureliano*
