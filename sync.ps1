# Script de sincronización — Pantera Essence
# Uso: .\sync.ps1 "P1" "Descripción de lo que se hizo"

param(
    [string]$direccion,
    [string]$descripcion
)

cd C:\Users\USUARIO\Desktop\gerencia-pantera-essence
git pull origin main
git add .
git commit -m "$direccion · 11/05/2026 · $descripcion"
git push origin main
Write-Host "✅ GitHub actualizado correctamente"
